import os

from openai import OpenAI

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


def embed_text(text: str) -> list[float]:
    model = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
    response = _get_client().embeddings.create(model=model, input=text)
    return response.data[0].embedding
