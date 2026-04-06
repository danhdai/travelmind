import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import waitlist, profile, reviews, itinerary, payment, concierge, admin, auth, group

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TravelMind API",
    description="AI Travel Designer - Backend API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(waitlist.router)
app.include_router(profile.router)
app.include_router(reviews.router)
app.include_router(itinerary.router)
app.include_router(payment.router)
app.include_router(concierge.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(group.router)


@app.get("/")
def root():
    return {"message": "TravelMind API v0.1.0", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/search")
def search(q: str, db=None):
    """Global search across places, reviews, destinations."""
    from fastapi import HTTPException
    if not q or len(q) > 255:
        raise HTTPException(status_code=400, detail="Query khong hop le")

    from database import SessionLocal
    from models.review import Review
    from sqlalchemy import func, or_

    db = SessionLocal()
    try:
        query = f"%{q.lower()}%"
        # Search reviews
        review_results = (
            db.query(
                Review.place_id,
                Review.place_name,
                func.count(Review.id).label("matches"),
                func.avg(Review.rating).label("avg_rating"),
            )
            .filter(
                or_(
                    func.lower(Review.place_name).like(query),
                    func.lower(Review.text).like(query),
                )
            )
            .group_by(Review.place_id, Review.place_name)
            .limit(10)
            .all()
        )

        places = [
            {
                "type": "place",
                "id": r.place_id,
                "name": r.place_name,
                "matches": r.matches,
                "rating": round(float(r.avg_rating or 0), 1),
                "url": f"/reviews/{r.place_id}",
            }
            for r in review_results
        ]

        # Search destinations
        destinations = []
        dest_map = {
            "quang binh": {"name": "Quảng Bình", "slug": "quang-binh", "emoji": "🏔"},
            "da lat": {"name": "Đà Lạt", "slug": "da-lat", "emoji": "🌸"},
            "phu quoc": {"name": "Phú Quốc", "slug": "phu-quoc", "emoji": "🏝"},
            "hoi an": {"name": "Hội An", "slug": "hoi-an", "emoji": "🏮"},
        }
        for key, info in dest_map.items():
            if q.lower() in key or q.lower() in info["name"].lower():
                destinations.append({
                    "type": "destination",
                    "name": info["name"],
                    "emoji": info["emoji"],
                    "url": f"/destination/{info['slug']}",
                })

        return {"query": q, "destinations": destinations, "places": places, "total": len(destinations) + len(places)}
    finally:
        db.close()
