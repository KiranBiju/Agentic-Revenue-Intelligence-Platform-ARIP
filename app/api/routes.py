from fastapi import APIRouter
from app.schemas.campaign import CampaignRequest, CampaignResponse
from app.orchestrator.orchestrator import DecisionOrchestrator

router = APIRouter(prefix="/api", tags=["Outreach"])

orchestrator = DecisionOrchestrator()


@router.post("/run-outreach")
async def run_outreach(request: CampaignRequest):
    
    result = orchestrator.run_campaign(request.leads)

    return {
        "status": "received",
        "processed_count": len(request.leads),
        "orchestrator_result": result
    }