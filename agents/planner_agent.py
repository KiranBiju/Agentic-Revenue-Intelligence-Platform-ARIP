from typing import Dict, Any, List

from app.agents.base_agent import BaseAgent
from app.core.logging import logger


class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="PlannerAgent")

    def execute(
        self,
        selected_leads: List[Dict[str, Any]],
        campaign_metadata: Dict[str, Any]
    ) -> Dict[int, Dict[str, Any]]:

        logger.info("[PLANNER] Building per-lead strategies")

        strategies = {}

        for lead in selected_leads:

            role = str(lead.get("role", "")).lower()
            user_id = lead.get("user_id")

            if "founder" in role:

                strategy = {
                    "tone": "persuasive",
                    "channel": "email",
                    "follow_up": True,
                    "personalization_level": "high"
                }

            elif "engineer" in role:

                strategy = {
                    "tone": "technical",
                    "channel": "linkedin",
                    "follow_up": False,
                    "personalization_level": "medium"
                }

            else:

                strategy = {
                    "tone": "professional",
                    "channel": "email",
                    "follow_up": False,
                    "personalization_level": "low"
                }

            strategies[user_id] = strategy

        logger.info("[PLANNER] Per-lead strategies created")

        return strategies