from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.models import Base

from app.api.v1 import users
from app.api.v1 import events
from app.api.v1 import registrations
from app.api.v1 import admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CampusConnect API",
    version="1.0.0",
    description="Smart College Event Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.0.102:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"]
)

app.include_router(
    events.router,
    prefix="/api/v1/events",
    tags=["Events"]
)

from app.api.v1 import dashboard
app.include_router(
    dashboard.router,
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)

app.include_router(
    registrations.router,
    prefix="/api/v1",
    tags=["Registrations"]
)

app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["Admin"]
)


@app.get("/")
def root():
    return {
        "message": "CampusConnect API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }