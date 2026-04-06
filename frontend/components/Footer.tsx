import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-gray-100 bg-gray-50 py-10 mt-auto">
      <div className="max-w-6xl mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2 font-bold text-lg mb-3">
              <span>✈</span>
              <span className="text-sky-600">TravelMind</span>
            </div>
            <p className="text-sm text-gray-500">
              AI Travel Designer — Research review thật, thiết kế lịch trình theo đúng con người bạn.
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-sm mb-3">Sản phẩm</h4>
            <div className="space-y-2 text-sm text-gray-500">
              <Link href="/reviews" className="block hover:text-sky-600">Review Explorer</Link>
              <Link href="/profile" className="block hover:text-sky-600">Travel DNA</Link>
              <Link href="/itinerary" className="block hover:text-sky-600">Tạo lịch trình</Link>
              <Link href="/pricing" className="block hover:text-sky-600">Bảng giá</Link>
              <Link href="/faq" className="block hover:text-sky-600">FAQ</Link>
            </div>
          </div>
          <div>
            <h4 className="font-semibold text-sm mb-3">Điểm đến</h4>
            <div className="space-y-2 text-sm text-gray-500">
              <span className="block">Quảng Bình (MVP)</span>
              <span className="block text-gray-300">Đà Lạt (sắp ra mắt)</span>
              <span className="block text-gray-300">Phú Quốc (sắp ra mắt)</span>
              <span className="block text-gray-300">Hội An (sắp ra mắt)</span>
            </div>
          </div>
          <div>
            <h4 className="font-semibold text-sm mb-3">Liên hệ</h4>
            <div className="space-y-2 text-sm text-gray-500">
              <p>hello@travelmind.vn</p>
              <p>BNG Agency</p>
            </div>
          </div>
        </div>
        <div className="border-t border-gray-200 pt-6 text-center text-xs text-gray-400">
          © 2026 TravelMind. MVP — Quảng Bình Pilot. Powered by AI.
        </div>
      </div>
    </footer>
  );
}
