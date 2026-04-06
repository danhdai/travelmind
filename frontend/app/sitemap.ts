import { MetadataRoute } from "next";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://travelmind.vn";

export default function sitemap(): MetadataRoute.Sitemap {
  const staticPages = [
    { url: `${BASE_URL}/`, priority: 1.0 },
    { url: `${BASE_URL}/reviews`, priority: 0.9 },
    { url: `${BASE_URL}/compare`, priority: 0.8 },
    { url: `${BASE_URL}/profile`, priority: 0.7 },
    { url: `${BASE_URL}/itinerary`, priority: 0.9 },
    { url: `${BASE_URL}/chat`, priority: 0.8 },
    { url: `${BASE_URL}/pricing`, priority: 0.7 },
    { url: `${BASE_URL}/faq`, priority: 0.6 },
    { url: `${BASE_URL}/login`, priority: 0.5 },
  ];

  const destinations = ["quang-binh", "da-lat", "phu-quoc", "hoi-an"].map(
    (slug) => ({
      url: `${BASE_URL}/destination/${slug}`,
      priority: 0.9,
    })
  );

  const places = [
    "phong_nha_cave", "paradise_cave", "dark_cave", "suoi_mooc",
    "nhat_le_beach", "son_doong", "dalat_langbiang", "dalat_coffee",
    "phuquoc_sao_beach", "phuquoc_vinwonders", "hoian_old_town", "hoian_food",
  ].map((id) => ({
    url: `${BASE_URL}/reviews/${id}`,
    priority: 0.7,
  }));

  return [...staticPages, ...destinations, ...places].map((page) => ({
    ...page,
    lastModified: new Date(),
    changeFrequency: "weekly" as const,
  }));
}
