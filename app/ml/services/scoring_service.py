import logging
from typing import List, Dict

from app.schemas.lead import LeadInput
from app.ml.model.lead_model import LeadScoringModel

logger = logging.getLogger(__name__)

# --- Load model once (important) ---
model = LeadScoringModel()
model.load()


def score_leads(leads: List[LeadInput]) -> List[Dict]:
    results = []

    for lead in leads:
        # --- Handle missing fields safely ---
        features = {
            "years_experience": getattr(lead, "years_experience", 3) or 3,
            "company_size": getattr(lead, "company_size", 100) or 100,
            "role_score": getattr(lead, "role", None),
            "activity_score": 5  # default (since not in schema yet)
        }

        # --- Convert role → role_score ---
        role_mapping = {
            "intern": 2,
            "engineer": 5,
            "manager": 7,
            "founder": 9
        }

        if features["role_score"]:
            features["role_score"] = role_mapping.get(
                str(features["role_score"]).lower(), 5
            )
        else:
            features["role_score"] = 5  # default

        try:
            # --- Model prediction ---
            response_prob = model.predict_probab(features)

            # --- Conversion score ---
            conversion_prob = response_prob * 0.7

            # --- Final priority score ---
            priority_score = (0.6 * response_prob) + (0.4 * conversion_prob)

            results.append({
                "user_id": lead.user_id,
                "response_prob": round(response_prob, 4),
                "conversion_prob": round(conversion_prob, 4),
                "priority_score": round(priority_score, 4)
            })

        except Exception as e:
            logger.error(f"Error scoring lead {lead.user_id}: {e}")

    return results