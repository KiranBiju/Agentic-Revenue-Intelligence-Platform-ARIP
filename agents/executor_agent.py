from typing import Dict, Any, Optional
from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.agents.base_agent import BaseAgent
from app.ml.model.provider import LLMProvider
from app.core.logging import logger


class ExecutorAgent(BaseAgent):

    def __init__(self):

        super().__init__(name="ExecutorAgent")

        self.llm_provider = LLMProvider()

        self.llm = self.llm_provider.get_llm()

        self.parser = StrOutputParser()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an elite AI sales outreach agent.

Your job is to generate highly personalized outreach messages.

RULES:
- Be concise
- Avoid spammy tone
- Keep message under 120 words
- Sound human and professional
- Personalize using role and company
- Include a soft CTA
- Never use hype language
- Never use excessive punctuation
"""
                ),

                (
                    "human",
                    """
Generate a {tone} outreach message.

Lead Details:
Name: {name}
Role: {role}
Company: {company}

Channel: {channel}

CTA:
{cta}
"""
                )
            ]
        )

        self.chain = (
            self.prompt
            | self.llm
            | self.parser
        )


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


        tone = strategy.get("tone", "professional")

        channel = strategy.get("channel", "email")


        if retry_context.get("soften_tone"):

            tone = "professional"

        short_cta = retry_context.get(
            "short_cta",
            False
        )

        cta = (
            "Open to a quick chat?"
            if short_cta
            else "Would a short conversation next week make sense?"
        )


        try:

            message = self.chain.invoke(
                {
                    "tone": tone,
                    "name": name,
                    "role": role,
                    "company": company,
                    "channel": channel,
                    "cta": cta
                }
            )

        except Exception as e:

            logger.error(
                f"[EXECUTOR] LLM generation failed "
                f"for user {user_id}: {str(e)}"
            )


            message = (
                f"Hi {name},\n\n"
                f"I noticed your work as a {role} at {company}. "
                f"We're helping teams improve outreach workflows "
                f"using AI-driven automation.\n\n"
                f"{cta}"
            )

        logger.info(
            f"[EXECUTOR] Message generated for user {user_id}"
        )

        return {
            "user_id": user_id,
            "message": message.strip(),
            "channel": channel,
            "tone": tone,
            "generated_at": datetime.utcnow().isoformat()
        }