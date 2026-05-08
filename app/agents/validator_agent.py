import re
from typing import Dict, Any, List

from app.agents.base_agent import BaseAgent
from app.core.logging import logger


class ValidatorAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="ValidatorAgent")

    def execute(
        self,
        generated_message: Dict[str, Any],
        strategy: Dict[str, Any]
    ) -> Dict[str, Any]:

        issues: List[str] = []

        message = generated_message.get("message", "")

        #Spam Detection

        if message.isupper():
            issues.append("Message is ALL CAPS")

        if "BUY NOW!!!" in message:
            issues.append("Spam phrase detected")

        excessive_punctuation = re.search(r"[!?.]{4,}", message)

        if excessive_punctuation:
            issues.append("Excessive punctuation detected")

        #Personalization

        personalization_checks = [
            "Hi ",
            " at "
        ]

        for token in personalization_checks:

            if token not in message:
                issues.append(
                    f"Missing personalization token: {token}"
                )

        #Tone Consistency

        tone = strategy.get("tone", "professional")

        aggressive_words = [
            "urgent",
            "buy now",
            "limited offer",
            "act immediately"
        ]

        if tone == "professional":

            lowered = message.lower()

            for word in aggressive_words:

                if word in lowered:
                    issues.append(
                        f"Aggressive wording detected: {word}"
                    )

        #Validation result

        valid = len(issues) == 0

        if valid:

            logger.info("[VALIDATOR] Validation passed")

        else:

            logger.warning(
                f"[VALIDATOR] Validation failed: {issues}"
            )

        return {
            "valid": valid,
            "issues": issues
        }