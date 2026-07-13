-- KB document upload pipeline: storage bucket + document source tracking.

insert into storage.buckets (id, name, public)
values ('kb-documents', 'kb-documents', false)
on conflict (id) do nothing;

alter table knowledge_documents
  add column if not exists source_type text not null default 'seed',
  add column if not exists storage_path text;

-- source_type: 'seed' (shipped kb/*.md via ingest.py) | 'upload' (PDF via /kb/documents) | 'url'
