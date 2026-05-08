from pydantic import BaseModel, EmailStr
from typing import Optional


class LeadInput(BaseModel):
    user_id: int
    name: str
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    years_experience: int = 3
    company: str | None = None
    company_size: int = 100
    activity_score: int = 5