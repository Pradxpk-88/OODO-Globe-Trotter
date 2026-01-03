from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Trip, Stop
from ..schemas.stop import StopCreate, StopOut
from ..utils.auth import get_current_user

router = APIRouter(
    prefix="/stops",
    tags=["Stops"]
)


@router.post("/", response_model=StopOut)
def create_stop(
    stop: StopCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trip = db.query(Trip).filter(
        Trip.id == stop.trip_id,
        Trip.user_id == current_user.id
    ).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    new_stop = Stop(
        name=stop.name,
        latitude=stop.latitude,
        longitude=stop.longitude,
        order=stop.order,
        trip_id=stop.trip_id,
    )

    db.add(new_stop)
    db.commit()
    db.refresh(new_stop)
    return new_stop


@router.get("/trip/{trip_id}", response_model=list[StopOut])
def get_stops_for_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    stops = db.query(Stop).filter(
        Stop.trip_id == trip_id
    ).order_by(Stop.order).all()

    return stops


@router.delete("/{stop_id}")
def delete_stop(
    stop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stop = (
        db.query(Stop)
        .join(Trip)
        .filter(
            Stop.id == stop_id,
            Trip.user_id == current_user.id
        )
        .first()
    )

    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")

    db.delete(stop)
    db.commit()
    return {"message": "Stop deleted successfully"}
