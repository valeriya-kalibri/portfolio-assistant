import os

from openai import OpenAI

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


CLASSIFY_PROMPT = """Classify the visitor's message into exactly one of:
- about_me: anything about Lera's background, skills, experience, projects, education, \
availability, or how to contact her
- off_topic: anything unrelated to Lera professionally (weather, general trivia, etc.)

Respond with only the single label, nothing else."""


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
    state["intent"] = label if label in ("about_me", "off_topic") else "about_me"
    return state


def rag_search(state: AgentState) -> AgentState:
    state["rag_results"] = search_knowledge(state["query"])
    return state


SYSTEM_PROMPT_TEMPLATE = """You are an AI assistant representing Valeriya "Lera" Paine \
on her portfolio site. You answer recruiters' and hiring managers' questions about her \
background, skills, experience, and projects.

Rules:
- Answer only from the context below. If the context doesn't cover the question, say \
you don't have that detail and suggest reaching out to Lera directly at \
Lera.Paine@gmail.com or linkedin.com/in/valeriya-paine.
- For questions unrelated to Lera professionally: politely decline and redirect to what \
Lera does.
- When asked how to contact her or about her availability, share her email and \
LinkedIn. Never share a phone number — she does not want it public.
- Keep answers concise and conversational.

Context:
{context}
"""


def generate_response(state: AgentState) -> AgentState:
    context = "\n\n".join(chunk["content"] for chunk in state.get("rag_results", []))
    if not context:
        context = "(no matching context found)"

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)

    if state["intent"] == "off_topic":
        system_prompt = (
            "You are an AI assistant representing Valeriya \"Lera\" Paine. The "
            "visitor's question is unrelated to her professionally. Politely decline "
            "and redirect them to ask about her background, skills, or projects."
        )

    role_map = {"human": "user", "ai": "assistant"}
    history = [
        {"role": role_map.get(m.type, "user"), "content": m.content}
        for m in state.get("messages", [])
    ]

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
