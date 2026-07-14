# Portfolio Assistant

A retrieval-augmented AI chatbot that answers questions about Valeriya Paine's
background, skills, and projects — built to demonstrate the same RAG/agent stack used
in production client work (FastAPI + LangGraph + Supabase pgvector), including the
document-ingestion pipeline (PDF/URL upload -> Storage -> chunk -> embed).

The frontend is a single-page landing site — photo, name, positioning line, links —
with the chatbot as the main interactive element. That page is the link shared with
employers.

## Architecture

```
frontend/   Next.js 15 (App Router) + TypeScript + Tailwind — landing page + chat UI
backend/    FastAPI + LangGraph agent + RAG over Supabase pgvector
kb/         Seed markdown content (about, skills, experience, projects)
supabase/   SQL migrations: pgvector, knowledge_chunks/documents, kb-documents bucket
```

## How the agent works

Each visitor message is classified as `about_me` or `off_topic` by the
`classify_intent` node. `about_me` queries are routed through `rag_search`, which
embeds the query with OpenAI and runs a pgvector similarity search against
`knowledge_chunks` in Supabase. `generate_response` then answers grounded in whatever
context came back — or, for `off_topic` messages, declines and redirects toward
Valeriya's work instead.

## Knowledge base & ingestion pipeline

Content reaches the vector store through three paths, all defined in
`backend/rag/documents.py` and landing in the same `knowledge_documents` /
`knowledge_chunks` tables so retrieval doesn't care how a chunk got there:

- **Seed content** — the markdown files in `kb/` (about, skills, experience,
  projects) are embedded by `ingest.py`. This is how the initial bio content got in.
- **PDF upload** — `store_uploaded_pdf` saves the file to the `kb-documents` Storage
  bucket, extracts text, chunks it, and embeds it. Exposed via
  `POST /kb/documents/upload`.
- **URL ingestion** — `store_url_document` fetches a page, strips HTML, chunks, and
  embeds. Exposed via `POST /kb/documents/url`.

`GET /kb/documents` lists what's currently ingested; `DELETE /kb/documents/{id}`
removes a document and its chunks (and its Storage object, if it has one). All four
`/kb/documents*` routes are gated by an `X-Admin-Key` header checked against the
`ADMIN_KEY` environment variable — there's no multi-tenant auth here, just a shared
secret since Valeriya is the only one managing this KB.

## Data layer

Two Supabase migrations set up the schema:

- `20260713_knowledge_base.sql` — enables the `pgvector` extension and creates
  `knowledge_documents`, `knowledge_chunks`, and the `match_knowledge_chunks` RPC used
  for similarity search.
- `20260714_kb_documents_storage.sql` — creates the private `kb-documents` Storage
  bucket and adds `source_type` / `storage_path` columns to `knowledge_documents` so
  seed, upload, and URL documents can be told apart and cleaned up correctly.

## Running it locally

The backend is a standard FastAPI app once `backend/.env` is populated with a
Supabase URL, service role key, OpenAI key, and a self-chosen `ADMIN_KEY`:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python ingest.py               # embeds kb/*.md as seed documents
uvicorn main:app --reload --port 8000
```

The frontend reads the backend's URL from `frontend/.env.local`
(`NEXT_PUBLIC_CHATBOT_API_URL`, defaulting to `http://localhost:8000` for local dev):

```bash
cd frontend
npm install
npm run dev
```

The landing page looks for a photo at `frontend/public/photo.jpg`, falling back to an
initials avatar if it isn't there. Links (GitHub, LinkedIn, press) live in
`frontend/src/lib/links.ts`.

## Deployment

The backend deploys to Railway (root directory `backend/`, start command
`uvicorn main:app --host 0.0.0.0 --port $PORT`, same env vars as `.env`). The frontend
deploys to Vercel (root directory `frontend/`, `NEXT_PUBLIC_CHATBOT_API_URL` pointed at
the Railway URL). The deployed Vercel URL is what goes in the GitHub README and
resume/LinkedIn as the live demo link — a local-only repo isn't reachable by anyone
else.

## Design notes

- The knowledge base intentionally excludes phone number; the assistant directs
  contact requests to email and LinkedIn instead.
- Seed ingestion is idempotent per title — re-running `ingest.py` replaces a
  document's chunks rather than duplicating them.
