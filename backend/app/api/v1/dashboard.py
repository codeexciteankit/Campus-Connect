from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.db.models import User, Event, Registration
from app.core.security import get_current_user

router = APIRouter()

@router.get("/stats/me")
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_events = db.query(Event).count()
    
    user_registrations = db.query(Registration).filter(Registration.user_id == current_user.id).all()
    registered_events_count = len(user_registrations)
    
    # Upcoming events registered by user
    upcoming_events = 0
    now = datetime.utcnow()
    for reg in user_registrations:
        event = db.query(Event).filter(Event.id == reg.event_id).first()
        if event and event.start_time > now:
            upcoming_events += 1

    return {
        "total_events": total_events,
        "registered_events": registered_events_count,
        "upcoming_events": upcoming_events
    }
