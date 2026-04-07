"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { API_BASE } from "@/lib/config";

interface Place {
  place_id: string;
  place_name: string;
  review_count: number;
  avg_rating: number;
  avg_trust_score: number;
}

const DESTINATIONS = [
  { slug: "quang-binh", name: "Quảng Bình", emoji: "🏔", tag: "Hang động kỳ vĩ", gradient: "from-emerald-500 to-teal-600", budget: "2-4tr", time: "T4-8" },
  { slug: "da-lat", name: "Đà Lạt", emoji: "🌸", tag: "Ngàn hoa, coffee", gradient: "from-pink-500 to-purple-600", budget: "2-3.5tr", time: "Quanh năm" },
  { slug: "phu-quoc", name: "Phú Quốc", emoji: "🏝", tag: "Đảo ngọc, biển xanh", gradient: "from-cyan-500 to-blue-600", budget: "4-7tr", time: "T11-4" },
  { slug: "hoi-an", name: "Hội An", emoji: "🏮", tag: "Phố cổ, đèn lồng", gradient: "from-amber-500 to-orange-600", budget: "2-3tr", time: "T2-5" },
];

const DEST_PLACES: Record<string, string[]> = {
  "quang-binh": ["phong_nha_cave", "paradise_cave", "dark_cave", "suoi_mooc", "nhat_le_beach", "son_doong"],
  "da-lat": ["dalat_langbiang", "dalat_valley_of_love", "dalat_coffee", "dalat_xq_village"],
  "phu-quoc": ["phuquoc_sao_beach", "phuquoc_vinwonders", "phuquoc_night_market"],
  "hoi-an": ["hoian_old_town", "hoian_an_bang_beach", "hoian_food"],
};

export default function ExplorePage() {
  const [places, setPlaces] = useState<Place[]>([]);
  const [filter, setFilter] = useState<string>("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/reviews/places/all`)
      .then((r) => r.json())
      .then((d) => setPlaces(d.places || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filteredPlaces = filter === "all"
    ? places
    : places.filter((p) => DEST_PLACES[filter]?.includes(p.place_id));

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold mb-2">Khám phá Việt Nam</h1>
        <p className="text-gray-500">4 điểm đến, 16 địa điểm, 53+ reviews thật</p>
      </div>

      {/* Destination cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
        {DESTINATIONS.map((d) => (
          <Link
            key={d.slug}
            href={`/destination/${d.slug}`}
            className={`bg-gradient-to-br ${d.gradient} text-white rounded-2xl p-5 hover:scale-105 transition-transform`}
          >
            <div className="text-3xl mb-2">{d.emoji}</div>
            <h3 className="font-bold">{d.name}</h3>
            <p className="text-xs opacity-80 mt-1">{d.tag}</p>
            <div className="flex gap-2 mt-3 text-[10px] opacity-70">
              <span>💰 {d.budget}</span>
              <span>📅 {d.time}</span>
            </div>
          </Link>
        ))}
      </div>

      {/* Filter */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        <button
          onClick={() => setFilter("all")}
          className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition ${
            filter === "all" ? "bg-sky-600 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"
          }`}
        >
          Tất cả ({places.length})
        </button>
        {DESTINATIONS.map((d) => (
          <button
            key={d.slug}
            onClick={() => setFilter(d.slug)}
            className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition ${
              filter === d.slug ? "bg-sky-600 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {d.emoji} {d.name}
          </button>
        ))}
      </div>

      {/* Places grid */}
      {loading ? (
        <div className="grid md:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="animate-pulse bg-gray-100 h-32 rounded-xl" />
          ))}
        </div>
      ) : (
        <div className="grid md:grid-cols-3 gap-4">
          {filteredPlaces.map((place) => (
            <Link
              key={place.place_id}
              href={`/reviews/${place.place_id}`}
              className="group p-5 border border-gray-100 rounded-xl hover:border-sky-200 hover:shadow-lg transition-all"
            >
              <h3 className="font-semibold group-hover:text-sky-600 transition">{place.place_name}</h3>
              <div className="flex items-center gap-3 mt-2 text-sm">
                <span className="text-yellow-500">★ {place.avg_rating}</span>
                <span className="text-gray-400">{place.review_count} reviews</span>
                <span className={`flex items-center gap-1 ${
                  place.avg_trust_score >= 0.8 ? "text-green-600" : "text-yellow-600"
                }`}>
                  <span className={`w-2 h-2 rounded-full ${
                    place.avg_trust_score >= 0.8 ? "bg-green-500" : "bg-yellow-500"
                  }`} />
                  Trust {Math.round(place.avg_trust_score * 100)}%
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* CTA */}
      <div className="mt-12 text-center">
        <p className="text-gray-500 mb-4">Tìm thấy điểm đến ưng ý?</p>
        <div className="flex gap-3 justify-center">
          <Link href="/itinerary" className="px-6 py-3 bg-sky-600 text-white rounded-xl font-medium hover:bg-sky-700 transition">
            Tạo lịch trình AI
          </Link>
          <Link href="/compare" className="px-6 py-3 border border-gray-200 rounded-xl font-medium hover:bg-gray-50 transition">
            So sánh điểm đến
          </Link>
        </div>
      </div>
    </div>
  );
}
