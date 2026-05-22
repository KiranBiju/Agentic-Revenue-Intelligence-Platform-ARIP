from typing import TypedDict, List, Dict, Any


class ARIPState(TypedDict):

    campaign_id: str

    status: str

    leads: List[Dict[str, Any]]

    ranked_leads: List[Dict[str, Any]]

    selected_leads: List[Dict[str, Any]]

    strategy: Dict[str, Any]

    results: List[Dict[str, Any]]

    retries: int

    logs: List[str]

    total_leads: int

    selected: int

    processed: int

    top_score: float