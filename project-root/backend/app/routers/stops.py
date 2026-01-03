from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Stop, Trip
from ..utils.auth import get_current_user
from ..utils.validation import StopCreate, StopUpdate, StopResponse

router = APIRouter(prefix="/stops", tags=["stops"])

@router.post("/", response_model=StopResponse, status_code=status.HTTP_201_CREATED)
def create_stop(stop: StopCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new stop for a trip"""
    # Verify trip exists and user owns it
    trip = db.query(Trip).filter(Trip.id == stop.trip_id, Trip.user_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Create new stop
    db_stop = Stop(**stop.dict())
    db.add(db_stop)
    db.commit()
    db.refresh(db_stop)
    return db_stop

@router.get("/trip/{trip_id}", response_model=List[StopResponse])
def get_trip_stops(trip_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all stops for a specific trip"""
    # Verify trip exists and user owns it
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    stops = db.query(Stop).filter(Stop.trip_id == trip_id).order_by(Stop.order).all()
    return stops

@router.get("/{stop_id}", response_model=StopResponse)
def get_stop(stop_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get a specific stop by ID"""
    stop = db.query(Stop).filter(Stop.id == stop_id).first()
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    
    # Verify user owns the trip
    trip = db.query(Trip).filter(Trip.id == stop.trip_id, Trip.user_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=403, detail="Not authorized to access this stop")
    
    return stop

@router.put("/{stop_id}", response_model=StopResponse)
def update_stop(stop_id: int, stop_update: StopUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update a stop"""
    stop = db.query(Stop).filter(Stop.id == stop_id).first()
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    
    # Verify user owns the trip
    trip = db.query(Trip).filter(Trip.id == stop.trip_id, Trip.user_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=403, detail="Not authorized to update this stop")
    
    # Update stop fields
    for field, value in stop_update.dict(exclude_unset=True).items():
        setattr(stop, field, value)
    
    db.commit()
    db.refresh(stop)
    return stop

@router.delete("/{stop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stop(stop_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete a stop"""
    stop = db.query(Stop).filter(Stop.id == stop_id).first()
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    
    # Verify user owns the trip
    trip = db.query(Trip).filter(Trip.id == stop.trip_id, Trip.user_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=403, detail="Not authorized to delete this stop")
    
    db.delete(stop)
    db.commit()
    return None