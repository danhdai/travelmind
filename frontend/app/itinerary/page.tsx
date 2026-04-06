"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { generateItinerary } from "@/lib/api";
import WeatherWidget from "@/components/WeatherWidget";

export default function ItineraryPage() {
  const router = useRouter();
  const [destination, setDestination] = useState("Quang Binh");
  const [numDays, setNumDays] = useState(3);
  const [budget, setBudget] = useState(3000000);
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [error, setError] = useState("");

  async function handleGenerate(e: React.FormEvent) {
    e.preventDefault();
    setStatus("loading");
    try {
      const result = await generateItinerary({
        destination,
        num_days: numDays,
        budget,
      });
      router.push(`/itinerary/${result.id}`);
    } catch (err) {
      setStatus("error");
      setError(err instanceof Error ? err.message : "Co loi xay ra");
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      <div className="text-center mb-10">
        <div className="text-4xl mb-3">🗺</div>
        <h1 className="text-3xl font-bold mb-2">Tao lich trinh AI</h1>
        <p className="text-gray-500">
          AI se thiet ke lich trinh day-by-day rieng cho ban
        </p>
      </div>

      <form onSubmit={handleGenerate} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Diem den
          </label>
          <select
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-sky-500 focus:ring-2 focus:ring-sky-200 outline-none"
          >
            <option value="Quang Binh">Quảng Bình</option>
            <option value="Da Lat">Đà Lạt</option>
            <option value="Phu Quoc">Phú Quốc</option>
            <option value="Hoi An">Hội An</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            So ngay
          </label>
          <div className="flex gap-3">
            {[2, 3, 4, 5].map((d) => (
              <button
                key={d}
                type="button"
                onClick={() => setNumDays(d)}
                className={`flex-1 py-3 rounded-lg border-2 font-medium transition ${
                  numDays === d
                    ? "border-sky-500 bg-sky-50 text-sky-700"
                    : "border-gray-200 hover:border-gray-300"
                }`}
              >
                {d} ngay
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Ngan sach tong (VND)
          </label>
          <input
            type="number"
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value))}
            step={500000}
            min={1000000}
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-sky-500 focus:ring-2 focus:ring-sky-200 outline-none"
          />
          <p className="text-xs text-gray-400 mt-1">
            ~{Math.round(budget / numDays).toLocaleString()} VND/ngay
          </p>
        </div>

        {/* Weather */}
        <WeatherWidget destination={destination} />

        {error && (
          <p className="text-red-500 text-sm">{error}</p>
        )}

        <button
          type="submit"
          disabled={status === "loading"}
          className="w-full py-4 bg-sky-600 text-white font-semibold rounded-xl hover:bg-sky-700 disabled:opacity-50 transition text-lg"
        >
          {status === "loading" ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              AI dang thiet ke lich trinh...
            </span>
          ) : (
            "Tao lich trinh"
          )}
        </button>
      </form>
    </div>
  );
}
