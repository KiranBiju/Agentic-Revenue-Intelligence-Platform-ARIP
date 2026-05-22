from langchain_core.prompts import PromptTemplate

from app.llm.provider import llm
from app.llm.prompts import OUTREACH_PROMPT


prompt = PromptTemplate.from_template(
    OUTREACH_PROMPT
)


outreach_chain = prompt | llm