"use client";

import { useState } from "react";

type Message = { role: "user" | "assistant"; content: string };

const API_URL = process.env.NEXT_PUBLIC_CHATBOT_API_URL ?? "http://localhost:8000";

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi, I'm an AI assistant trained on Lera's background. Ask me about her skills, experience, or projects.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

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
    <div className="mx-auto flex h-[80vh] w-full max-w-2xl flex-col rounded-xl border border-neutral-800 bg-neutral-900">
      <div className="flex-1 space-y-4 overflow-y-auto p-6">
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
            <span
              className={
                "inline-block max-w-[80%] rounded-lg px-4 py-2 text-sm " +
                (m.role === "user" ? "bg-blue-600 text-white" : "bg-neutral-800 text-neutral-100")
              }
            >
              {m.content}
            </span>
          </div>
        ))}
        {loading && <div className="text-left text-sm text-neutral-500">Thinking...</div>}
      </div>
      <div className="flex gap-2 border-t border-neutral-800 p-4">
        <input
          className="flex-1 rounded-md border border-neutral-700 bg-neutral-950 px-3 py-2 text-sm outline-none focus:border-blue-500"
          placeholder="Ask about Lera's skills, experience, or projects..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
