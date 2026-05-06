from pydantic import BaseModel, EmailStr
from typing import Optional


class LeadInput(BaseModel):
    user_id: int
    name: str
    email: Optional[EmailStr] = None
    role: Optional[str] = None