import requests

BASE_URL = "http://localhost:8000/api"


def run_campaign(payload):

    try:

        response = requests.post(
            f"{BASE_URL}/run-outreach",
            json=payload,
            timeout=300
        )

        return response.json()

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e),
            "ranked_leads": [],
            "selected_leads": [],
            "results": [],
            "logs": []
        }