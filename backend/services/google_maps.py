from __future__ import annotations

from typing import Dict, List, Optional

import httpx
import os
from models.review import Review
from sqlalchemy.orm import Session

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

QUANG_BINH_PLACES = [
    {"name": "Phong Nha Cave", "query": "Phong Nha Cave Quang Binh"},
    {"name": "Paradise Cave (Dong Thien Duong)", "query": "Paradise Cave Quang Binh"},
    {"name": "Dark Cave (Hang Toi)", "query": "Dark Cave Quang Binh"},
    {"name": "Suoi Mooc (Mooc Spring)", "query": "Suoi Mooc Quang Binh"},
    {"name": "Nuoc Mooc Eco Trail", "query": "Nuoc Mooc Eco Trail"},
    {"name": "Son Doong Cave", "query": "Son Doong Cave"},
    {"name": "Nhat Le Beach", "query": "Nhat Le Beach Dong Hoi"},
    {"name": "Bai Dinh Beach", "query": "Bai Dinh Beach Quang Binh"},
    {"name": "Phong Nha Botanical Garden", "query": "Phong Nha Botanical Garden"},
    {"name": "Chay River - Dark Cave", "query": "Chay River Dark Cave Quang Binh"},
]


async def search_place(query: str) -> Optional[Dict]:
    if not GOOGLE_MAPS_API_KEY:
        return None

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://maps.googleapis.com/maps/api/place/textsearch/json",
            params={"query": query, "key": GOOGLE_MAPS_API_KEY, "language": "vi"},
        )
        data = resp.json()
        if data.get("results"):
            return data["results"][0]
    return None


async def get_place_reviews(place_id: str) -> List[Dict]:
    if not GOOGLE_MAPS_API_KEY:
        return []

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://maps.googleapis.com/maps/api/place/details/json",
            params={
                "place_id": place_id,
                "key": GOOGLE_MAPS_API_KEY,
                "fields": "name,rating,reviews,photos,formatted_address",
                "language": "vi",
            },
        )
        data = resp.json()
        result = data.get("result", {})
        return result.get("reviews", [])


def simple_sentiment(text: str) -> float:
    """Basic Vietnamese sentiment: count positive/negative keywords."""
    positive = ["dep", "tuyet", "hay", "ngon", "sach", "tot", "thich", "tuyet voi", "xinh", "ok", "oke", "recommend", "nen di", "rat dep", "dinh"]
    negative = ["xau", "ban", "dat", "chan", "te", "dở", "khong nen", "that vong", "kem", "toi te"]

    text_lower = text.lower()
    pos = sum(1 for w in positive if w in text_lower)
    neg = sum(1 for w in negative if w in text_lower)

    if pos + neg == 0:
        return 0.5
    return pos / (pos + neg)


async def crawl_quang_binh_reviews(db: Session):
    """Crawl Google Maps reviews for Quang Binh destinations."""
    results = []
    for place_info in QUANG_BINH_PLACES:
        place = await search_place(place_info["query"])
        if not place:
            continue

        place_id = place["place_id"]
        place_name = place.get("name", place_info["name"])

        reviews = await get_place_reviews(place_id)
        for rev in reviews:
            existing = db.query(Review).filter(
                Review.place_id == place_id,
                Review.author_name == rev.get("author_name"),
            ).first()
            if existing:
                continue

            text = rev.get("text", "")
            sentiment = simple_sentiment(text) if text else 0.5
            trust = min(1.0, (rev.get("rating", 3) / 5) * 0.4 + sentiment * 0.3 + (0.3 if len(text) > 50 else 0.1))

            review_record = Review(
                place_id=place_id,
                place_name=place_name,
                source="google_maps",
                author_name=rev.get("author_name"),
                rating=rev.get("rating"),
                text=text,
                sentiment_score=sentiment,
                trust_score=trust,
                photos=[p.get("photo_reference") for p in rev.get("photos", [])],
                raw_data=rev,
            )
            db.add(review_record)
            results.append(place_name)

    db.commit()
    return results
