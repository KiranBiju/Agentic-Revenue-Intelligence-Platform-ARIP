from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid


@dataclass
class CampaignState:
    #Identity
    campaign_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_traces: list = field(default_factory=list)
    
    #Input
    input_leads: List[Any] = field(default_factory=list)
    scored_leads: List[Dict[str, Any]] = field(default_factory=list)
    selected_leads: List[Dict[str, Any]] = field(default_factory=list)

    
    #Strategy metadata
    strategy: Dict[str, Any] = field(default_factory=dict)

    #Final output

    results: Dict[str, Any] = field(default_factory=dict)

    status: str = "initialized"  # initialized → processing → completed → failed

    #Observability

    logs: List[str] = field(default_factory=list)

    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    #Helper methods

    def add_trace(
        self,
        agent: str,
        action: str,
        outcome: str
    ):

        self.agent_traces.append({
            "agent": agent,
            "action": action,
            "outcome": outcome,
            "timestamp": datetime.utcnow().isoformat()
        })

    def add_log(self, message: str):
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)

    def update_status(self, new_status: str):
        self.status = new_status
        self.add_log(f"Status changed to: {new_status}")