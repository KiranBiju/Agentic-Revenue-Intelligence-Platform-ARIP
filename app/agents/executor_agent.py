from typing import Dict, Any, Optional
from datetime import datetime
from app.agents.base_agent import BaseAgent
from app.core.logging import logger


class ExecutorAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="ExecutorAgent")

    def execute(
        self,
        lead: Dict[str, Any],
        strategy: Dict[str, Any],
        retry_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        retry_context = retry_context or {}

        user_id = lead.get("user_id")
        name = lead.get("name", "there")
        role = lead.get("role", "professional")
        company = lead.get("company", "your company")

        #Strategy defaults
        tone = strategy.get("tone", "professional")
        channel = strategy.get("channel", "email")

        #RETRY ADAPTATION

        #If validator says tone too aggressive
        if retry_context.get("soften_tone"):
            tone = "professional"

        #Short CTA for retry attempts
        short_cta = retry_context.get("short_cta", False)

        cta = (
            "Open to a quick chat?"
            if short_cta
            else "Would a short conversation next week make sense?"
        )

        #MESSAGE GENERATION

        if tone == "persuasive":

            message = (
                f"Hi {name},\n\n"
                f"I noticed your work as a {role} at {company}. "
                f"We're helping fast-moving teams improve outreach performance "
                f"through AI-driven workflows.\n\n"
                f"I'd love to show you how this could help your team.\n\n"
                f"{cta}\n"
            )

        elif tone == "technical":

            message = (
                f"Hi {name},\n\n"
                f"I saw that you're working as a {role} at {company}. "
                f"We've built an AI orchestration system that automates lead scoring, "
                f"ranking, and campaign execution.\n\n"
                f"I'd be happy to share technical details if you're interested.\n\n"
                f"{cta}\n"
            )

        else:

            message = (
                f"Hi {name},\n\n"
                f"I wanted to reach out regarding AI-powered outreach systems "
                f"for teams like yours at {company}.\n\n"
                f"{cta}\n"
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