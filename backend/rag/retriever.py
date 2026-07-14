import os

from db.supabase_client import get_supabase
from rag.embedder import embed_text


def _default_top_k() -> int:
    return int(os.environ.get("RAG_TOP_K", "6"))


def _default_threshold() -> float:
    return float(os.environ.get("RAG_SIMILARITY_THRESHOLD", "0.15"))


def search_knowledge(
    query: str, top_k: int | None = None, threshold: float | None = None
) -> list[dict]:
    embedding = embed_text(query)
    response = get_supabase().rpc(
        "match_kb_documents",
        {
            "query_embedding": embedding,
            "match_count": top_k if top_k is not None else _default_top_k(),
            "similarity_threshold": threshold if threshold is not None else _default_threshold(),
        },
    ).execute()
    return response.data or []
