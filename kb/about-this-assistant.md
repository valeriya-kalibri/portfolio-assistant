# About This Assistant

This is a retrieval-augmented chatbot Valeriya built to represent her professionally
to recruiters and hiring managers — and it's also one of her own projects, so it's
fair game to ask about directly.

Under the hood: a FastAPI backend runs a LangGraph state graph. Every incoming
message first goes through an intent classifier with three branches — questions
about Valeriya, meta questions about this assistant itself (like the one you might
be asking right now), and off-topic questions — rather than a simple in-scope/
out-of-scope split.

For on-topic questions, a query-rewriting step runs before retrieval: it takes the
raw message plus recent chat history and produces a standalone search query with
pronouns and implicit references resolved, so a follow-up like "why that one?"
still retrieves the right context instead of searching for the literal, ambiguous
phrase. That step is skipped on the very first message of a conversation, since
there's no history yet to resolve against.

Retrieval itself runs over a Supabase Postgres database using the pgvector
extension for similarity search. The knowledge base this document is part of is
deliberately chunked one document per topic — this file, the career timeline, each
individual project, skills, and so on — rather than split by arbitrary token
windows. That matters: it means every retrieved chunk is a complete, self-contained
answer rather than a fragment cut off mid-thought, which is a big part of why this
assistant can handle follow-up questions and rephrasings instead of breaking on
anything slightly unexpected.

If a question doesn't match anything in the knowledge base with reasonable
confidence, the assistant is designed to say so plainly and point toward what it
can help with, or toward Valeriya's direct contact info — rather than guessing or
hallucinating an answer it doesn't actually have grounded.

The frontend is Next.js with TypeScript. The whole thing runs on OpenAI's API for
both chat and embeddings.
