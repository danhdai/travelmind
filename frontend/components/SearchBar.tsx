"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { API_BASE } from "@/lib/config";

interface SearchResult {
  type: "destination" | "place";
  name: string;
  emoji?: string;
  url: string;
  rating?: number;
  matches?: number;
}

export default function SearchBar({ onClose }: { onClose: () => void }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    if (query.length < 2) { setResults([]); return; }

    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        setResults([...data.destinations, ...data.places]);
      } catch {}
      setLoading(false);
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  function navigate(url: string) {
    router.push(url);
    onClose();
  }

  return (
    <div className="fixed inset-0 z-[200] bg-black/50 flex items-start justify-center pt-20" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg mx-4 overflow-hidden" onClick={(e) => e.stopPropagation()}>
        {/* Input */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-gray-100">
          <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Tìm điểm đến, địa điểm, review..."
            className="flex-1 outline-none text-sm"
            onKeyDown={(e) => { if (e.key === "Escape") onClose(); }}
          />
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-sm">ESC</button>
        </div>

        {/* Results */}
        <div className="max-h-80 overflow-y-auto">
          {loading && (
            <div className="p-4 text-center text-sm text-gray-400">Đang tìm...</div>
          )}

          {!loading && query.length >= 2 && results.length === 0 && (
            <div className="p-8 text-center">
              <div className="text-3xl mb-2">🔍</div>
              <p className="text-sm text-gray-500">Không tìm thấy kết quả cho &ldquo;{query}&rdquo;</p>
            </div>
          )}

          {results.map((r, i) => (
            <button
              key={i}
              onClick={() => navigate(r.url)}
              className="w-full flex items-center gap-3 px-4 py-3 hover:bg-sky-50 transition text-left"
            >
              <div className="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center text-sm">
                {r.type === "destination" ? r.emoji : "📍"}
              </div>
              <div className="flex-1">
                <div className="text-sm font-medium">{r.name}</div>
                <div className="text-xs text-gray-400">
                  {r.type === "destination" ? "Điểm đến" : `${r.matches} reviews • ★ ${r.rating}`}
                </div>
              </div>
              <svg className="w-4 h-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          ))}

          {/* Quick links */}
          {query.length < 2 && (
            <div className="p-4">
              <div className="text-xs text-gray-400 mb-2">Tìm kiếm nhanh</div>
              <div className="flex flex-wrap gap-2">
                {["Quảng Bình", "Đà Lạt", "Phú Quốc", "Hội An", "hang động", "biển", "coffee"].map((t) => (
                  <button
                    key={t}
                    onClick={() => setQuery(t)}
                    className="text-xs px-3 py-1.5 bg-gray-100 rounded-full hover:bg-sky-100 hover:text-sky-700 transition"
                  >
                    {t}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
