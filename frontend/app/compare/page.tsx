"use client";

import { useState } from "react";
import Link from "next/link";

interface Destination {
  id: string;
  name: string;
  emoji: string;
  bestTime: string;
  avgBudget: string;
  avgBudgetNum: number;
  highlights: string[];
  food: string[];
  rating: number;
  travelStyle: string[];
  duration: string;
  transport: string;
}

const DESTINATIONS: Destination[] = [
  {
    id: "quang-binh",
    name: "Quảng Bình",
    emoji: "🏔",
    bestTime: "Tháng 4-8",
    avgBudget: "2-4 triệu/người",
    avgBudgetNum: 3000000,
    highlights: ["Động Phong Nha (UNESCO)", "Dark Cave zipline + tắm bùn", "Động Thiên Đường 31km", "Suối Moọc", "Biển Nhật Lệ"],
    food: ["Bánh lọc, bánh nậm", "Cháo canh", "Ram cuốn", "Hải sản tươi"],
    rating: 4.7,
    travelStyle: ["Phượt thủ", "Mạo hiểm", "Thiên nhiên"],
    duration: "3-4 ngày",
    transport: "Bay → Đồng Hới (VDH), thuê xe máy",
  },
  {
    id: "da-lat",
    name: "Đà Lạt",
    emoji: "🌸",
    bestTime: "Quanh năm (tốt nhất 11-3)",
    avgBudget: "2-3.5 triệu/người",
    avgBudgetNum: 2500000,
    highlights: ["Núi LangBiang 2167m", "Vườn hoa thành phố", "Coffee culture", "Chợ đêm Đà Lạt", "Đường hầm Đất Sét"],
    food: ["Bánh căn", "Lẩu bò", "Bánh tráng nướng", "Sữa đậu nành", "Mứt Đà Lạt"],
    rating: 4.5,
    travelStyle: ["Nghỉ dưỡng", "Couple", "Coffee lover"],
    duration: "2-3 ngày",
    transport: "Bay → Liên Khương, thuê xe máy/ô tô",
  },
  {
    id: "phu-quoc",
    name: "Phú Quốc",
    emoji: "🏝",
    bestTime: "Tháng 11-4 (mùa khô)",
    avgBudget: "4-7 triệu/người",
    avgBudgetNum: 5000000,
    highlights: ["Bãi Sao cát trắng", "VinWonders", "Snorkeling An Thới", "Hoàng hôn Sunset Sanato", "Chợ đêm hải sản"],
    food: ["Bún quậy", "Nhum biển", "Cua hoàng đế", "Gỏi cá trích", "Nước mắm Phú Quốc"],
    rating: 4.6,
    travelStyle: ["Biển", "Resort", "Gia đình", "Couple"],
    duration: "3-5 ngày",
    transport: "Bay → Phú Quốc (PQC), thuê xe máy",
  },
  {
    id: "hoi-an",
    name: "Hội An",
    emoji: "🏮",
    bestTime: "Tháng 2-5",
    avgBudget: "2-3 triệu/người",
    avgBudgetNum: 2000000,
    highlights: ["Phố cổ UNESCO", "Đèn lồng sông Hoài", "Biển An Bàng", "Làng rau Trà Quế", "May đo trong 24h"],
    food: ["Cao lầu", "Bánh mì Phượng (CNN)", "Mì Quảng", "Cơm gà Bà Buội", "White Rose"],
    rating: 4.8,
    travelStyle: ["Văn hóa", "Ẩm thực", "Couple", "Photography"],
    duration: "2-3 ngày",
    transport: "Bay → Đà Nẵng, taxi/bus 30 phút",
  },
];

