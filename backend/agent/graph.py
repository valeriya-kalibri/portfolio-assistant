from langgraph.graph import END, StateGraph

from agent.nodes import classify_intent, generate_response, rag_search
from agent.state import AgentState


def _route_after_classify(state: AgentState) -> str:
    return "rag_search" if state["intent"] == "about_me" else "generate_response"


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("rag_search", rag_search)
    graph.add_node("generate_response", generate_response)

    graph.set_entry_point("classify_intent")
    graph.add_conditional_edges(
        "classify_intent",
        _route_after_classify,
        {"rag_search": "rag_search", "generate_response": "generate_response"},
    )
    graph.add_edge("rag_search", "generate_response")
    graph.add_edge("generate_response", END)

    return graph.compile()


agent_graph = build_graph()
