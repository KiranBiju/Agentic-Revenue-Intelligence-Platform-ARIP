from pydantic import BaseModel
from typing import List
from app.schemas.lead import LeadInput


class CampaignRequest(BaseModel):
    leads: List[LeadInput]


class CampaignResponse(BaseModel):
    status: str
    processed_count: int