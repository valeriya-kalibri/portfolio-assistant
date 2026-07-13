from typing import TypedDict

from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: list[BaseMessage]
    query: str
    intent: str
    rag_results: list[dict]
    response: str
