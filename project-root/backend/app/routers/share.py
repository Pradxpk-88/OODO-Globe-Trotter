from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.trip import Trip

router = APIRouter()

@router.get("/{token}")
def get_shared_trip(token: str, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.share_token == token).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    # Return read-only data (trip, stops, activities)
    return trip