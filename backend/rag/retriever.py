from db.supabase_client import get_supabase
from rag.embedder import embed_text


def search_knowledge(query: str, top_k: int = 5, threshold: float = 0.5) -> list[dict]:
    embedding = embed_text(query)
    response = get_supabase().rpc(
        "match_knowledge_chunks",
        {
            "query_embedding": embedding,
            "match_count": top_k,
            "match_threshold": threshold,
        },
    ).execute()
    return response.data or []
