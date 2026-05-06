import os
import logging
from typing import List, Dict
from dotenv import load_dotenv

from app.schemas.lead import LeadInput
from app.ml.services.scoring_service import score_leads

load_dotenv()

logger = logging.getLogger(__name__)

class DecisionOrchestrator:

    def __init__(self):
        self.state = {}

    def run_campaign(self, leads: List[LeadInput]) -> Dict:
        total_leads = len(leads)

        logger.info(f"Received {total_leads} leads")

        #Score leads
        ranked_leads = score_leads(leads, top_n=None)

        logger.info(f"Scored {len(ranked_leads)} leads")

        #Log top score
        top_score = ranked_leads[0]["priority_score"] if ranked_leads else 0
        logger.info(f"Top lead score: {top_score}")

        #Apply constraint
        max_outreach = int(os.getenv("MAX_OUTREACH", 10))

        limit = min(max_outreach, len(ranked_leads))

        selected_leads = ranked_leads[:limit]

        logger.info(f"Selected top {len(selected_leads)} leads")

        #Store state
        self.state["selected_leads"] = selected_leads

        return {
            "total_leads": total_leads,
            "selected": len(selected_leads),
            "top_score": top_score,
            "ranked_leads": ranked_leads[:5],
        }