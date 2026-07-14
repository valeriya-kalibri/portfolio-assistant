# Project: Business Operations Audit Agent

An agentic workflow that orchestrates a multi-step audit of a business's operations
— combining tool access, external API calls, and structured data handoff — to
produce a report a non-technical operator can actually act on.

This is a genuinely agentic problem rather than a single-prompt problem, and that
distinction matters. Auditing a business's operations means pulling data from
multiple sources, reasoning across all of it together, and producing a structured
deliverable at the end — not answering one question with one LLM call. That's a
better fit for a multi-step orchestrated workflow, where each step has a clear
responsibility (gather, analyze, synthesize, report) and can call external tools or
APIs as needed, than for one large prompt trying to do everything at once.

The output is designed deliberately for a non-technical audience: a business owner
running a med spa or a service business doesn't want a wall of AI-generated
commentary — they want a report that tells them what's working, what isn't, and
what to do next. Getting the agent design right here was as much about scoping what
the report should contain as it was about the orchestration itself.
