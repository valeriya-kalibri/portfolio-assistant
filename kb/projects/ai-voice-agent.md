# Project: AI Front Desk Voice Agent

A voice-based AI agent for automated customer engagement — handling live spoken
phone conversations end-to-end: answering, qualifying the caller, and booking. This
is the voice half of Kalibri Studios' "AI Front Desk" product line, built for small
businesses that lose revenue every time a call goes to voicemail.

Voice introduces two constraints that text-based chat doesn't have. First, turn-taking
— the system has to reliably tell the difference between a caller pausing to think
and a caller actually being done talking, which is a much harder problem than it
sounds and directly affects whether the conversation feels natural or annoying.
Second, recoverability — a bad turn in a text chat can be silently retried or edited
by the user; a bad moment on a live phone call can't be undone, so there's less
margin for the system to "figure it out as it goes."

Those constraints push the design toward telephony integration paired with explicit
state management via structured output — the agent always knows which stage of the
call it's in (greeting, qualifying, booking, confirming) rather than improvising
purely from the raw transcript. That structure is what makes the difference between
a voice agent that sounds impressive in a controlled demo and one that holds up on a
real, messy phone call.
