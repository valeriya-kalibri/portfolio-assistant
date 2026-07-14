# Project: LeadPulse

An internal prospect-qualification tool she built to run Kalibri Studios' own sales
pipeline, not a client-facing product. It takes Apollo CSV exports, scrapes the
listed business websites, scores each lead Hot/Warm/Cold, generates AI-written
intel cards on demand for any lead she wants more context on, and syncs qualifying
leads into HubSpot — creating both a Contact and a Company record, so the CRM
reflects the actual relationship structure rather than a flat list of names.

She built it for internal use first rather than starting from "let's make this a
SaaS product" — the sequencing matters. Before offering a lead-scoring tool to
other businesses, she wanted to run it against her own outreach and prove the
scoring logic actually surfaces the leads worth spending time on, using real Apollo
exports from her own med spa prospecting. A multi-tenant SaaS version is a possible
future direction, but only after the internal version has proven itself, not before.

Technically, the interesting part is the scoring and enrichment layer: rather than
scoring leads purely on firmographic data pulled from Apollo, LeadPulse scrapes each
prospect's actual website to generate a contextual intel card — meaning the scoring
reflects what a business is actually doing right now, not just what category it
falls into on a CSV export. The HubSpot sync then has to correctly create and
associate both Contact and Company records rather than dumping everything into one
flat object, which is what keeps the CRM usable instead of turning into a pile of
duplicate, disconnected entries.
