from typing import Dict


class LLMProvider:

    def generate(
        self,
        prompt: str,
        metadata: Dict = None
    ) -> str:

        """
        Placeholder abstraction layer.

        Future:
        - OpenAI
        - Claude
        - Gemini
        - Local LLMs
        """

        return prompt