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
      setMessage("Dang ky thanh cong! Chung toi se lien he ban som.");
      setEmail("");
    } catch (err) {
      setStatus("error");
      setMessage(err instanceof Error ? err.message : "Co loi xay ra");
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
      <input
        type="email"
        required
        placeholder="Email cua ban..."
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="flex-1 px-4 py-3 rounded-lg border border-gray-300 focus:border-sky-500 focus:ring-2 focus:ring-sky-200 outline-none transition"
      />
      <button
        type="submit"
        disabled={status === "loading"}
        className="px-6 py-3 bg-orange-500 text-white font-semibold rounded-lg hover:bg-orange-600 disabled:opacity-50 transition whitespace-nowrap"
      >
        {status === "loading" ? "Dang gui..." : "Tham gia Waitlist"}
      </button>
      {status !== "idle" && (
        <p className={`text-sm mt-1 sm:mt-0 sm:self-center ${status === "success" ? "text-green-600" : "text-red-500"}`}>
          {message}
        </p>
      )}
    </form>
  );
}
