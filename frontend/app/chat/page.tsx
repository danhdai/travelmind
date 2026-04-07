"use client";

import { useState, useRef, useEffect } from "react";
import { API_BASE } from "@/lib/config";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatResponse {
  reply: string;
  suggestions: string[];
  related_places: string[];
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([
    "Nên đi Quảng Bình mấy ngày?",
    "Chi phí trung bình bao nhiêu?",
    "Địa điểm nào hay nhất?",
    "Ăn gì ở Quảng Bình?",
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
        body: JSON.stringify({
          message: text,
          history: newMessages.slice(-10),
        }),
      });
      const data: ChatResponse = await res.json();
      setMessages([...newMessages, { role: "assistant", content: data.reply }]);
      if (data.suggestions.length > 0) {
        setSuggestions(data.suggestions);
      }
    } catch {
      setMessages([
        ...newMessages,
        { role: "assistant", content: "Xin lỗi, có lỗi xảy ra. Vui lòng thử lại." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    sendMessage(input);
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      {/* Header */}
      <div className="border-b border-gray-100 px-4 py-3 bg-white">
        <div className="max-w-3xl mx-auto flex items-center gap-3">
          <div className="w-10 h-10 bg-sky-100 rounded-full flex items-center justify-center text-lg">
            💬
          </div>
          <div>
            <h1 className="font-semibold">AI Concierge</h1>
            <p className="text-xs text-green-600">Online — Quảng Bình Expert</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto space-y-4">
          {/* Welcome */}
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="text-5xl mb-4">✈</div>
              <h2 className="text-xl font-bold mb-2">Xin chào! Tôi là AI Concierge</h2>
              <p className="text-gray-500 mb-6">
                Trợ lý du lịch Quảng Bình 24/7. Hỏi tôi bất cứ điều gì!
              </p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  msg.role === "user"
                    ? "bg-sky-600 text-white rounded-br-sm"
                    : "bg-gray-100 text-gray-800 rounded-bl-sm"
                }`}
              >
                <div className="text-sm whitespace-pre-wrap leading-relaxed">
                  {msg.content.split("\n").map((line, j) => {
                    // Bold **text**
                    const parts = line.split(/(\*\*.*?\*\*)/g);
                    return (
                      <div key={j} className={j > 0 ? "mt-1" : ""}>
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
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-2xl rounded-bl-sm px-4 py-3">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Suggestions */}
      {suggestions.length > 0 && (
        <div className="px-4 py-2 border-t border-gray-50">
          <div className="max-w-3xl mx-auto flex gap-2 overflow-x-auto pb-1">
            {suggestions.map((s) => (
              <button
                key={s}
                onClick={() => sendMessage(s)}
                className="whitespace-nowrap text-xs px-3 py-1.5 bg-sky-50 text-sky-700 rounded-full hover:bg-sky-100 transition flex-shrink-0"
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="border-t border-gray-200 px-4 py-3 bg-white">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Hỏi về Quảng Bình..."
            className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:border-sky-500 focus:ring-2 focus:ring-sky-100 outline-none text-sm"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="px-5 py-3 bg-sky-600 text-white rounded-xl hover:bg-sky-700 disabled:opacity-40 transition"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
}
