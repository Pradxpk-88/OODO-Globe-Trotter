from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, trips, stops, activities, costs, share

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(trips.router, prefix="/trips", tags=["trips"])
app.include_router(stops.router, prefix="/stops", tags=["stops"])
app.include_router(activities.router, prefix="/activities", tags=["activities"])
app.include_router(costs.router, prefix="/costs", tags=["costs"])
app.include_router(share.router, prefix="/share", tags=["share"])