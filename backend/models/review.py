from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from datetime import datetime, timezone
from database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(String, nullable=False, index=True)
    place_name = Column(String, nullable=False)
    source = Column(String, default="google_maps")
    author_name = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    text = Column(Text, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    trust_score = Column(Float, nullable=True)
    photos = Column(JSON, nullable=True)
    raw_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
