# Project: AI Lead Capture Chatbot

An industry-specific conversational agent that qualifies inbound leads and captures
contact information, handing off structured lead data for follow-up.

The deliberate design choice here is narrow scope. A chatbot that tries to answer
every possible question about a business ends up answering none of them well —
qualification logic and conversation flow are tuned to the specific industry it's
deployed for, built around the actual buying signals that matter in that vertical
(for a med spa, that might be treatment interest and location; for a different
service business, it's a different set of signals entirely). That specificity is
what makes the qualification useful to the business owner on the other end, rather
than producing a pile of unqualified contact records that still need to be sorted
through manually — which defeats the point of automating lead capture in the first
place.
