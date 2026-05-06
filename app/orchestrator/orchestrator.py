import logging
from typing import List
from app.schemas.lead import LeadInput

logger = logging.getLogger(__name__)


class DecisionOrchestrator:
    
    def run_campaign(self, leads: List[LeadInput]) -> dict:
        lead_count = len(leads)

        logger.info(f"Received {lead_count} leads for campaign")

        # Dummy logic 
        return {
            "selected": 1,
            "messages_sent": 1
        }