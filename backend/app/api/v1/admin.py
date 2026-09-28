from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import User, Event, Registration
from app.core.dependencies import require_admin

router = APIRouter()


@router.get("/stats")
def get_admin_stats(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()
    total_events = db.query(Event).count()
    total_registrations = db.query(Registration).count()
    
    return {
        "total_users": total_users,
        "total_events": total_events,
        "total_registrations": total_registrations
    }


@router.get("/users")
def get_all_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return db.query(User).all()


@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted"}


@router.get("/events")
def get_all_events_admin(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return db.query(Event).all()


@router.delete("/events/{event_id}")
def delete_event_admin(
    event_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    
    return {"message": "Event deleted"}


@router.get("/registrations")
def get_all_registrations(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return db.query(Registration).all()


@router.delete("/registrations/{registration_id}")
def delete_registration(
    registration_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    registration = db.query(Registration).filter(Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    db.delete(registration)
    db.commit()
    
    return {"message": "Registration deleted"}
