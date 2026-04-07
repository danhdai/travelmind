const PRODUCTION_API = "https://travelmind-r36f.onrender.com";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== "undefined" && window.location.hostname !== "localhost"
    ? PRODUCTION_API
    : "http://localhost:8000");
