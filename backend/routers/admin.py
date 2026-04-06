from __future__ import annotations

from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.waitlist import Waitlist
from models.user import User
from models.itinerary import Itinerary
from models.review import Review
from services.auth import get_current_user

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Simple admin check - in production, use role-based auth
ADMIN_EMAILS = {"admin@travelmind.vn", "demo@travelmind.vn"}


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    waitlist_count = db.query(Waitlist).count()
    user_count = db.query(User).count()
    itinerary_count = db.query(Itinerary).count()
    review_count = db.query(Review).count()
    place_count = db.query(Review.place_id).distinct().count()

    # Recent waitlist
    recent_waitlist = (
        db.query(Waitlist)
        .order_by(Waitlist.created_at.desc())
        .limit(10)
        .all()
    )

    # Top destinations
    top_destinations = (
        db.query(
            Itinerary.destination,
            func.count(Itinerary.id).label("count"),
        )
        .group_by(Itinerary.destination)
        .order_by(func.count(Itinerary.id).desc())
        .limit(5)
        .all()
    )

    # Review stats per place
    review_stats = (
        db.query(
            Review.place_name,
            func.count(Review.id).label("count"),
            func.avg(Review.rating).label("avg_rating"),
            func.avg(Review.trust_score).label("avg_trust"),
        )
        .group_by(Review.place_name)
        .order_by(func.count(Review.id).desc())
        .all()
    )

    return {
        "overview": {
            "waitlist": waitlist_count,
            "users": user_count,
            "itineraries": itinerary_count,
            "reviews": review_count,
            "places": place_count,
        },
        "recent_waitlist": [
            {"email": w.email, "name": w.name, "date": str(w.created_at)} for w in recent_waitlist
        ],
        "top_destinations": [
            {"destination": d.destination, "count": d.count} for d in top_destinations
        ],
        "review_stats": [
            {
                "place": r.place_name,
                "reviews": r.count,
                "avg_rating": round(float(r.avg_rating or 0), 1),
                "avg_trust": round(float(r.avg_trust or 0), 2),
            }
            for r in review_stats
        ],
    }
