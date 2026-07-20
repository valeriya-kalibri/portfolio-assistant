# Portfolio Assistant

A retrieval-augmented AI chatbot that answers questions about Valeriya Paine's
background, skills, and projects — built to demonstrate the same RAG/agent stack used
in production client work (FastAPI + LangGraph + Supabase pgvector), including the
document-ingestion pipeline (PDF/URL upload -> Storage -> extract -> embed).

The frontend is a single-page landing site — photo, name, positioning line, links —
with the chatbot as the main interactive element. That page is the link shared with
employers.

## Architecture

```
frontend/   Next.js 15 (App Router) + TypeScript + Tailwind — landing page + chat UI
backend/    FastAPI + LangGraph agent + RAG over Supabase pgvector
kb/         18 topic-coherent seed docs (identity, career, venture, 8 projects, skills,
            education, press, faq, personality, assistant's own architecture, her
            3D/VR production background)
supabase/   SQL migrations: pgvector, kb_documents (single-table, whole-doc chunking),
            kb-documents Storage bucket
```

## How the agent works

Each visitor message is classified by the `classify_intent` node into one of three
labels: `about_me`, `meta` (questions about the assistant itself — its architecture,
whether it's an AI), or `off_topic`. `about_me` queries first pass through
`rewrite_query`, which contextualizes follow-ups ("why that one?") against chat
history into a standalone search query before retrieval; `meta` queries skip
rewriting and go straight to retrieval. Both then hit `rag_search`, which embeds the
query with OpenAI and runs a pgvector similarity search (`match_kb_documents`) against
`kb_documents` in Supabase. `generate_response` answers grounded in whatever context
came back, using a branch-specific system prompt — or, for `off_topic` messages,
declines and redirects toward Valeriya's work instead without hitting retrieval at
all.

## Knowledge base & ingestion pipeline

Content reaches the vector store through three paths, all defined in
`backend/rag/documents.py` and landing in the same `kb_documents` table so retrieval
doesn't care how a document got there. Nothing is sub-split — each row is one
complete, topic-coherent document, embedded and retrieved as a single chunk:

- **Seed content** — the 18 markdown files in `kb/` (identity, career timeline, the
  Kalibri Studios venture, eight individual projects, skills, education, press, FAQ,
  personality, the assistant's own architecture, and her 3D/VR production background)
  are embedded by `backend/rag/ingest.py`, run via `python -m scripts.run_ingest` from
  `backend/`. This is how the initial bio content got in.
- **PDF upload** — `store_uploaded_pdf` saves the file to the `kb-documents` Storage
  bucket, extracts text, and embeds it whole. Exposed via
  `POST /kb/documents/upload`.
- **URL ingestion** — `store_url_document` fetches a page, strips HTML, and embeds the
  resulting text whole. Exposed via `POST /kb/documents/url`.

`GET /kb/documents` lists what's currently ingested; `DELETE /kb/documents/{id}`
removes a document (and its Storage object, if it has one). All four `/kb/documents*`
routes are gated by an `X-Admin-Key` header checked against the `ADMIN_KEY`
environment variable — there's no multi-tenant auth here, just a shared secret since
Valeriya is the only one managing this KB.

## Data layer

The schema went through a rework: the original two-table `knowledge_documents` /
`knowledge_chunks` model (generic character-sliding-window chunking) was replaced by a
single `kb_documents` table, one row per topic-coherent whole document. Current
Supabase migrations, in order:

- `20260713_knowledge_base.sql` — original two-table schema (`knowledge_documents`,
  `knowledge_chunks`) and the `match_knowledge_chunks` RPC. Superseded below.
- `20260714_kb_documents_storage.sql` — creates the private `kb-documents` Storage
  bucket and adds `source_type` / `storage_path` columns.
- `20260714_drop_oversized_ivfflat_index.sql` — drops the ivfflat index on the old
  table; at this corpus size (dozens of rows) it was silently missing relevant
  matches, and a sequential scan is both faster and exact.
- `20260714_lower_match_threshold.sql` — intermediate threshold tuning on the old
  schema.
- `20260714_kb_documents_rebuild.sql` — the actual rebuild: creates `kb_documents`
  (with a `kb_topic` enum, an HNSW index, and `source_type`/`storage_path` for
  seed/upload/url documents) and the `match_kb_documents` RPC, then drops the old
  `knowledge_chunks` / `knowledge_documents` tables entirely.
- `20260714_tune_kb_similarity_threshold.sql` — retunes `match_kb_documents` defaults
  to `match_count=6`, `similarity_threshold=0.15` after stress-testing showed the
  original `0.75` starting point excluded the correct document on every test query
  (real cosine similarities ranged 0.19–0.69). `RAG_TOP_K` / `RAG_SIMILARITY_THRESHOLD`
  env vars (`backend/.env`) mirror these defaults.

## Running it locally

The backend is a standard FastAPI app once `backend/.env` is populated with a
Supabase URL, service role key, OpenAI key, and a self-chosen `ADMIN_KEY`:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m scripts.run_ingest   # embeds kb/*.md as seed documents
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

## CI

`.github/workflows/ingest-kb.yml` re-runs `python -m scripts.run_ingest` against the
production Supabase project whenever a push to `main` touches `kb/**`, so editing a
seed doc and merging is enough to update the live KB — no manual re-ingestion step.

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
- Seed ingestion is idempotent per `slug` — re-running `python -m scripts.run_ingest`
  upserts each document in place (`ON CONFLICT (slug)`) rather than duplicating it.
