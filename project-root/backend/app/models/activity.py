from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..database import Base

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    stop_id = Column(Integer, ForeignKey("stops.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    cost = Column(Float, default=0.0)
    date = Column(DateTime, nullable=False)
    
    stop = relationship("Stop", back_populates="activities")