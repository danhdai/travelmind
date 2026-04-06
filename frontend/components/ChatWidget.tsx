"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatResponse {
  reply: string;
  suggestions: string[];
  related_places: string[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([
    "Nên đi đâu ở Quảng Bình?",
    "Chi phí bao nhiêu?",
    "Ăn gì ngon?",
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage(text: string) {
    if (!text.trim() || loading) return;
    const userMsg: Message = { role: "user", content: text };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");
    setLoading(true);
    setSuggestions([]);

    try {
      const res = await fetch(`${API_BASE}/api/concierge/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, history: newMessages.slice(-10) }),
      });
      const data: ChatResponse = await res.json();
      setMessages([...newMessages, { role: "assistant", content: data.reply }]);
      if (data.suggestions.length > 0) setSuggestions(data.suggestions);
    } catch {
      setMessages([...newMessages, { role: "assistant", content: "Xin lỗi, có lỗi xảy ra." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {/* Floating button */}
      <button
        onClick={() => setOpen(!open)}
        className={`fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full shadow-lg flex items-center justify-center transition-all duration-300 ${
          open ? "bg-gray-700 rotate-0" : "bg-sky-600 hover:bg-sky-700 hover:scale-110"
        }`}
      >
        {open ? (
          <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <span className="text-2xl">💬</span>
        )}
      </button>

      {/* Unread badge */}
      {!open && messages.length === 0 && (
        <div className="fixed bottom-[5.5rem] right-6 z-50 bg-white rounded-xl shadow-lg px-4 py-2 text-sm text-gray-700 animate-bounce">
          Hỏi tôi về du lịch!
          <div className="absolute -bottom-1 right-4 w-3 h-3 bg-white rotate-45 shadow" />
        </div>
      )}

      {/* Chat panel */}
      {open && (
        <div className="fixed bottom-24 right-6 z-50 w-[360px] max-h-[520px] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden">
          {/* Header */}
          <div className="bg-sky-600 text-white px-4 py-3 flex items-center gap-3">
            <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center text-sm">✈</div>
            <div className="flex-1">
              <div className="font-semibold text-sm">AI Concierge</div>
              <div className="text-[10px] text-sky-200">Online — Sẵn sàng hỗ trợ</div>
            </div>
            <a href="/chat" className="text-[10px] text-sky-200 hover:text-white underline">
              Mở rộng
            </a>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3 min-h-[200px] max-h-[320px]">
            {messages.length === 0 && (
              <div className="text-center py-6">
                <div className="text-3xl mb-2">✈</div>
                <p className="text-xs text-gray-500">Xin chào! Hỏi tôi về du lịch Việt Nam</p>
              </div>
            )}

            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[85%] rounded-2xl px-3 py-2 text-xs leading-relaxed ${
                    msg.role === "user"
                      ? "bg-sky-600 text-white rounded-br-sm"
                      : "bg-gray-100 text-gray-700 rounded-bl-sm"
                  }`}
                >
                  {msg.content.split("\n").map((line, j) => {
                    const parts = line.split(/(\*\*.*?\*\*)/g);
                    return (
                      <div key={j} className={j > 0 ? "mt-0.5" : ""}>
                        {parts.map((part, k) =>
                          part.startsWith("**") && part.endsWith("**") ? (
                            <strong key={k}>{part.slice(2, -2)}</strong>
                          ) : (
                            <span key={k}>{part}</span>
                          )
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-2xl rounded-bl-sm px-3 py-2">
                  <div className="flex gap-1">
                    <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                    <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                    <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Suggestions */}
          {suggestions.length > 0 && (
            <div className="px-3 py-1.5 flex gap-1.5 overflow-x-auto border-t border-gray-50">
              {suggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => sendMessage(s)}
                  className="whitespace-nowrap text-[10px] px-2 py-1 bg-sky-50 text-sky-700 rounded-full hover:bg-sky-100 transition flex-shrink-0"
                >
                  {s}
                </button>
              ))}
            </div>
          )}

          {/* Input */}
          <form
            onSubmit={(e) => { e.preventDefault(); sendMessage(input); }}
            className="border-t border-gray-100 px-3 py-2 flex gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Nhập câu hỏi..."
              className="flex-1 px-3 py-2 rounded-lg border border-gray-200 text-xs focus:border-sky-500 outline-none"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="px-3 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 disabled:opacity-40 transition"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
}
