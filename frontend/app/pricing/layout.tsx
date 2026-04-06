import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Bảng giá - TravelMind",
  description: "Bảng giá TravelMind: Free, Explorer (199k), Premium (599k), VIP. Tạo lịch trình AI cá nhân hóa.",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
