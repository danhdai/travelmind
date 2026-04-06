from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime, timezone
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=True)
    name = Column(String, nullable=True)
    travel_dna = Column(JSON, nullable=True)
    saved_itineraries = Column(JSON, default=list)
    referral_code = Column(String, unique=True, nullable=True, index=True)
    referred_by = Column(String, nullable=True)
    referral_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
