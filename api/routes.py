from fastapi import APIRouter, HTTPException

from app.schemas.campaign import (
    CampaignRequest
)

from app.orchestrator.orchestrator import (
    DecisionOrchestrator
)

from app.db.session import SessionLocal

from app.db.crud import (
    get_campaign_summary
)

from app.core.redis_client import (
    get_campaign_progress
)

router = APIRouter(
    prefix="/api",
    tags=["Outreach"]
)

orchestrator = DecisionOrchestrator()


@router.post("/run-outreach")
async def run_outreach(
    request: CampaignRequest
):

    try:

        result = orchestrator.run_campaign(
            request.leads
        )

        normalized_response = {

    # Campaign status
            "status": result.get(
                "status",
                "completed"
             ),

    # Campaign ID
            "campaign_id": result.get(
                "campaign_id",
                ""
            ),

    # Metrics
            "total_leads": result.get(
                "total_leads",
                len(request.leads)
            ),

            "selected": result.get(
                "selected",
                0
            ),

            "processed": result.get(
                "processed",
                0
            ),

            "top_score": result.get(
                "top_score",
                0
            ),

    # Ranked leads
            "ranked_leads": result.get(
                "ranked_leads",
                []
            ),

    # Selected leads
            "selected_leads": result.get(
                "selected_leads",
                []
            ),

    # FIXED FIELD NAME
            "results": result.get(
                "results",
                []
            ),

    # Logs
            "logs": result.get(
                "logs",
                []
            ),

    # Agent traces
            "agent_traces": result.get(
                "agent_traces",
                []
            )
        }
        
        return normalized_response

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e),
            "total_leads": 0,
            "selected_leads": [],
            "ranked_leads": [],
            "results": [],
            "logs": []
        }


@router.get(
    "/campaign-status/{campaign_id}"
)
def campaign_status(
    campaign_id: str
):

    db = SessionLocal()

    try:

        summary = get_campaign_summary(
            db,
            campaign_id
        )

        if not summary:

            raise HTTPException(
                status_code=404,
                detail="Campaign not found"
            )

        summary["progress"] = (
            get_campaign_progress(
                campaign_id
            )
        )

        return summary

    finally:

        db.close()