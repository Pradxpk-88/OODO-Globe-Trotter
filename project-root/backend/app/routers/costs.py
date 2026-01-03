from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.cost import Cost
from ..models.trip import Trip
from ..utils.auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/{trip_id}")
def add_cost(trip_id: int, cost_data: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    cost = Cost(**cost_data, trip_id=trip_id)
    db.add(cost)
    db.commit()
    # Auto-calculate total: sum all costs for the trip
    total = db.query(Cost).filter(Cost.trip_id == trip_id).with_entities(Cost.amount).all()
    return {"cost": cost, "total": sum([c[0] for c in total])}