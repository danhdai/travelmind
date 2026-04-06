"use client";

import { useParams } from "next/navigation";
import Link from "next/link";
import ReviewSummary from "@/components/ReviewSummary";
import WeatherWidget from "@/components/WeatherWidget";

interface DestInfo {
  name: string;
  apiName: string;
  emoji: string;
  tagline: string;
  description: string;
  gradient: string;
  bestTime: string;
  budget: string;
  duration: string;
  places: Array<{ id: string; name: string; icon: string; desc: string }>;
  foodTips: string[];
  transportTips: string[];
}

const DESTINATIONS: Record<string, DestInfo> = {
  "quang-binh": {
    name: "Quảng Bình",
    apiName: "Quang Binh",
    emoji: "🏔",
    tagline: "Vương quốc hang động",
    description: "Quảng Bình sở hữu hệ thống hang động kỳ vĩ nhất thế giới, bao gồm Sơn Đoòng — hang động lớn nhất hành tinh. Từ Phong Nha đến Dark Cave, mỗi trải nghiệm đều khó quên.",
    gradient: "from-emerald-600 to-teal-700",
    bestTime: "Tháng 4 - 8",
    budget: "2-4 triệu/người",
    duration: "3-4 ngày",
    places: [
      { id: "phong_nha_cave", name: "Động Phong Nha", icon: "🏔", desc: "Di sản UNESCO, đi thuyền vào động" },
      { id: "paradise_cave", name: "Động Thiên Đường", icon: "✨", desc: "31km thạch nhũ hùng vĩ" },
      { id: "dark_cave", name: "Hang Tối (Dark Cave)", icon: "🦇", desc: "Zipline + tắm bùn, highlight #1" },
      { id: "suoi_mooc", name: "Suối Moọc", icon: "💧", desc: "Nước trong ngọc bích, kayak" },
      { id: "nhat_le_beach", name: "Biển Nhật Lệ", icon: "🏖", desc: "Cát mịn, hải sản tươi, giá rẻ" },
      { id: "son_doong", name: "Hang Sơn Đoòng", icon: "🌍", desc: "Hang lớn nhất thế giới, 70tr/tour" },
    ],
    foodTips: ["Bánh lọc, bánh nậm — ăn sáng kinh điển", "Cháo canh hải sản", "Ram cuốn rau sống", "Hải sản tươi Nhật Lệ — giá 1/3 thành phố"],
    transportTips: ["Bay: Vietnam Airlines/Vietjet → Đồng Hới (VDH)", "Thuê xe máy: 120-150k/ngày", "Đồng Hới → Phong Nha: 45km, 1h xe máy"],
  },
  "da-lat": {
    name: "Đà Lạt",
    apiName: "Da Lat",
    emoji: "🌸",
    tagline: "Thành phố ngàn hoa",
    description: "Đà Lạt mê hoặc du khách bằng khí hậu mát mẻ quanh năm, coffee culture đỉnh cao, và những đồi thông bất tận. Thiên đường cho couple và tín đồ cafe.",
    gradient: "from-pink-500 to-purple-600",
    bestTime: "Quanh năm (đẹp nhất 11-3)",
    budget: "2-3.5 triệu/người",
    duration: "2-3 ngày",
    places: [
      { id: "dalat_langbiang", name: "Núi LangBiang", icon: "⛰", desc: "2167m, view 360° toàn Đà Lạt" },
      { id: "dalat_valley_of_love", name: "Thung Lũng Tình Yêu", icon: "💕", desc: "Vườn hoa, hồ, check-in" },
      { id: "dalat_coffee", name: "Coffee Đà Lạt", icon: "☕", desc: "An Cafe, La Viet, specialty" },
      { id: "dalat_xq_village", name: "Làng Lụa XQ", icon: "🎨", desc: "Tranh thêu tay, vườn hoa" },
    ],
    foodTips: ["Bánh căn Cô Duyên", "Lẩu bò Đà Lạt", "Bánh tráng nướng chợ đêm", "Sữa đậu nành nóng"],
    transportTips: ["Bay: → Liên Khương, taxi 30 phút vào TP", "Thuê xe máy: 100-120k/ngày", "Xe bus từ TPHCM: ~7h"],
  },
  "phu-quoc": {
    name: "Phú Quốc",
    apiName: "Phu Quoc",
    emoji: "🏝",
    tagline: "Đảo ngọc phương Nam",
    description: "Phú Quốc là thiên đường biển đảo với bãi cát trắng, nước trong vắt, hoàng hôn mê hồn và hải sản tươi sống. Resort đẳng cấp và VinWonders cho mọi đối tượng.",
    gradient: "from-cyan-500 to-blue-600",
    bestTime: "Tháng 11 - 4",
    budget: "4-7 triệu/người",
    duration: "3-5 ngày",
    places: [
      { id: "phuquoc_sao_beach", name: "Bãi Sao", icon: "🏖", desc: "Bãi biển đẹp nhất đảo" },
      { id: "phuquoc_vinwonders", name: "VinWonders", icon: "🎢", desc: "Cáp treo 8km vượt biển" },
      { id: "phuquoc_night_market", name: "Chợ đêm", icon: "🦞", desc: "Hải sản tươi sống, nhum biển" },
    ],
    foodTips: ["Bún quậy — đặc sản chỉ có ở PQ", "Nhum biển nướng mỡ hành", "Cua hoàng đế", "Nước mắm Phú Quốc — mua làm quà"],
    transportTips: ["Bay: Nhiều hãng → Phú Quốc (PQC)", "Thuê xe máy: 150-200k/ngày", "Grab có hoạt động"],
  },
  "hoi-an": {
    name: "Hội An",
    apiName: "Hoi An",
    emoji: "🏮",
    tagline: "Phố cổ đèn lồng",
    description: "Hội An là viên ngọc di sản UNESCO với phố cổ mê hoặc, đèn lồng lung linh, ẩm thực đỉnh cao và biển An Bàng tuyệt đẹp. Nơi thời gian ngừng trôi.",
    gradient: "from-amber-500 to-orange-600",
    bestTime: "Tháng 2 - 5",
    budget: "2-3 triệu/người",
    duration: "2-3 ngày",
    places: [
      { id: "hoian_old_town", name: "Phố cổ Hội An", icon: "🏮", desc: "UNESCO, đèn lồng, Chùa Cầu" },
      { id: "hoian_an_bang_beach", name: "Biển An Bàng", icon: "🏄", desc: "Beach bar, lướt sóng" },
      { id: "hoian_food", name: "Ẩm thực Hội An", icon: "🍜", desc: "Cao lầu, bánh mì Phượng" },
    ],
    foodTips: ["Cao lầu — chỉ có ở Hội An", "Bánh mì Phượng (CNN voted)", "Mì Quảng Ông Hai", "Cơm gà Bà Buội", "White Rose, bánh bao bánh vạc"],
    transportTips: ["Bay: → Đà Nẵng, taxi/bus 30 phút", "Thuê xe đạp: 20-30k/ngày", "Phố cổ cấm xe máy 8h-23h"],
  },
};

