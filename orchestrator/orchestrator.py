import os
import time
from uuid import uuid4
from datetime import datetime
from typing import List, Dict, TypedDict
from langgraph.graph import StateGraph, END
from app.schemas.lead import LeadInput
from app.ml.services.scoring_service import score_leads
from app.orchestrator.state import CampaignState
from app.orchestrator.state import AgentTrace
from app.agents.planner_agent import PlannerAgent
from app.agents.executor_agent import ExecutorAgent
from app.agents.validator_agent import ValidatorAgent
from app.core.logging import logger

class GraphState(TypedDict):

    input_leads: List[LeadInput]

    scored_leads: list

    selected_leads: list

    strategy: dict

    results: list

    current_lead_index: int

    campaign_id: str

    status: str

    logs: list


class DecisionOrchestrator:

    MAX_RETRIES = 3

    def __init__(self):

        self.state: CampaignState | None = None

        self.planner_agent = PlannerAgent()

        self.executor_agent = ExecutorAgent()

        self.validator_agent = ValidatorAgent()

        self.graph = self._build_graph()

    def _build_graph(self):

        workflow = StateGraph(GraphState)

        workflow.add_node(
            "initialize_campaign",
            self.initialize_campaign_node
        )

        workflow.add_node(
            "score_leads",
            self.score_leads_node
        )

        workflow.add_node(
            "select_top_leads",
            self.select_top_leads_node
        )

        workflow.add_node(
            "plan_strategy",
            self.plan_strategy_node
        )

        workflow.add_node(
            "execute_pipeline",
            self.execute_pipeline_node
        )

        workflow.add_node(
            "finalize_campaign",
            self.finalize_campaign_node
        )

        workflow.set_entry_point(
            "initialize_campaign"
        )

        workflow.add_edge(
            "initialize_campaign",
            "score_leads"
        )

        workflow.add_edge(
            "score_leads",
            "select_top_leads"
        )

        workflow.add_edge(
            "select_top_leads",
            "plan_strategy"
        )

        workflow.add_edge(
            "plan_strategy",
            "execute_pipeline"
        )

        workflow.add_edge(
            "execute_pipeline",
            "finalize_campaign"
        )

        workflow.add_edge(
            "finalize_campaign",
            END
        )

        return workflow.compile()

    def initialize_campaign_node(
        self,
        state: GraphState
    ):

        self.state = CampaignState()

        self.state.input_leads = state[
            "input_leads"
        ]

        self.state.update_status(
            "processing"
        )

        total = len(
            state["input_leads"]
        )

        logger.info(
            "[INIT] Campaign started"
        )

        logger.info(
            f"[INIT] Received {total} leads"
        )

        self.state.add_log(
            "[INIT] Campaign started"
        )

        self.state.add_log(
            f"[INIT] Received {total} leads"
        )

        return {
            **state,

            "campaign_id":
                self.state.campaign_id,

            "status": "processing",

            "logs": self.state.logs
        }

    def score_leads_node(
        self,
        state: GraphState
    ):

        scored = score_leads(
            self.state.input_leads,
            top_n=None
        )

        self.state.scored_leads = scored

        logger.info(
            f"[ML] Scored {len(scored)} leads"
        )

        self.state.add_log(
            f"[ML] Scored {len(scored)} leads"
        )

        return {
            **state,

            "scored_leads": scored,

            "ranked_leads": scored,

            "logs": self.state.logs
        }

    def select_top_leads_node(
        self,
        state: GraphState
    ):

        max_outreach = int(
            os.getenv(
                "MAX_OUTREACH",
                10
            )
        )

        selected = state[
            "scored_leads"
        ][:max_outreach]

        self.state.selected_leads = selected

        logger.info(
            f"[SELECT] Top {len(selected)} leads selected"
        )

        self.state.add_log(
            f"[SELECT] Top {len(selected)} leads selected"
        )

        return {
            **state,

            "selected_leads": selected,

            "logs": self.state.logs
        }

    def plan_strategy_node(
        self,
        state: GraphState
    ):

        start = time.time()

        strategy = self.planner_agent.execute(
            selected_leads=state[
                "selected_leads"
            ],
            campaign_metadata={}
        )

        latency = time.time() - start

        self.state.strategy = strategy

        logger.info(
            "[PLAN] Strategy created"
        )

        self.state.add_log(
            "[PLAN] Strategy created"
        )

        self.add_agent_trace(
            agent="PlannerAgent",

            action="plan_strategy",

            input_data={
                "selected_count": len(
                    state["selected_leads"]
                )
            },

            output_data=strategy,

            latency=latency,

            success=True
        )

        return {
            **state,

            "strategy": strategy,

            "logs": self.state.logs
        }

    def execute_pipeline_node(
        self,
        state: GraphState
    ):

        logger.info(
            "[EXEC] Processing selected leads"
        )

        self.state.add_log(
            "[EXEC] Processing selected leads"
        )

        results = []

        for lead in state[
            "selected_leads"
        ]:

            user_id = lead["user_id"]

            success = False

            attempts = 0

            validation_issues = []

            retry_context = {}

            while attempts < self.MAX_RETRIES:

                attempts += 1

                exec_start = time.time()

                try:

                    generated = (
                        self.executor_agent.execute(
                            lead=lead,
                            strategy=state[
                                "strategy"
                            ],
                            retry_context=retry_context
                        )
                    )

                except Exception as e:

                    logger.error(
                        f"[EXECUTOR] "
                        f"Generation failed "
                        f"for user {user_id}: "
                        f"{str(e)}"
                    )

                    generated = {
                        "message":
                            "Fallback outreach message.",
                        "channel":
                            "email"
                    }

                exec_latency = (
                    time.time() - exec_start
                )

                self.add_agent_trace(
                    agent="ExecutorAgent",

                    action="generate_message",

                    input_data=lead,

                    output_data=generated,

                    latency=exec_latency,

                    success=True
                )

                val_start = time.time()

                validation = (
                    self.validator_agent.execute(
                        generated_message=generated,
                        strategy=state[
                            "strategy"
                        ]
                    )
                )

                val_latency = (
                    time.time() - val_start
                )

                self.add_agent_trace(
                    agent="ValidatorAgent",

                    action="validate_message",

                    input_data=generated,

                    output_data=validation,

                    latency=val_latency,

                    success=validation["valid"]
                )

                if (
                    validation["valid"]
                    and validation[
                        "quality_score"
                    ] >= 0.75
                ):

                    results.append({

                        "user_id": user_id,

                        "status": "success",

                        "attempts": attempts,

                        "message":
                            generated.get(
                                "message",
                                ""
                            ),

                        "channel":
                            generated.get(
                                "channel",
                                "email"
                            ),

                        "quality_score":
                            validation.get(
                                "quality_score",
                                0
                            ),

                        "validation_issues": []
                    })

                    success = True

                    break

                validation_issues = (
                    validation.get(
                        "issues",
                        []
                    )
                )

                logger.warning(
                    f"[RETRY] "
                    f"Validation failed "
                    f"for user {user_id} "
                    f"(attempt {attempts})"
                )

                retry_context = {
                    "soften_tone": True,
                    "short_cta": True
                }

            if not success:

                logger.error(
                    f"[FAILED] Validation failed "
                    f"after retries "
                    f"for user {user_id}"
                )

                results.append({

                    "user_id": user_id,

                    "status": "failed",

                    "attempts": attempts,

                    "reason":
                        "validation_failed",

                    "validation_issues":
                        validation_issues
                })

        self.state.results = results

        return {
            **state,

            "results": results,

            "logs": self.state.logs
        }

    def finalize_campaign_node(self, state: GraphState):

        self.state.update_status("completed")

        total_leads = len(self.state.input_leads)

        selected_count = len(self.state.selected_leads)

        processed_count = len(self.state.results)

        top_score = 0

        if self.state.selected_leads:

           top_score = self.state.selected_leads[0].get(
               "priority_score",
                0
           )

        logger.info("[DONE] Campaign completed")

        self.state.add_log(
             "[DONE] Campaign completed"
        )

        ranked_leads = self.state.scored_leads[:5]

        successful_results = [
            r for r in self.state.results
            if r.get("status") == "success"
        ]

        return {

            # Core
            "campaign_id": self.state.campaign_id,
            "status": self.state.status,

        # Snake case
            "total_leads": total_leads,
            "selected": selected_count,
            "processed": processed_count,
            "top_score": top_score,
            "ranked_leads": ranked_leads,

        # Camel case compatibility
            "totalLeads": total_leads,
            "selectedLeads": selected_count,
            "processedLeads": processed_count,
            "topScore": top_score,
            "rankedLeads": ranked_leads,

        # Data
            "strategy": self.state.strategy,
            "results": self.state.results,
            "successful_results": successful_results,

        # Logs
            "logs": self.state.logs[-20:],

        # Traces
            "agent_traces": self.state.agent_traces
        }

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

            campaign_id=
                self.state.campaign_id,

            agent=agent,

            action=action,

            input_data=input_data,

            output_data=output_data,

            latency=latency,

            success=success,

            timestamp=datetime.utcnow()
            .isoformat()
        )

        self.state.agent_traces.append(
            trace.__dict__
        )

    def run_campaign(    
        self,
        leads: List[LeadInput]
    ) -> Dict:
 
        result = {}

        try:

            initial_state = {

                "input_leads": leads,

                "scored_leads": [],

                "selected_leads": [],

                "strategy": {},

                "results": [],

                "current_lead_index": 0,

                "campaign_id": "",

                "status": "initialized",

                "logs": []
            }

            result = self.graph.invoke(
                initial_state
            )

            return {

                "campaign_id":
                    result.get(
                        "campaign_id"
                    ),

                "status":
                    result.get(
                        "status"
                    ),

                "total_leads":
                    result.get(
                        "total_leads",
                        0
                    ),

                "selected":
                    len(
                        result.get(
                            "selected_leads",
                            []
                        )
                    ),    

                "processed":
                    len(
                       result.get(
                           "processed",
                           []
                    )   
                ),

                "top_score":
                   max(
                      [
                           lead.get("score", 0)
                           for lead in result.get(
                               "ranked_leads",
                               []
                           )
                      ],
                      default=0
                    ),

                "strategy":
                    result.get(
                        "strategy",
                        {}
                    ),

                "results":
                    result.get(
                        "results",
                        []
                    ),

                "ranked_leads":
                    result.get(
                        "ranked_leads",
                        []
                    ),

                "selected_leads":
                    result.get(
                        "selected_leads",
                        []
                    ),

                "logs":
                    result.get(
                        "logs",
                        []
                    ),

                "agent_traces":
                    result.get(
                        "agent_traces",
                        []
                    )
            }

        except Exception as e:

            logger.exception(
                "[ERROR] Campaign failed"
            )

            if self.state:

                self.state.update_status(
                    "failed"
                )

                self.state.add_log(
                    f"[ERROR] {str(e)}"
                )

            return {

    # IDs / status
                "campaign_id": result.get("campaign_id"),
                "status": result.get("status"),

    # Snake case
                "total_leads": result.get("total_leads", 0),
                "selected": result.get("selected", 0),
                "processed": result.get("processed", 0),
                "top_score": result.get("top_score", 0),
                "ranked_leads": result.get("ranked_leads", []),

    # Camel case compatibility
                "totalLeads": result.get("totalLeads", result.get("total_leads", 0)),
                "selectedLeads": result.get("selectedLeads", result.get("selected", 0)),
                "processedLeads": result.get("processedLeads", result.get("processed", 0)),
                "topScore": result.get("topScore", result.get("top_score", 0)),
                "rankedLeads": result.get("rankedLeads", result.get("ranked_leads", [])),

    # Data
                "strategy": result.get("strategy", {}),
                "results": result.get("results", []),
                "successful_results": result.get("successful_results", []),

    # Logs
                "logs": result.get("logs", []),

    # Agent traces
                "agent_traces": result.get("agent_traces", [])
            }

            