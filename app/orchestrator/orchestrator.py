import os
from typing import List, Dict
from app.schemas.lead import LeadInput
from app.ml.services.scoring_service import score_leads
from app.orchestrator.state import CampaignState
from app.core.logging import logger


class DecisionOrchestrator:

    def __init__(self):
        self.state: CampaignState | None = None

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

        strategy = {
            "tone": "professional",
            "channel": "email"
        }

        self.state.strategy = strategy

        logger.info("[PLAN] Strategy created")

        self.state.add_log("[PLAN] Strategy created")

    #EXECUTION LOOP

    def execute_pipeline(self):

        logger.info("[EXEC] Processing selected leads")

        self.state.add_log("[EXEC] Processing selected leads")

        results = []

        for lead in self.state.selected_leads:

            result = {
                "user_id": lead["user_id"],
                "status": "pending"
            }

            results.append(result)

        self.state.results = results


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