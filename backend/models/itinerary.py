from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime, timezone
from database import Base


class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=True, index=True)
    destination = Column(String, nullable=False)
    num_days = Column(Integer, nullable=False)
    budget = Column(Float, nullable=True)
    travel_dna = Column(JSON, nullable=True)
    itinerary_data = Column(JSON, nullable=False)
    tier = Column(String, default="free")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
