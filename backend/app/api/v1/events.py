from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.db.database import get_db
from app.db.models import Event, Registration, User
from app.schemas import EventCreate, EventResponse
from app.core.security import get_current_user

router = APIRouter()


# =====================================
# CREATE EVENT
# =====================================

@router.post("/", response_model=EventResponse)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    db_event = Event(
        title=event.title,
        description=event.description,
        category=event.category,
        venue=event.venue,
        organizer_id=event.organizer_id,
        start_time=event.start_time,
        end_time=event.end_time,
        capacity=event.capacity,
        banner_url=event.banner_url,
        status="Upcoming"
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event


# =====================================
# GET ALL EVENTS
# =====================================

@router.get("/", response_model=list[EventResponse])
def get_events(
    db: Session = Depends(get_db)
):
    return db.query(Event).all()


# =====================================
# GET SINGLE EVENT
# =====================================

@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: str,
    db: Session = Depends(get_db)
):
    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


# =====================================
# REGISTER FOR EVENT
# =====================================

@router.post("/{event_id}/register")
def register_for_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    existing_registration = (
        db.query(Registration)
        .filter(
            Registration.user_id == current_user.id,
            Registration.event_id == event_id
        )
        .first()
    )

    if existing_registration:
        raise HTTPException(
            status_code=400,
            detail="Already registered for this event"
        )

    registration = Registration(
        user_id=current_user.id,
        event_id=event_id,
        qr_code_data=str(uuid.uuid4()),
        status="confirmed"
    )

    db.add(registration)
    db.commit()

    return {
        "message": "Successfully registered"
    }


# =====================================
# UPDATE EVENT
# =====================================

@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: str,
    event: EventCreate,
    db: Session = Depends(get_db)
):
    db_event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not db_event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    db_event.title = event.title
    db_event.description = event.description
    db_event.category = event.category
    db_event.venue = event.venue
    db_event.start_time = event.start_time
    db_event.end_time = event.end_time
    db_event.capacity = event.capacity
    db_event.banner_url = event.banner_url

    db.commit()
    db.refresh(db_event)

    return db_event


# =====================================
# DELETE EVENT
# =====================================

@router.delete("/{event_id}")
def delete_event(
    event_id: str,
    db: Session = Depends(get_db)
):
    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    db.delete(event)
    db.commit()

    return {
        "message": "Event deleted successfully"
    }
