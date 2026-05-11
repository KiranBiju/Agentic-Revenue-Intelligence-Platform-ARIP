from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(String, unique=True, index=True, nullable=False)
    total_leads = Column(Integer, nullable=False)
    selected_leads = Column(Integer, default=0)
    status = Column(String, default="running")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MessageResult(Base):
    __tablename__ = "mess_results"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(String, index=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    attempts = Column(Integer, default=1)
    channel = Column(String, default="email")
    message = Column(Text)
    failure_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())