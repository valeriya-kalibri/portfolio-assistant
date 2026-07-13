import io
import re
import uuid

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

from db.supabase_client import get_supabase
from rag.chunking import chunk_text
from rag.embedder import embed_text

STORAGE_BUCKET = "kb-documents"


def _replace_document(title: str, source_type: str, storage_path: str | None) -> dict:
    supabase = get_supabase()

    existing = (
        supabase.table("knowledge_documents")
        .select("id")
        .eq("title", title)
        .execute()
    )
    for doc in existing.data:
        supabase.table("knowledge_documents").delete().eq("id", doc["id"]).execute()

    return (
        supabase.table("knowledge_documents")
        .insert({"title": title, "source_type": source_type, "storage_path": storage_path})
        .execute()
        .data[0]
    )


def _embed_and_store_chunks(document_id: str, text: str) -> int:
    supabase = get_supabase()
    chunks = chunk_text(text)
    for chunk in chunks:
        embedding = embed_text(chunk)
        supabase.table("knowledge_chunks").insert(
            {"document_id": document_id, "content": chunk, "embedding": embedding}
        ).execute()
    return len(chunks)


def store_seed_document(title: str, source_path: str, text: str) -> int:
    doc = _replace_document(title, "seed", None)
    return _embed_and_store_chunks(doc["id"], text)


def store_uploaded_pdf(title: str, filename: str, file_bytes: bytes) -> int:
    supabase = get_supabase()
    storage_path = f"{uuid.uuid4()}-{filename}"
    supabase.storage.from_(STORAGE_BUCKET).upload(
        storage_path, file_bytes, {"content-type": "application/pdf"}
    )

    reader = PdfReader(io.BytesIO(file_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    doc = _replace_document(title, "upload", storage_path)
    return _embed_and_store_chunks(doc["id"], text)


def store_url_document(title: str, url: str) -> int:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = re.sub(r"\n{3,}", "\n\n", soup.get_text("\n")).strip()

    doc = _replace_document(title, "url", url)
    return _embed_and_store_chunks(doc["id"], text)


def list_documents() -> list[dict]:
    return (
        get_supabase()
        .table("knowledge_documents")
        .select("id, title, source_type, created_at")
        .order("created_at", desc=True)
        .execute()
        .data
    )


def delete_document(document_id: str) -> None:
    supabase = get_supabase()
    doc = (
        supabase.table("knowledge_documents")
        .select("storage_path")
        .eq("id", document_id)
        .execute()
        .data
    )
    if not doc:
        return
    storage_path = doc[0].get("storage_path")
    if storage_path:
        supabase.storage.from_(STORAGE_BUCKET).remove([storage_path])
    supabase.table("knowledge_documents").delete().eq("id", document_id).execute()
