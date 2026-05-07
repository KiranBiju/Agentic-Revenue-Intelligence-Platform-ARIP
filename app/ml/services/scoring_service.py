import logging
import time
from typing import List, Dict, Optional

from app.schemas.lead import LeadInput
from app.ml.model.lead_model import LeadScoringModel

logger = logging.getLogger(__name__)

#Config
DEFAULTS = {
    "years_experience": 3,
    "company_size": 100,
    "activity_score": 5,
    "role_score": 5
}

ROLE_MAPPING = {
    "intern": 2,
    "engineer": 5,
    "manager": 7,
    "founder": 9
}

TOP_N_DEFAULT = 10

#Load model once
model = LeadScoringModel()
model.load()


def score_leads(
    leads: List[LeadInput],
    top_n: Optional[int] = TOP_N_DEFAULT,
    sort_results: bool = True
) -> List[Dict]:

    start_time = time.perf_counter()

    results = []

    for lead in leads:
        try:
            #Feature construction
            role_value = getattr(lead, "role", None)

            role_score = ROLE_MAPPING.get(
                str(role_value).lower(), DEFAULTS["role_score"]
            ) if role_value else DEFAULTS["role_score"]

            features = {
                "years_experience": getattr(lead, "years_experience", DEFAULTS["years_experience"]) or DEFAULTS["years_experience"],
                "company_size": getattr(lead, "company_size", DEFAULTS["company_size"]) or DEFAULTS["company_size"],
                "activity_score": getattr(lead, "activity_score", DEFAULTS["activity_score"]) or DEFAULTS["activity_score"],
                "role_score": role_score
            }

            #Model prediction
            response_prob = model.predict_probab(features)

            #Derived scores
            conversion_prob = response_prob * 0.7
            priority_score = (0.6 * response_prob) + (0.4 * conversion_prob)

            results.append({
                "user_id": lead.user_id,
                "response_prob": round(response_prob, 4),
                "conversion_prob": round(conversion_prob, 4),
                "priority_score": round(priority_score, 4)
            })

        except Exception as e:
            logger.exception(f"Failed to score lead {lead.user_id}: {e}")

    #Sorting
    if sort_results:
        results.sort(key=lambda x: x["priority_score"], reverse=True)

    #Ranking
    for idx, item in enumerate(results):
        item["rank"] = idx + 1    

    #Top N selection
    if top_n is not None:
        results = results[:top_n]

    #Latency logging
    duration = time.perf_counter() - start_time
    logger.info(
        f"Scored {len(leads)} leads | returned {len(results)} | time={duration:.4f}s"
    )

    return results
    