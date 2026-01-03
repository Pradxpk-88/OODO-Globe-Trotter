from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.trip import Trip
from ..models.user import User
from ..utils.auth import get_current_user
from ..utils.validation import TripCreate

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/")
def get_trips(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Trip).filter(Trip.user_id == user.id).all()

@router.post("/")
def create_trip(trip_data: TripCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trip = Trip(**trip_data.dict(), user_id=user.id)
    db.add(trip)
    db.commit()
    return trip

# Add update/delete endpoints similarly