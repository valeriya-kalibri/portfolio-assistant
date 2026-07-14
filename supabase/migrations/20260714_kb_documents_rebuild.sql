-- KB rebuild: single kb_documents table, one row per topic-coherent document.
-- Replaces the two-table knowledge_documents/knowledge_chunks model (undifferentiated
-- character-sliding-window chunking) with 16 curated, whole-document KB files, each
-- embedded and retrieved as a single unit -- no sub-splitting.

create extension if not exists vector;

create type kb_topic as enum (
  'identity', 'career', 'venture', 'project',
  'skills', 'education', 'press', 'faq', 'personality', 'meta',
  'other' -- ad-hoc admin-uploaded PDF/URL content; not one of the 16 curated kb/*.md docs
);

create table kb_documents (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  topic kb_topic not null,
  title text not null,
  content text not null,
  embedding vector(1536) not null,
  source_type text not null default 'seed', -- 'seed' (kb/*.md) | 'upload' (PDF) | 'url'
  storage_path text,                        -- Storage key, 'upload' rows only
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index kb_documents_embedding_idx
  on kb_documents using hnsw (embedding vector_cosine_ops);

alter table kb_documents enable row level security;
-- No policies added: service role only (bypasses RLS by design).

create or replace function match_kb_documents(
  query_embedding vector(1536),
  match_count int default 3,
  similarity_threshold float default 0.75
)
returns table (
  slug text,
  topic kb_topic,
  title text,
  content text,
  similarity float
)
language sql stable as $$
  select
    kb_documents.slug,
    kb_documents.topic,
    kb_documents.title,
    kb_documents.content,
    1 - (kb_documents.embedding <=> query_embedding) as similarity
  from kb_documents
  where 1 - (kb_documents.embedding <=> query_embedding) > similarity_threshold
  order by kb_documents.embedding <=> query_embedding
  limit match_count;
$$;

-- Old two-table schema fully superseded; nothing left reads it.
drop function if exists match_knowledge_chunks(vector, int, float);
drop table if exists knowledge_chunks;
drop table if exists knowledge_documents;

-- Note: the kb-documents storage bucket (from 20260714_kb_documents_storage.sql)
-- stays as-is -- still used for 'upload' rows via storage_path above.
