"use client";

import { useState } from "react";
import { useAuth } from "@/lib/auth";
import { useToast } from "@/lib/toast";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface SubmitReviewProps {
  placeId: string;
  placeName: string;
  onSubmitted?: () => void;
}

export default function SubmitReview({ placeId, placeName, onSubmitted }: SubmitReviewProps) {
  const { user } = useAuth();
  const { toast } = useToast();
  const [open, setOpen] = useState(false);
  const [rating, setRating] = useState(5);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ sentiment: { label: string; score: number }; trust_score: number } | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!text.trim()) return;
    setLoading(true);
    try {
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (user) headers.Authorization = `Bearer ${user.token}`;

      const res = await fetch(`${API_BASE}/api/reviews/submit`, {
        method: "POST",
        headers,
        body: JSON.stringify({ place_id: placeId, place_name: placeName, rating, text }),
      });
      const data = await res.json();
      setResult(data);
      toast("Review đã gửi thành công!", "success");
      setText("");
      onSubmitted?.();
    } catch {
      toast("Có lỗi xảy ra", "error");
    } finally {
      setLoading(false);
    }
  }

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="text-sm text-sky-600 hover:text-sky-700 font-medium flex items-center gap-1"
      >
        <span>+</span> Viết review
      </button>
    );
  }

  return (
    <div className="border border-sky-200 bg-sky-50/50 rounded-xl p-4 mt-3">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-medium text-sm">Viết review cho {placeName}</h4>
        <button onClick={() => setOpen(false)} className="text-gray-400 hover:text-gray-600 text-sm">✕</button>
      </div>

      {result ? (
        <div className="text-center py-3">
          <div className="text-green-600 font-medium mb-2">Cảm ơn bạn đã review!</div>
          <div className="flex justify-center gap-4 text-xs text-gray-500">
            <span>Sentiment: {Math.round(result.sentiment.score * 100)}% ({result.sentiment.label})</span>
            <span>Trust: {Math.round(result.trust_score * 100)}%</span>
          </div>
          <button onClick={() => { setResult(null); setOpen(false); }} className="text-xs text-sky-600 mt-2">Đóng</button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-3">
          {/* Rating */}
          <div>
            <label className="text-xs text-gray-500 block mb-1">Đánh giá</label>
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  onClick={() => setRating(star)}
                  className={`text-2xl transition ${star <= rating ? "text-yellow-400" : "text-gray-300"}`}
                >
                  ★
                </button>
              ))}
            </div>
          </div>

          {/* Text */}
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Chia sẻ trải nghiệm của bạn... (ví dụ: đẹp lắm, giá 150k, nên đi sáng sớm)"
            rows={3}
            required
            minLength={10}
            className="w-full px-3 py-2 rounded-lg border border-gray-200 text-sm focus:border-sky-500 outline-none resize-none"
          />

          <div className="flex items-center justify-between">
            <span className="text-[10px] text-gray-400">
              {user ? `Đăng với tên: ${user.email}` : "Đăng ẩn danh"} • AI sẽ phân tích sentiment + trust
            </span>
            <button
              type="submit"
              disabled={loading || text.length < 10}
              className="px-4 py-2 bg-sky-600 text-white text-sm rounded-lg hover:bg-sky-700 disabled:opacity-50 transition"
            >
              {loading ? "Đang gửi..." : "Gửi review"}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
