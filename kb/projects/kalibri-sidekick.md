# Project: Kalibri Sidekick. 

A Real-Time Call Coaching Assistant.
An AI assistant that listens to live sales calls and provides in-call guidance to
the sales rep as the conversation happens, using structured output pipelines and
telephony integration. Internally, this project is nicknamed "Sidekick."

The real-time constraint changes the entire shape of the problem compared to a
typical chatbot. This isn't request-and-response — it's a streaming pipeline that
has to keep pace with a live conversation, extract structured signals as they occur
(objections being raised, buying signals, how talk-time is split between rep and
prospect), and surface useful guidance to the rep without adding noticeable lag. A
long, free-form generation step doesn't fit that constraint, so the design leans
toward fast, structured output rather than open-ended text, and toward decoupling
"listen and detect" from "advise" as separate stages so each can be tuned and
optimized independently rather than as one monolithic step.

It's built and deployed, but not yet stress-tested in live call conditions — that's
the next milestone before deciding on a go-to-market path. Two options are on the
table: self-serve SaaS first to validate demand cheaply, or direct B2B team sales
into sales orgs that would get the most value from it. That decision is intentionally
being made after real usage data, not before.