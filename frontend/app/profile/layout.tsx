import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Travel DNA Profile - TravelMind",
  description: "Tạo Travel DNA - AI hiểu phong cách du lịch của bạn để thiết kế lịch trình hoàn hảo.",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
