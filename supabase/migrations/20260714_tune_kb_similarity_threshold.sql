-- CLAUDE.md's original defaults (match_count=3, similarity_threshold=0.75) were
-- explicitly flagged as unvalidated starting points. Stress-tested against the actual
-- 16-doc corpus: with text-embedding-3-small, the correct document's cosine similarity
-- ranged from 0.69 down to 0.19 depending on phrasing (a meta question like "how were
-- you built?" only reached 0.19, ranked 4th of 16) -- 0.75 excluded the correct answer
-- in every test query. Retuned so top_k does the real limiting and the threshold only
-- trims clearly-unrelated docs.

create or replace function match_kb_documents(
  query_embedding vector(1536),
  match_count int default 6,
  similarity_threshold float default 0.15
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
