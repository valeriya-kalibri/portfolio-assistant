# Portfolio Assistant

A retrieval-augmented AI chatbot that answers questions about Valeriya Paine's
background, skills, and projects — built to demonstrate the same RAG/agent stack used
in production client work (FastAPI + LangGraph + Supabase pgvector), including the
document-ingestion pipeline (PDF/URL upload -> Storage -> chunk -> embed).

Live: a single-page landing site (photo, name, positioning line, links) with the
chatbot as the main interactive element — this is the link to share with employers.

## Architecture

```
frontend/   Next.js 15 (App Router) + TypeScript + Tailwind — landing page + chat UI
backend/    FastAPI + LangGraph agent + RAG over Supabase pgvector
kb/         Seed markdown content (about, skills, experience, projects)
supabase/   SQL migrations: pgvector, knowledge_chunks/documents, kb-documents bucket
```

**Chat flow:** visitor message -> `classify_intent` (about_me / off_topic) ->
`rag_search` (OpenAI embeddings + Supabase pgvector similarity search) ->
`generate_response` (LLM answer grounded in retrieved context).

**Ingestion pipeline** (`rag/documents.py`):
- `store_seed_document` — used by `ingest.py` for the markdown files in `kb/`
- `store_uploaded_pdf` — PDF -> `kb-documents` Storage bucket -> text extraction -> chunk -> embed
- `store_url_document` — fetch a URL -> strip HTML -> chunk -> embed
- `list_documents` / `delete_document` — manage what's in the knowledge base

All three source types land in the same `knowledge_documents` / `knowledge_chunks`
tables, so `/chat` retrieval doesn't care how a chunk got there.

## Setup

### 1. Supabase

1. Create a free project at supabase.com.
2. Run both files in `supabase/migrations/` in the SQL editor, in order:
   - `20260713_knowledge_base.sql` — pgvector extension, tables, match function
   - `20260714_kb_documents_storage.sql` — `kb-documents` Storage bucket, source tracking columns
   - If the `insert into storage.buckets` statement errors on permissions, create the
     bucket manually instead: Dashboard -> Storage -> New bucket -> name it
     `kb-documents`, leave it **private**.
3. Grab your project URL and `service_role` key (Project Settings -> API).

### 2. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY, ADMIN_KEY
python ingest.py       # embeds kb/*.md into Supabase as seed documents
uvicorn main:app --reload --port 8000
```

`ADMIN_KEY` is your own secret — pick anything; it's the value you pass as the
`X-Admin-Key` header on `/kb/documents*` requests.

### 3. Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Add a photo at `frontend/public/photo.jpg` (falls back to an initials avatar if
missing). Edit `frontend/src/lib/links.ts` with your real GitHub URL and any
press/media links.

Open http://localhost:3000 and chat.

## Managing the knowledge base

Add a PDF:
```bash
curl -X POST http://localhost:8000/kb/documents/upload \
  -H "X-Admin-Key: $ADMIN_KEY" \
  -F "title=Some Doc Title" \
  -F "file=@/path/to/file.pdf"
```

Add a URL:
```bash
curl -X POST http://localhost:8000/kb/documents/url \
  -H "X-Admin-Key: $ADMIN_KEY" -H "Content-Type: application/json" \
  -d '{"title": "Some Page", "url": "https://example.com"}'
```

List / delete:
```bash
curl http://localhost:8000/kb/documents -H "X-Admin-Key: $ADMIN_KEY"
curl -X DELETE http://localhost:8000/kb/documents/<id> -H "X-Admin-Key: $ADMIN_KEY"
```

## Deployment (so recruiters can actually use it)

A local-only repo isn't reachable by anyone else — deploy both halves, same as the
real chatbot:

1. **Backend -> Railway**: new project from this repo, root directory `backend/`,
   start command `uvicorn main:app --host 0.0.0.0 --port $PORT`. Set the same env vars
   as `.env` in Railway's dashboard.
2. **Frontend -> Vercel**: new project from this repo, root directory `frontend/`. Set
   `NEXT_PUBLIC_CHATBOT_API_URL` to the deployed Railway URL.
3. Put the resulting Vercel URL in your GitHub README and resume/LinkedIn as the live
   demo link.

## Notes

- The knowledge base intentionally excludes phone number; the assistant directs
  contact requests to email and LinkedIn instead.
- `ingest.py` and `store_seed_document` are idempotent per title — re-running replaces
  that document's chunks rather than duplicating them.
