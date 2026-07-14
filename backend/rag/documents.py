import io
import re
import uuid
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

from db.supabase_client import get_supabase
from rag.embedder import embed_text

STORAGE_BUCKET = "kb-documents"


def upsert_kb_document(*, slug: str, topic: str, title: str, content: str) -> dict:
    embedding = embed_text(content)
    return (
        get_supabase()
        .table("kb_documents")
        .upsert(
            {
                "slug": slug,
                "topic": topic,
                "title": title,
                "content": content,
                "embedding": embedding,
                "source_type": "seed",
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
            on_conflict="slug",
        )
        .execute()
        .data[0]
    )


def _replace_admin_document(
    title: str, source_type: str, storage_path: str | None
) -> None:
    supabase = get_supabase()
    existing = (
        supabase.table("kb_documents")
        .select("id, storage_path")
        .eq("title", title)
        .eq("source_type", source_type)
        .execute()
    )
    for doc in existing.data:
        if doc.get("storage_path"):
            supabase.storage.from_(STORAGE_BUCKET).remove([doc["storage_path"]])
        supabase.table("kb_documents").delete().eq("id", doc["id"]).execute()


def store_uploaded_pdf(title: str, filename: str, file_bytes: bytes) -> dict:
    supabase = get_supabase()
    storage_path = f"{uuid.uuid4()}-{filename}"
    supabase.storage.from_(STORAGE_BUCKET).upload(
        storage_path, file_bytes, {"content-type": "application/pdf"}
    )

    reader = PdfReader(io.BytesIO(file_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    _replace_admin_document(title, "upload", storage_path)
    embedding = embed_text(text)
    return (
        supabase.table("kb_documents")
        .insert(
            {
                "slug": f"upload-{uuid.uuid4().hex[:8]}",
                "topic": "other",
                "title": title,
                "content": text,
                "embedding": embedding,
                "source_type": "upload",
                "storage_path": storage_path,
            }
        )
        .execute()
        .data[0]
    )


def store_url_document(title: str, url: str) -> dict:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = re.sub(r"\n{3,}", "\n\n", soup.get_text("\n")).strip()

    _replace_admin_document(title, "url", None)
    embedding = embed_text(text)
    return (
        get_supabase()
        .table("kb_documents")
        .insert(
            {
                "slug": f"url-{uuid.uuid4().hex[:8]}",
                "topic": "other",
                "title": title,
                "content": text,
                "embedding": embedding,
                "source_type": "url",
            }
        )
        .execute()
        .data[0]
    )


def list_documents() -> list[dict]:
    return (
        get_supabase()
        .table("kb_documents")
        .select("id, slug, topic, title, source_type, created_at")
        .order("created_at", desc=True)
        .execute()
        .data
    )


def delete_document(document_id: str) -> None:
    supabase = get_supabase()
    doc = (
        supabase.table("kb_documents")
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
    supabase.table("kb_documents").delete().eq("id", document_id).execute()
