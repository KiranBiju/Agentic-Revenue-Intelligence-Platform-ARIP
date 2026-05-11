from fastapi import APIRouter, HTTPException

from app.db.session import SessionLocal
from app.db.crud import get_campaign_summary
from app.core.redis_client import get_campaign_progress

router = APIRouter(prefix="/api")


@router.get("/campaign-analytics/{campaign_id}")
def campaign_analytics(campaign_id: str):
    db = SessionLocal()
    try:
        summary = get_campaign_summary(db, campaign_id)
        if not summary:
            raise HTTPException(status_code=404, detail="Campaign not found")

        summary["progress"] = get_campaign_progress(campaign_id)
        return summary
    finally:
        db.close()