from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.review import Review
from services.nlp_vietnamese import (
    analyze_sentiment,
    extract_entities,
    compute_trust_score,
    generate_review_summary,
)
from services.auth import get_current_user

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


class ReviewResponse(BaseModel):
    id: int
    place_id: str
    place_name: str
    source: str
    author_name: Optional[str]
    rating: Optional[float]
    text: Optional[str]
    sentiment_score: Optional[float]
    trust_score: Optional[float]


class ReviewSummary(BaseModel):
    place_id: str
    place_name: str
    total_reviews: int
    avg_rating: float
    avg_trust_score: float
    reviews: List[ReviewResponse]


@router.get("/{place_id}", response_model=ReviewSummary)
def get_reviews(place_id: str, limit: int = Query(20, le=100), db: Session = Depends(get_db)):
    reviews = (
        db.query(Review)
        .filter(Review.place_id == place_id)
        .order_by(Review.trust_score.desc().nullslast())
        .limit(limit)
        .all()
    )

    if not reviews:
        return ReviewSummary(
            place_id=place_id,
            place_name="Unknown",
            total_reviews=0,
            avg_rating=0,
            avg_trust_score=0,
            reviews=[]
        )

    total = db.query(Review).filter(Review.place_id == place_id).count()
    ratings = [r.rating for r in reviews if r.rating is not None]
    trust_scores = [r.trust_score for r in reviews if r.trust_score is not None]

    return ReviewSummary(
        place_id=place_id,
        place_name=reviews[0].place_name,
        total_reviews=total,
        avg_rating=sum(ratings) / len(ratings) if ratings else 0,
        avg_trust_score=sum(trust_scores) / len(trust_scores) if trust_scores else 0,
        reviews=[
            ReviewResponse(
                id=r.id,
                place_id=r.place_id,
                place_name=r.place_name,
                source=r.source,
                author_name=r.author_name,
                rating=r.rating,
                text=r.text,
                sentiment_score=r.sentiment_score,
                trust_score=r.trust_score,
            )
            for r in reviews
        ]
    )


@router.get("/{place_id}/summary")
def get_review_summary(place_id: str, db: Session = Depends(get_db)):
    """Get AI-generated review summary for a place."""
    reviews = db.query(Review).filter(Review.place_id == place_id).all()
    if not reviews:
        return {"place_id": place_id, "summary": "Chua co review"}

    review_dicts = [
        {"text": r.text or "", "rating": r.rating or 3, "author": r.author_name}
        for r in reviews
    ]
    summary = generate_review_summary(review_dicts)
    summary["place_id"] = place_id
    summary["place_name"] = reviews[0].place_name
    return summary


@router.get("/{place_id}/analyze")
def analyze_reviews(place_id: str, db: Session = Depends(get_db)):
    """Deep NLP analysis of reviews for a place."""
    reviews = db.query(Review).filter(Review.place_id == place_id).all()
    if not reviews:
        return {"place_id": place_id, "analysis": []}

    all_ratings = [r.rating for r in reviews if r.rating]
    analyzed = []
    for r in reviews:
        text = r.text or ""
        trust = compute_trust_score(
            text=text,
            rating=r.rating or 3,
            author_name=r.author_name or "",
            other_ratings=all_ratings,
        )
        entities = extract_entities(text)
        analyzed.append({
            "id": r.id,
            "author": r.author_name,
            "text": text,
            "rating": r.rating,
            "trust_score": trust["trust_score"],
            "trust_breakdown": trust["breakdown"],
            "sentiment": trust["sentiment"],
            "fake_check": trust["fake_check"],
            "entities": entities,
        })

    return {
        "place_id": place_id,
        "place_name": reviews[0].place_name,
        "total_analyzed": len(analyzed),
        "analysis": analyzed,
    }


@router.get("/places/all")
def list_places(db: Session = Depends(get_db)):
    """List all places with review counts."""
    from sqlalchemy import func
    results = (
        db.query(
            Review.place_id,
            Review.place_name,
            func.count(Review.id).label("review_count"),
            func.avg(Review.rating).label("avg_rating"),
            func.avg(Review.trust_score).label("avg_trust"),
        )
        .group_by(Review.place_id, Review.place_name)
        .all()
    )
    return {
        "places": [
            {
                "place_id": r.place_id,
                "place_name": r.place_name,
                "review_count": r.review_count,
                "avg_rating": round(float(r.avg_rating or 0), 1),
                "avg_trust_score": round(float(r.avg_trust or 0), 2),
            }
            for r in results
        ]
    }


class SubmitReviewRequest(BaseModel):
    place_id: str
    place_name: str
    rating: float
    text: str


@router.post("/submit")
def submit_review(
    req: SubmitReviewRequest,
    db: Session = Depends(get_db),
    email: Optional[str] = Depends(get_current_user),
):
    """Submit a user review. NLP auto-analyzes sentiment + trust."""
    from fastapi import HTTPException
    if not req.text or len(req.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Review phai co it nhat 10 ky tu")
    if len(req.text) > 5000:
        raise HTTPException(status_code=400, detail="Review qua dai (max 5000 ky tu)")
    if not 1 <= req.rating <= 5:
        raise HTTPException(status_code=400, detail="Rating phai tu 1-5")
    if not req.place_id or len(req.place_id) > 100:
        raise HTTPException(status_code=400, detail="Place ID khong hop le")

    author = email or "Anonymous"
    sentiment = analyze_sentiment(req.text)
    all_ratings = [r.rating for r in db.query(Review).filter(Review.place_id == req.place_id).all() if r.rating]
    trust = compute_trust_score(
        text=req.text,
        rating=req.rating,
        author_name=author,
        other_ratings=all_ratings,
    )

    review = Review(
        place_id=req.place_id,
        place_name=req.place_name,
        source="user_submit",
        author_name=author,
        rating=req.rating,
        text=req.text,
        sentiment_score=sentiment["score"],
        trust_score=trust["trust_score"],
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    return {
        "id": review.id,
        "message": "Review da duoc gui! Cam on ban.",
        "sentiment": sentiment,
        "trust_score": trust["trust_score"],
    }
