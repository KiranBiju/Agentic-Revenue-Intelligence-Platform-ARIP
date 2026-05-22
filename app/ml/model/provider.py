import os
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq


class LLMProvider:

    def __init__(self):

        self.provider = os.getenv(
            "LLM_PROVIDER",
            "groq"
        ).lower()


    def get_llm(self):


        if self.provider == "groq":

            return ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"),
                model=os.getenv(
                    "GROQ_MODEL",
                    "llama-3.3-70b-versatile"
                ),
                temperature=0.7
            )


        elif self.provider == "openai":

            return ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                model=os.getenv(
                    "OPENAI_MODEL",
                    "gpt-4o-mini"
                ),
                temperature=0.
            )


        raise ValueError(
            f"Unsupported LLM provider: {self.provider}"
        )