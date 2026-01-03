from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Cost(Base):
    __tablename__ = "costs"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    category = Column(String, nullable=False)  # e.g., "stay", "transport", "activities"
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    
    trip = relationship("Trip", back_populates="costs")