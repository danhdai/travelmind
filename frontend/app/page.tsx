import WaitlistForm from "@/components/WaitlistForm";
import Link from "next/link";

const features = [
  {
    icon: "🔍",
    title: "Review Aggregator",
    desc: "Tổng hợp review thật từ Facebook, TikTok, Google Maps. AI phân tích sentiment, tính Trust Score cho mỗi địa điểm.",
  },
  {
    icon: "🧬",
    title: "Travel DNA Profile",
    desc: "AI hiểu bạn trước khi lên kế hoạch — persona, budget, energy level, sở thích ẩm thực, deal breakers.",
  },
  {
    icon: "🗺",
    title: "AI Itinerary Designer",
    desc: "Lịch trình day-by-day thiết kế riêng cho bạn, tối ưu khoảng cách, thời gian, sở thích. Kèm review thật + budget breakdown.",
  },
  {
    icon: "💬",
    title: "AI Concierge 24/7",
    desc: "Trợ lý du lịch trong suốt chuyến đi — gợi ý nhà hàng, hoạt động indoor khi trời mưa, cập nhật real-time.",
  },
];

const stats = [
  { value: "27+", label: "Reviews thật" },
  { value: "6", label: "Địa điểm Quảng Bình" },
  { value: "89%", label: "Trust Score TB" },
  { value: "30s", label: "Tạo lịch trình" },
];

export default function Home() {
  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-sky-50 via-white to-orange-50">
        <div className="max-w-6xl mx-auto px-4 py-20 md:py-32 text-center">
          <div className="inline-block px-4 py-1.5 bg-sky-100 text-sky-700 rounded-full text-sm font-medium mb-6">
            MVP — Quảng Bình Pilot
          </div>
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 leading-tight mb-6">
            AI Travel Designer
            <br />
            <span className="text-sky-600">cá nhân hóa cho bạn</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto mb-10">
            Research review thật, thiết kế lịch trình theo đúng con người bạn.
            Không còn copy paste lịch trình generic — AI hiểu bạn và tạo chuyến
            đi hoàn hảo.
          </p>
          <WaitlistForm />
          <p className="text-sm text-gray-400 mt-4">
            Miễn phí trải nghiệm. Không cần thẻ tín dụng.
          </p>
        </div>
      </section>

      {/* Stats */}
      <section className="py-8 border-b border-gray-100">
        <div className="max-w-4xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            {stats.map((s) => (
              <div key={s.label}>
                <div className="text-2xl md:text-3xl font-bold text-sky-600">{s.value}</div>
                <div className="text-sm text-gray-500 mt-1">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-4">
            Tại sao chọn TravelMind?
          </h2>
          <p className="text-gray-500 text-center mb-12 max-w-xl mx-auto">
            Không chỉ là app lên lịch trình — đây là designer du lịch AI hiểu bạn
          </p>
          <div className="grid md:grid-cols-2 gap-8">
            {features.map((f) => (
              <div
                key={f.title}
                className="group p-6 rounded-2xl border border-gray-100 hover:border-sky-200 hover:shadow-lg transition-all duration-300"
              >
                <div className="text-3xl mb-3 group-hover:scale-110 transition-transform duration-300">{f.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
                <p className="text-gray-600 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            Cách hoạt động
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { step: "1", title: "Tạo Travel DNA", desc: "Trả lời 6 câu hỏi để AI hiểu phong cách du lịch của bạn", link: "/profile" },
              { step: "2", title: "Chọn điểm đến", desc: "Chọn địa điểm, số ngày, ngân sách. AI tạo lịch trình trong 30s", link: "/itinerary" },
              { step: "3", title: "Xem review thật", desc: "Mỗi địa điểm kèm review thật + Trust Score. Đặt dịch vụ ngay", link: "/reviews" },
            ].map((item) => (
              <Link href={item.link} key={item.step} className="text-center group">
                <div className="w-12 h-12 bg-sky-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4 group-hover:scale-110 transition-transform">
                  {item.step}
                </div>
                <h3 className="font-semibold mb-2">{item.title}</h3>
                <p className="text-sm text-gray-600">{item.desc}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Destinations */}
      <section className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-4">Điểm đến</h2>
          <p className="text-gray-500 text-center mb-12">Khám phá ngay — AI thiết kế lịch trình trong 30 giây</p>
          <div className="grid md:grid-cols-4 gap-4">
            {[
              { slug: "quang-binh", name: "Quảng Bình", emoji: "🏔", tag: "Hang động", gradient: "from-emerald-500 to-teal-600" },
              { slug: "da-lat", name: "Đà Lạt", emoji: "🌸", tag: "Ngàn hoa", gradient: "from-pink-500 to-purple-600" },
              { slug: "phu-quoc", name: "Phú Quốc", emoji: "🏝", tag: "Biển đảo", gradient: "from-cyan-500 to-blue-600" },
              { slug: "hoi-an", name: "Hội An", emoji: "🏮", tag: "Phố cổ", gradient: "from-amber-500 to-orange-600" },
            ].map((d) => (
              <Link key={d.slug} href={`/destination/${d.slug}`}
                className={`group bg-gradient-to-br ${d.gradient} text-white rounded-2xl p-6 text-center hover:scale-105 transition-transform`}>
                <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">{d.emoji}</div>
                <h3 className="text-lg font-bold">{d.name}</h3>
                <p className="text-sm opacity-80">{d.tag}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-sky-600 text-white text-center">
        <div className="max-w-3xl mx-auto px-4">
          <h2 className="text-3xl font-bold mb-4">
            Sẵn sàng khám phá Việt Nam?
          </h2>
          <p className="text-sky-100 text-lg mb-8">
            Thử ngay AI Travel Designer — lịch trình Quảng Bình 3 ngày chỉ trong 30 giây
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/itinerary"
              className="inline-block bg-white text-sky-600 font-semibold px-8 py-4 rounded-xl hover:bg-sky-50 transition text-lg"
            >
              Tạo lịch trình ngay
            </a>
            <a
              href="/reviews"
              className="inline-block border-2 border-white text-white font-semibold px-8 py-4 rounded-xl hover:bg-white/10 transition text-lg"
            >
              Xem reviews
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
