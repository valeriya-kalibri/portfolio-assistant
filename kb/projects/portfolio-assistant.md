# Project: Portfolio Assistant (this chatbot)

This assistant — the one you're talking to right now — is itself one of Valeriya's
projects, built to answer recruiter and hiring-manager questions about her
background, skills, and experience conversationally instead of forcing a flat resume
read.

The problem with a static portfolio page is that different visitors care about
different things — one recruiter wants a quick skills match, another wants to dig
into how a specific project was architected — and a page can't adapt to that. A
retrieval-augmented chatbot can.

Architecture: a FastAPI backend orchestrates a LangGraph state machine. An intent
classifier routes each incoming message into one of three branches — questions about
Valeriya, meta questions about the assistant itself, or off-topic — rather than a
binary in/out classifier, because "are you an AI?" and "what's a good pizza topping?"
need different handling. For on-topic questions, a query-rewriting step
contextualizes follow-ups against chat history before retrieval runs, so a
pronoun-heavy follow-up like "why that one?" still resolves to the right search
query instead of embedding "why that one?" literally and retrieving nothing useful.

Retrieval runs over a Supabase Postgres database with the pgvector extension. The
knowledge base is deliberately chunked one document per topic — identity, career
timeline, each individual project, skills, and so on — rather than split by token
windows. That means every retrieved chunk is a complete, self-contained answer, not
a fragment that cuts off mid-thought. The frontend is Next.js with TypeScript.

This project is worth calling out specifically because it's simultaneously a working
tool and a demonstration piece: the same category of decisions that make this
assistant hold up under real conversation — topic-based chunking, contextual query
rewriting, graceful degradation instead of hard refusals when retrieval comes up
empty — are the decisions that matter on a client-facing production RAG system.
