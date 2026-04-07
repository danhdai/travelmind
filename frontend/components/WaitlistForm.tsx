"use client";

import { useState } from "react";
import { joinWaitlist } from "@/lib/api";

export default function WaitlistForm() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("loading");
    try {
      await joinWaitlist(email);
      setStatus("success");
      setMessage("Đăng ký thành công! Chúng tôi sẽ liên hệ bạn sớm.");
      setEmail("");
    } catch (err) {
      setStatus("error");
      setMessage(err instanceof Error ? err.message : "Có lỗi xảy ra, vui lòng thử lại");
    }
  }

  if (status === "success") {
    return (
      <div className="max-w-md mx-auto text-center">
        <div className="bg-green-50 border border-green-200 rounded-xl px-6 py-4">
          <div className="text-2xl mb-2">✓</div>
          <p className="text-green-700 font-medium">{message}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
        <input
          type="email"
          required
          placeholder="Email của bạn..."
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="flex-1 px-4 py-3 rounded-lg border border-gray-300 focus:border-sky-500 focus:ring-2 focus:ring-sky-200 outline-none transition text-sm"
        />
        <button
          type="submit"
          disabled={status === "loading"}
          className="px-6 py-3 bg-orange-500 text-white font-semibold rounded-lg hover:bg-orange-600 disabled:opacity-50 transition whitespace-nowrap text-sm"
        >
          {status === "loading" ? "Đang gửi..." : "Tham gia Waitlist"}
        </button>
      </form>
      {status === "error" && (
        <p className="text-red-500 text-sm text-center mt-3">{message}</p>
      )}
    </div>
  );
}
