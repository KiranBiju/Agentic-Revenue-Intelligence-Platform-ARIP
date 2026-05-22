from sqlalchemy.orm import Session
from app.db.models import Campaign, MessageResult


def create_campaign(db: Session, campaign_id: str, total_leads: int, selected_leads: int):
    campaign = Campaign(
        campaign_id=campaign_id,
        total_leads=total_leads,
        selected_leads=selected_leads,
        status="running",
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def update_campaign_status(db: Session, campaign_id: str, status: str):
    campaign = db.query(Campaign).filter(Campaign.campaign_id == campaign_id).first()
    if campaign:
        campaign.status = status
        db.commit()
    return campaign

def save_message_result(
    db: Session,
    campaign_id: str,
    user_id: int,
    status: str,
    attempts: int,
    channel: str,
    message: str,
    failure_reason: str | None = None,
):
    result = MessageResult(
        campaign_id=campaign_id,
        user_id=user_id,
        status=status,
        attempts=attempts,
        channel=channel,
        message=message,
        failure_reason=failure_reason,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

def get_campaign_summary(db: Session, campaign_id: str):
    campaign = db.query(Campaign).filter(Campaign.campaign_id == campaign_id).first()
    results = db.query(MessageResult).filter(MessageResult.campaign_id == campaign_id).all()

    if not campaign:
        return None

    sent = sum(1 for r in results if r.status == "sent")
    failed = sum(1 for r in results if r.status == "failed")

    return {
        "campaign_id": campaign.campaign_id,
        "status": campaign.status,
        "total_leads": campaign.total_leads,
        "selected_leads": campaign.selected_leads,
        "processed": len(results),
        "sent": sent,
        "failed": failed,
    }