export default function DestinationPage() {
  const params = useParams();
  const slug = params.slug as string;
  const dest = DESTINATIONS[slug];

  if (!dest) {
    return (
      <div className="text-center py-32">
        <h1 className="text-2xl font-bold mb-2">Không tìm thấy điểm đến</h1>
        <Link href="/" className="text-sky-600 hover:underline">Về trang chủ</Link>
      </div>
    );
  }

  return (
    <div>
      {/* Hero */}
      <section className={`bg-gradient-to-br ${dest.gradient} text-white py-16 md:py-24`}>
        <div className="max-w-4xl mx-auto px-4 text-center">
          <div className="text-5xl mb-4">{dest.emoji}</div>
          <h1 className="text-4xl md:text-5xl font-bold mb-3">{dest.name}</h1>
          <p className="text-xl opacity-90 mb-2">{dest.tagline}</p>
          <p className="opacity-80 max-w-2xl mx-auto mb-8">{dest.description}</p>
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            <div className="bg-white/20 rounded-lg px-4 py-2 text-sm">📅 {dest.bestTime}</div>
            <div className="bg-white/20 rounded-lg px-4 py-2 text-sm">💰 {dest.budget}</div>
            <div className="bg-white/20 rounded-lg px-4 py-2 text-sm">🕐 {dest.duration}</div>
          </div>
          <Link
            href="/itinerary"
            className="inline-block bg-white text-gray-900 font-semibold px-8 py-4 rounded-xl hover:bg-gray-100 transition text-lg"
          >
            Tạo lịch trình {dest.name}
          </Link>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 py-12 space-y-12">
        {/* Weather */}
        <WeatherWidget destination={dest.apiName} />

        {/* Places */}
        <section>
          <h2 className="text-2xl font-bold mb-6">Địa điểm nổi bật</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {dest.places.map((p) => (
              <div key={p.id} className="border border-gray-100 rounded-xl overflow-hidden">
                <div className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xl">{p.icon}</span>
                    <h3 className="font-semibold">{p.name}</h3>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">{p.desc}</p>
                  <ReviewSummary placeId={p.id} />
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Food + Transport */}
        <div className="grid md:grid-cols-2 gap-8">
          <section className="bg-orange-50 rounded-2xl p-6">
            <h2 className="text-xl font-bold mb-4">🍜 Ẩm thực</h2>
            <ul className="space-y-2">
              {dest.foodTips.map((tip) => (
                <li key={tip} className="text-sm text-gray-700 flex items-start gap-2">
                  <span className="text-orange-500 mt-0.5">•</span> {tip}
                </li>
              ))}
            </ul>
          </section>
          <section className="bg-sky-50 rounded-2xl p-6">
            <h2 className="text-xl font-bold mb-4">🚗 Di chuyển</h2>
            <ul className="space-y-2">
              {dest.transportTips.map((tip) => (
                <li key={tip} className="text-sm text-gray-700 flex items-start gap-2">
                  <span className="text-sky-500 mt-0.5">•</span> {tip}
                </li>
              ))}
            </ul>
          </section>
        </div>

        {/* CTA */}
        <div className="text-center py-8">
          <Link
            href="/itinerary"
            className={`inline-block bg-gradient-to-r ${dest.gradient} text-white font-semibold px-8 py-4 rounded-xl hover:opacity-90 transition text-lg`}
          >
            Tạo lịch trình {dest.name} ngay →
          </Link>
        </div>
      </div>
    </div>
  );
}
