from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.itinerary import Itinerary
from models.review import Review
from services.ai_itinerary import generate_itinerary
from services.nlp_vietnamese import generate_review_summary

router = APIRouter(prefix="/api/itinerary", tags=["itinerary"])


class ItineraryRequest(BaseModel):
    destination: str
    num_days: int
    budget: Optional[float] = None
    travel_dna: Optional[Dict] = None
    email: Optional[str] = None


class ItineraryResponse(BaseModel):
    id: int
    destination: str
    num_days: int
    budget: Optional[float]
    itinerary_data: Dict


@router.post("/generate", response_model=ItineraryResponse)
async def create_itinerary(req: ItineraryRequest, db: Session = Depends(get_db)):
    itinerary_data = await generate_itinerary(
        destination=req.destination,
        num_days=req.num_days,
        budget=req.budget,
        travel_dna=req.travel_dna,
    )

    # Attach real review summaries to itinerary
    itinerary_data["review_summaries"] = _get_review_summaries(db)

    record = Itinerary(
        user_email=req.email,
        destination=req.destination,
        num_days=req.num_days,
        budget=req.budget,
        travel_dna=req.travel_dna,
        itinerary_data=itinerary_data,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return ItineraryResponse(
        id=record.id,
        destination=record.destination,
        num_days=record.num_days,
        budget=record.budget,
        itinerary_data=record.itinerary_data,
    )


def _get_review_summaries(db: Session) -> List:
    """Get review summaries for all places in DB."""
    from sqlalchemy import func
    places = (
        db.query(Review.place_id, Review.place_name)
        .group_by(Review.place_id, Review.place_name)
        .all()
    )
    summaries = []
    for place_id, place_name in places:
        reviews = db.query(Review).filter(Review.place_id == place_id).all()
        if not reviews:
            continue
        review_dicts = [{"text": r.text or "", "rating": r.rating or 3} for r in reviews]
        summary = generate_review_summary(review_dicts)
        summary["place_id"] = place_id
        summary["place_name"] = place_name
        summaries.append(summary)
    return summaries


@router.get("/{itinerary_id}", response_model=ItineraryResponse)
def get_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    record = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
    if not record:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return ItineraryResponse(
        id=record.id,
        destination=record.destination,
        num_days=record.num_days,
        budget=record.budget,
        itinerary_data=record.itinerary_data,
    )
