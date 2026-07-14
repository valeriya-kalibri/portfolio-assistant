"use client";

import { useEffect, useRef, useState } from "react";

type Message = { role: "user" | "assistant"; content: string };

const API_URL = process.env.NEXT_PUBLIC_CHATBOT_API_URL ?? "http://localhost:8000";

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi, I'm an AI assistant trained on Val's background. Ask me about her skills, experience, or projects.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage() {
    const text = input.trim();
    if (!text || loading) return;

    const nextMessages: Message[] = [...messages, { role: "user", content: text }];
    setMessages(nextMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          history: messages.map((m) => ({ role: m.role, content: m.content })),
        }),
      });
      const data = await res.json();
      setMessages([...nextMessages, { role: "assistant", content: data.response }]);
    } catch {
      setMessages([
        ...nextMessages,
        { role: "assistant", content: "Something went wrong reaching the backend. Is it running?" },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto flex h-[65vh] w-full min-h-0 flex-1 flex-col rounded-[10px] border border-gold/40 bg-[#141311] shadow-[0_0_30px_rgba(212,175,55,0.08)] sm:h-auto">
      <div className="flex-1 space-y-4 overflow-y-auto p-6">
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
            <span
              className={
                "inline-block max-w-[80%] rounded-lg px-4 py-3 text-lg " +
                (m.role === "user" ? "bg-gold font-medium text-ink" : "bg-white/10 text-white")
              }
            >
              {m.content}
            </span>
          </div>
        ))}
        {loading && <div className="text-left text-base text-white/40">Thinking...</div>}
        <div ref={bottomRef} />
      </div>
      <div className="flex gap-2 border-t border-gold/15 p-4">
        <input
          className="flex-1 rounded-md border border-white/10 bg-ink px-4 py-3 text-lg text-white outline-none focus:border-gold"
          placeholder="Ask about Val's skills, experience, or projects..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="rounded-md bg-gold px-6 py-3 text-lg font-semibold text-ink transition-shadow hover:bg-gold-light hover:shadow-[0_0_20px_rgba(212,175,55,0.35)] disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