export default function ComparePage() {
  const [selected, setSelected] = useState<[string, string]>(["quang-binh", "hoi-an"]);

  const dest1 = DESTINATIONS.find((d) => d.id === selected[0])!;
  const dest2 = DESTINATIONS.find((d) => d.id === selected[1])!;

  function CompareRow({ label, val1, val2, highlight }: { label: string; val1: string; val2: string; highlight?: "lower" | "higher" }) {
    return (
      <div className="grid grid-cols-3 py-3 border-b border-gray-50">
        <div className="text-sm font-medium text-gray-500 text-center">{val1}</div>
        <div className="text-xs text-gray-400 text-center self-center">{label}</div>
        <div className="text-sm font-medium text-gray-500 text-center">{val2}</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="text-center mb-10">
        <div className="text-4xl mb-3">⚖</div>
        <h1 className="text-3xl font-bold mb-2">So sánh điểm đến</h1>
        <p className="text-gray-500">Chọn 2 điểm đến để so sánh</p>
      </div>

      {/* Selectors */}
      <div className="grid grid-cols-2 gap-4 mb-8">
        {[0, 1].map((idx) => (
          <select
            key={idx}
            value={selected[idx]}
            onChange={(e) => {
              const newSel = [...selected] as [string, string];
              newSel[idx] = e.target.value;
              setSelected(newSel);
            }}
            className="px-4 py-3 rounded-xl border border-gray-200 text-center font-medium focus:border-sky-500 outline-none"
          >
            {DESTINATIONS.map((d) => (
              <option key={d.id} value={d.id}>
                {d.emoji} {d.name}
              </option>
            ))}
          </select>
        ))}
      </div>

      {/* Comparison */}
      <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
        {/* Headers */}
        <div className="grid grid-cols-2 border-b border-gray-100">
          {[dest1, dest2].map((d) => (
            <div key={d.id} className="p-6 text-center">
              <div className="text-4xl mb-2">{d.emoji}</div>
              <h2 className="text-xl font-bold">{d.name}</h2>
              <div className="flex items-center justify-center gap-1 mt-1">
                <span className="text-yellow-500">★</span>
                <span className="font-semibold">{d.rating}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Rows */}
        <div className="px-4">
          <CompareRow label="Thời điểm" val1={dest1.bestTime} val2={dest2.bestTime} />
          <CompareRow label="Ngân sách" val1={dest1.avgBudget} val2={dest2.avgBudget} />
          <CompareRow label="Thời gian" val1={dest1.duration} val2={dest2.duration} />
          <CompareRow label="Di chuyển" val1={dest1.transport} val2={dest2.transport} />

          {/* Highlights */}
          <div className="grid grid-cols-2 py-4 border-b border-gray-50">
            {[dest1, dest2].map((d) => (
              <div key={d.id} className="px-2">
                <div className="text-xs text-gray-400 mb-2 text-center">Điểm nổi bật</div>
                <ul className="space-y-1">
                  {d.highlights.map((h) => (
                    <li key={h} className="text-xs text-gray-600 flex items-start gap-1">
                      <span className="text-green-500 mt-0.5">•</span> {h}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          {/* Food */}
          <div className="grid grid-cols-2 py-4 border-b border-gray-50">
            {[dest1, dest2].map((d) => (
              <div key={d.id} className="px-2">
                <div className="text-xs text-gray-400 mb-2 text-center">Ẩm thực</div>
                <div className="flex flex-wrap gap-1 justify-center">
                  {d.food.map((f) => (
                    <span key={f} className="text-[10px] px-2 py-0.5 bg-orange-50 text-orange-700 rounded-full">
                      {f}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Style */}
          <div className="grid grid-cols-2 py-4">
            {[dest1, dest2].map((d) => (
              <div key={d.id} className="px-2">
                <div className="text-xs text-gray-400 mb-2 text-center">Phong cách</div>
                <div className="flex flex-wrap gap-1 justify-center">
                  {d.travelStyle.map((s) => (
                    <span key={s} className="text-[10px] px-2 py-0.5 bg-sky-50 text-sky-700 rounded-full">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="grid grid-cols-2 border-t border-gray-100">
          {[dest1, dest2].map((d) => (
            <Link
              key={d.id}
              href={`/itinerary`}
              className="p-4 text-center text-sm font-medium text-sky-600 hover:bg-sky-50 transition"
            >
              Tạo lịch trình {d.name} →
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
