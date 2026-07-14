from typing import Literal, TypedDict

from langchain_core.messages import BaseMessage

Intent = Literal["about_me", "meta", "off_topic"]


class AgentState(TypedDict):
    messages: list[BaseMessage]
    query: str
    search_query: str
    intent: Intent
    rag_results: list[dict]
    response: str
