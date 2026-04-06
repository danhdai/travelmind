import { Metadata } from "next";

export const metadata: Metadata = {
  title: "So sánh điểm đến - TravelMind",
  description: "So sánh Quảng Bình, Đà Lạt, Phú Quốc, Hội An. Chi phí, thời điểm, highlights, ẩm thực.",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
