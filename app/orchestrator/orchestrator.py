import os
from uuid import uuid4
from datetime import datetime
from typing import List, Dict
from app.schemas.lead import LeadInput
from app.ml.services.scoring_service import score_leads
from app.orchestrator.state import CampaignState
from app.agents.planner_agent import PlannerAgent
from app.agents.executor_agent import ExecutorAgent
from app.agents.validator_agent import ValidatorAgent
from app.core.logging import logger
from app.orchestrator.state import AgentTrace


class DecisionOrchestrator:
    
    MAX_RETRIES = 3

    def __init__(self):
        self.state: CampaignState | None = None
        self.planner_agent = PlannerAgent()
        self.executor_agent = ExecutorAgent()
        self.validator_agent = ValidatorAgent()

    #INITIALIZE CAMPAIGN

    def initialize_campaign(self, leads: List[LeadInput]):

        self.state = CampaignState()

        self.state.input_leads = leads
        self.state.update_status("processing")

        total = len(leads)

        logger.info("[INIT] Campaign started")
        logger.info(f"[INIT] Received {total} leads")

        self.state.add_log("[INIT] Campaign started")
        self.state.add_log(f"[INIT] Received {total} leads")

    #ML SCORING

    def score_leads(self):

        scored = score_leads(self.state.input_leads, top_n=None)

        self.state.scored_leads = scored

        logger.info(f"[ML] Scored {len(scored)} leads")

        self.state.add_log(f"[ML] Scored {len(scored)} leads")

    #TOP-K SELECTION

    def select_top_leads(self):

        max_outreach = int(os.getenv("MAX_OUTREACH", 10))

        selected = self.state.scored_leads[:max_outreach]

        self.state.selected_leads = selected

        logger.info(f"[SELECT] Top {len(selected)} leads selected")

        self.state.add_log(
            f"[SELECT] Top {len(selected)} leads selected"
        )

    #STRATEGY PLANNING

    def plan_strategy(self):

        strategy = self.planner_agent.execute(
        selected_leads=self.state.selected_leads,
        campaign_metadata={}
    )

        self.state.strategy = strategy

        logger.info("[PLAN] Strategy created")

        self.state.add_log("[PLAN] Strategy created")


    #EXECUTION LOOP

    def execute_pipeline(self):

        logger.info("[EXEC] Processing selected leads")

        self.state.add_log("[EXEC] Processing selected leads")

        results = []

        for lead in self.state.selected_leads:

            user_id = lead["user_id"]

            success = False
            attempts = 0
            validation_issues = []

            retry_context = {}

            while attempts < self.MAX_RETRIES:

                 attempts += 1

                #EXECUTION

                 generated = self.executor_agent.execute(
                    lead=lead,
                    strategy=self.state.strategy,
                    retry_context=retry_context
                )

                 self.state.add_trace(
                    agent="ExecutorAgent",
                    action="generate_message",
                    outcome=f"attempt_{attempts}"
                )

                #VALIDATION

                 validation = self.validator_agent.execute(
                     generated_message=generated,
                     strategy=self.state.strategy
                 )

                 self.state.add_trace(
                    agent="ValidatorAgent",
                    action="validate_message",
                    outcome="passed" if validation["valid"] else "failed"
                 )

                 #SUCCESS

                 if (
                     validation["valid"]
                     and validation["quality_score"] >= 0.75
                ):

                     results.append({
                        "user_id": user_id,
                        "status": "success",
                        "attempts": attempts,
                        "message": generated["message"],
                        "channel": generated["channel"],
                        "quality_score": validation["quality_score"],
                        "validation_issues": []
                     })

                     success = True

                     break

                    #FAILURE

                 validation_issues = validation["issues"]

                 logger.warning(
                    f"[RETRY] Validation failed for user {user_id} "
                    f"(attempt {attempts})"
                 )

                 #Retry strategy
                 retry_context = {
                    "soften_tone": True,
                    "short_cta": True
                 }

                #MAX RETRIES

            if not success:

                logger.error(
                    f"[FAILED] Validation failed after retries "
                    f"for user {user_id}"
                 )

                results.append({
                    "user_id": user_id,
                    "status": "failed",
                    "attempts": attempts,
                    "reason": "validation_failed",
                    "validation_issues": validation_issues
                })

        self.state.results = results

    def add_agent_trace(
        self,
        agent: str,
        action: str,
        input_data,
        output_data,
        latency: float,
        success: bool
):

        trace = AgentTrace(
            trace_id=str(uuid4()),
            campaign_id=self.state.campaign_id,
            agent=agent,
            action=action,
            input_data=input_data,
            output_data=output_data,
            latency=latency,
            success=success,
            timestamp=datetime.utcnow().isoformat()
        )

        self.state.agent_traces.append(trace.__dict__)    


    def finalize_campaign(self) -> Dict:

        self.state.update_status("completed")

        total_leads = len(self.state.input_leads)
        selected = len(self.state.selected_leads)
        processed = len(self.state.results)

        top_score = (
            self.state.selected_leads[0]["priority_score"]
            if self.state.selected_leads else 0
        )

        logger.info("[DONE] Campaign completed")

        self.state.add_log("[DONE] Campaign completed")

        return {
            "campaign_id": self.state.campaign_id,
            "status": self.state.status,
            "total_leads": total_leads,
            "selected": selected,
            "processed": processed,
            "top_score": top_score,
            "strategy": self.state.strategy,
            "results": self.state.results,
            "ranked_leads": self.state.scored_leads[:5],
            "logs": self.state.logs[-10:]
        }

    #MAIN PIPELINE CONTROLLER

    def run_campaign(self, leads: List[LeadInput]) -> Dict:

        try:

            #Step 1
            self.initialize_campaign(leads)

            #Step 2
            self.score_leads()

            #Step 3
            self.select_top_leads()

            #Step 4
            self.plan_strategy()

            #Step 5
            self.execute_pipeline()

            #Step 6
            return self.finalize_campaign()

        except Exception as e:

            logger.exception("[ERROR] Campaign failed")

            if self.state:
                self.state.update_status("failed")
                self.state.add_log(f"[ERROR] {str(e)}")

            return {
                "status": "failed",
                "error": str(e)
            }