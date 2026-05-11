import re
from typing import Dict, Any

from app.agents.base_agent import BaseAgent
from app.core.logging import logger


class ValidatorAgent(BaseAgent):

    MAX_MESSAGE_LENGTH = 500

    def __init__(self):
        super().__init__(name="ValidatorAgent")

    def execute(
        self,
        generated_message: Dict[str, Any],
        strategy: Dict[str, Any]
    ) -> Dict[str, Any]:

        issues = []

        message = generated_message.get("message", "")
        tone = strategy.get("tone", "professional")

        quality_score = 1.0

        #SPAM CHECK

        if re.search(r"[A-Z]{6,}", message):
            issues.append("Possible ALL CAPS spam")
            quality_score -= 0.2

        if "!!!" in message:
            issues.append("Excessive punctuation")
            quality_score -= 0.1

        if message.count("AI") > 2:
            issues.append("Too many AI mentions")
            quality_score -= 0.1

        #MESSAGE LENGTH

        if len(message) > self.MAX_MESSAGE_LENGTH:
            issues.append("Message too long")
            quality_score -= 0.2

        #PERSONALIZATION

        if "Hi there" in message:
            issues.append("Weak personalization")
            quality_score -= 0.2

        if "your company" in message:
            issues.append("Missing company personalization")
            quality_score -= 0.2

        #REPETITIVE CTA

        if message.count("quick chat") > 1:
            issues.append("Repetitive CTA")
            quality_score -= 0.1

        #TONE CONSISTENCY

        if tone == "professional":

            aggressive_words = [
                "buy now",
                "limited offer",
                "act immediately"
            ]

            for word in aggressive_words:
                if word.lower() in message.lower():
                    issues.append("Aggressive tone mismatch")
                    quality_score -= 0.2

        quality_score = max(0.0, round(quality_score, 2))

        valid = quality_score >= 0.7 and len(issues) == 0

        if valid:
            logger.info("[VALIDATOR] Validation passed")
        else:
            logger.warning(f"[VALIDATOR] Validation failed: {issues}")

        return {
            "valid": valid,
            "issues": issues,
            "quality_score": quality_score
        }