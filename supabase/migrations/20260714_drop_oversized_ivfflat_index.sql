-- The ivfflat index (lists = 100) is wildly oversized for a knowledge base
-- this small (dozens of chunks). With ~100 buckets for ~30 rows, most rows
-- sit alone in their own bucket, and the default probes = 1 only searches
-- the single nearest bucket to the query vector -- so genuinely relevant
-- chunks in a different bucket are silently missed, returning zero results
-- regardless of match_threshold. At this scale a sequential scan is both
-- fast and exact, so drop the approximate index rather than tune probes.

drop index if exists knowledge_chunks_embedding_idx;
