# Project: RAG-Based Client Support Chatbot

A multi-tenant, white-label AI assistant platform: each client gets their own
embeddable chat widget, powered by a LangGraph agent doing retrieval-augmented
generation over that client's own knowledge base, plus a dashboard where the client
can view captured leads and conversation history. Stack: Next.js, Supabase
(Postgres + pgvector), Python with LangGraph and FastAPI.

The interesting engineering problem here isn't the chatbot itself — it's the
multi-tenancy. When multiple clients' knowledge bases live in one shared system, the
isolation between them can't just be an application-level filter that happens to be
correct today; it has to be enforced at the database layer, so a bug in the app code
can't leak one client's data into another client's retrieval results. Each tenant's
documents are embedded and stored under their own tenant identifier, and every
retrieval query is scoped to that tenant by row-level security, not by trusting the
application to remember to filter correctly.

That design choice matters more as the platform scales — it's the difference between
"multi-tenant in the demo" and "multi-tenant in a way that survives an audit." The
dashboard layer exists so a non-technical business owner can see what their chatbot
has actually been doing — what leads came in, what conversations happened — without
needing to touch the underlying system at all. That's a deliberate product decision:
the AI does the work, but the client still needs visibility into it to trust the
tool.
