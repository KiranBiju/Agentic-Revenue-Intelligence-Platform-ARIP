from typing import List, Dict, Any

from app.agents.base_agent import BaseAgent
from app.core.logging import logger


class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="PlannerAgent")

    def execute(
        self,
        selected_leads: List[Dict],
        campaign_metadata: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:

        logger.info("[PLANNER] Building outreach strategy")

        if not selected_leads:

            logger.warning("[PLANNER] No leads provided")

            return {
                "tone": "professional",
                "channel": "email",
                "follow_up": False,
                "personalization_level": "low"
            }

        #Simple deterministic strategy

        founder_count = 0
        engineer_count = 0

        for lead in selected_leads:

            role = str(lead.get("role", "")).lower()

            if "founder" in role:
                founder_count += 1

            elif "engineer" in role:
                engineer_count += 1

        #Strategy selection

        if founder_count > engineer_count:

            strategy = {
                "tone": "persuasive",
                "channel": "email",
                "follow_up": True,
                "personalization_level": "high"
            }

            logger.info(
                "[PLANNER] Founder-heavy campaign detected"
            )

        else:

            strategy = {
                "tone": "technical",
                "channel": "linkedin",
                "follow_up": False,
                "personalization_level": "medium"
            }

            logger.info(
                "[PLANNER] Engineer-heavy campaign detected"
            )

        #Logging

        logger.info(
            f"[PLANNER] Tone set to {strategy['tone']}"
        )

        logger.info(
            f"[PLANNER] Channel selected: {strategy['channel']}"
        )

        return strategy