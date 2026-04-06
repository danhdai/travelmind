"use client";

import Link from "next/link";
import { useState } from "react";
import { useAuth } from "@/lib/auth";
import SearchBar from "@/components/SearchBar";

const navLinks = [
  { href: "/explore", label: "Khám phá" },
  { href: "/reviews", label: "Reviews" },
  { href: "/itinerary", label: "Tạo lịch trình" },
  { href: "/chat", label: "AI Concierge" },
  { href: "/pricing", label: "Bảng giá" },
];

export default function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const { user, logout } = useAuth();

  return (
    <>
    <header className="border-b border-gray-100 bg-white/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 font-bold text-xl">
          <span className="text-2xl">✈</span>
          <span className="text-sky-600">TravelMind</span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden lg:flex items-center gap-5 text-sm font-medium text-gray-600">
          {navLinks.map((link) => (
            <Link key={link.href} href={link.href} className="hover:text-sky-600 transition">
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setSearchOpen(true)}
            className="p-2 text-gray-400 hover:text-sky-600 transition"
            title="Tìm kiếm (Ctrl+K)"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
          {user ? (
            <div className="hidden sm:flex items-center gap-2">
              <div className="w-8 h-8 bg-sky-100 text-sky-600 rounded-full flex items-center justify-center text-sm font-bold">
                {(user.name || user.email)[0].toUpperCase()}
              </div>
              <span className="text-sm text-gray-700 max-w-[100px] truncate">{user.name || user.email.split("@")[0]}</span>
              <button onClick={logout} className="text-xs text-gray-400 hover:text-red-500 transition">
                Thoát
              </button>
            </div>
          ) : (
            <Link
              href="/login"
              className="hidden sm:inline-block bg-sky-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-sky-700 transition"
            >
              Đăng nhập
            </Link>
          )}

          {/* Mobile hamburger */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="lg:hidden p-2 text-gray-600 hover:text-gray-900"
          >
            {mobileOpen ? (
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="lg:hidden border-t border-gray-100 bg-white px-4 py-4 space-y-1">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMobileOpen(false)}
              className="block px-3 py-2.5 rounded-lg text-gray-700 hover:bg-sky-50 hover:text-sky-600 font-medium transition"
            >
              {link.label}
            </Link>
          ))}
          {user ? (
            <div className="flex items-center justify-between px-3 py-2.5 border-t border-gray-100 mt-2 pt-3">
              <span className="text-sm text-gray-600">{user.name || user.email}</span>
              <button onClick={() => { logout(); setMobileOpen(false); }} className="text-sm text-red-500">Thoát</button>
            </div>
          ) : (
            <Link
              href="/login"
              onClick={() => setMobileOpen(false)}
              className="block mt-2 text-center bg-sky-600 text-white px-4 py-3 rounded-lg font-medium"
            >
              Đăng nhập / Đăng ký
            </Link>
          )}
        </div>
      )}
    </header>

    {/* Search modal */}
    {searchOpen && <SearchBar onClose={() => setSearchOpen(false)} />}
    </>
  );
}
