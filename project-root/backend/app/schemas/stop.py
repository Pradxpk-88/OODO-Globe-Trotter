from pydantic import BaseModel


class StopCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    order: int
    trip_id: int


class StopOut(StopCreate):
    id: int

    class Config:
        from_attributes = True

