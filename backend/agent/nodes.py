import os
from datetime import date

from openai import OpenAI

from agent.prompts import (
    ABOUT_ME_SYSTEM_PROMPT,
    CLASSIFY_PROMPT,
    LOW_CONFIDENCE_INSTRUCTIONS,
    META_SYSTEM_PROMPT,
    OFF_TOPIC_SYSTEM_PROMPT,
    REWRITE_PROMPT,
)
from agent.state import AgentState
from rag.retriever import search_knowledge

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


def _chat_model() -> str:
    return os.environ.get("CHAT_MODEL", "gpt-4o-mini")


def _history_as_openai_messages(messages: list) -> list[dict]:
    role_map = {"human": "user", "ai": "assistant"}
    return [{"role": role_map.get(m.type, "user"), "content": m.content} for m in messages]


def classify_intent(state: AgentState) -> AgentState:
    completion = _get_client().chat.completions.create(
        model=_chat_model(),
        messages=[
            {"role": "system", "content": CLASSIFY_PROMPT},
            {"role": "user", "content": state["query"]},
        ],
        temperature=0,
    )
    label = completion.choices[0].message.content.strip().lower()
    state["intent"] = label if label in ("about_me", "meta", "off_topic") else "about_me"
    return state


def rewrite_query(state: AgentState) -> AgentState:
    history = state.get("messages") or []
    if not history:
        state["search_query"] = state["query"]
        return state

    completion = _get_client().chat.completions.create(
        model=_chat_model(),
        messages=[
            {"role": "system", "content": REWRITE_PROMPT},
            *_history_as_openai_messages(history),
            {"role": "user", "content": state["query"]},
        ],
        temperature=0,
    )
    state["search_query"] = completion.choices[0].message.content.strip()
    return state


def rag_search(state: AgentState) -> AgentState:
    query = state.get("search_query") or state["query"]
    state["rag_results"] = search_knowledge(query)
    return state


def generate_response(state: AgentState) -> AgentState:
    intent = state["intent"]

    if intent == "off_topic":
        system_prompt = OFF_TOPIC_SYSTEM_PROMPT
    else:
        rag_results = state.get("rag_results", [])
        context = "\n\n---\n\n".join(
            f"## {r['title']}\n\n{r['content']}" for r in rag_results
        ) or "(no matching context found)"

        template = ABOUT_ME_SYSTEM_PROMPT if intent == "about_me" else META_SYSTEM_PROMPT
        system_prompt = template.format(
            context=context,
            low_confidence_instructions=LOW_CONFIDENCE_INSTRUCTIONS if not rag_results else "",
            today=date.today().isoformat(),
        )

    history = _history_as_openai_messages(state.get("messages", []))

    completion = _get_client().chat.completions.create(
        model=_chat_model(),
        messages=[
            {"role": "system", "content": system_prompt},
            *history,
            {"role": "user", "content": state["query"]},
        ],
        temperature=0.3,
    )
    state["response"] = completion.choices[0].message.content
    return state
