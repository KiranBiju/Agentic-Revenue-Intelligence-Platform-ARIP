from typing import Dict, Any
from datetime import datetime

from app.agents.base_agent import BaseAgent
from app.core.logging import logger


class ExecutorAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="ExecutorAgent")

    def execute(
        self,
        lead: Dict[str, Any],
        strategy: Dict[str, Any]
    ) -> Dict[str, Any]:

        user_id = lead.get("user_id")
        name = lead.get("name", "there")
        role = lead.get("role", "professional")
        company = lead.get("company", "your company")

        tone = strategy.get("tone", "professional")
        channel = strategy.get("channel", "email")

        #Lightweight template generation

        if tone == "persuasive":

            message = (
                f"Hi {name},\n\n"
                f"I noticed your work as a {role} at {company}. "
                f"We're helping fast-moving teams improve outreach performance "
                f"through AI-driven workflows.\n\n"
                f"I'd love to show you how this could help your team.\n\n"
                f"Would you be open to a quick 15-minute chat?\n"
            )

        elif tone == "technical":

            message = (
                f"Hi {name},\n\n"
                f"I saw that you're working as a {role} at {company}. "
                f"We've built an AI orchestration system that automates lead scoring, "
                f"ranking, and campaign execution.\n\n"
                f"I'd be happy to share technical details if you're interested.\n\n"
                f"Would a short conversation next week make sense?\n"
            )

        else:

            message = (
                f"Hi {name},\n\n"
                f"I wanted to reach out regarding AI-powered outreach systems "
                f"for teams like yours at {company}.\n\n"
                f"Would you be open to learning more?\n"
            )

        logger.info(
            f"[EXECUTOR] Message generated for user {user_id}"
        )

        return {
            "user_id": user_id,
            "message": message,
            "channel": channel,
            "generated_at": datetime.utcnow().isoformat()
        }