from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime, timezone
from database import Base
import uuid


class TripGroup(Base):
    __tablename__ = "trip_groups"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, default=lambda: uuid.uuid4().hex[:8], index=True)
    name = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    num_days = Column(Integer, default=3)
    owner_email = Column(String, nullable=False)
    members = Column(JSON, default=list)  # [{email, name, joined_at}]
    votes = Column(JSON, default=dict)   # {place_id: [email1, email2]}
    status = Column(String, default="planning")  # planning, voted, finalized
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
