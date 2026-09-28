import uuid
import qrcode
import io
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from app.db.database import get_db
from app.db.models import Registration, Event, User
from app.core.security import get_current_user

router = APIRouter()


@router.post("/events/{event_id}/register")
def register_for_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if already registered
    existing_registration = (
        db.query(Registration)
        .filter(
            Registration.user_id == current_user.id,
            Registration.event_id == event_id
        )
        .first()
    )
    
    if existing_registration:
        raise HTTPException(status_code=400, detail="Already registered for this event")
    
    # Check capacity
    registration_count = (
        db.query(Registration)
        .filter(Registration.event_id == event_id)
        .count()
    )
    
    if registration_count >= event.capacity:
        raise HTTPException(status_code=400, detail="Event is full")
    
    # Generate unique QR code data
    qr_code_data = f"REG-{uuid.uuid4().hex[:16].upper()}"
    
    # Create registration
    registration = Registration(
        user_id=current_user.id,
        event_id=event_id,
        status="confirmed",
        qr_code_data=qr_code_data
    )
    
    db.add(registration)
    db.commit()
    db.refresh(registration)
    
    return {
        "message": "Successfully registered for event",
        "registration_id": registration.id,
        "qr_code_data": qr_code_data
    }


@router.get("/registrations/{registration_id}/qr")
def get_qr_code(
    registration_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    registration = (
        db.query(Registration)
        .filter(Registration.id == registration_id)
        .first()
    )
    
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    # Only the registered user can view their QR code
    if registration.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(registration.qr_code_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return StreamingResponse(
        img_buffer,
        media_type="image/png",
        headers={
            "Content-Disposition": f"attachment; filename=qr_{registration_id}.png"
        }
    )


@router.get("/registrations/{registration_id}/certificate")
def generate_certificate(
    registration_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    registration = (
        db.query(Registration)
        .filter(Registration.id == registration_id)
        .first()
    )
    
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    # Only the registered user can view their certificate
    if registration.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get event and user details
    event = db.query(Event).filter(Event.id == registration.event_id).first()
    user = db.query(User).filter(User.id == registration.user_id).first()
    
    if not event or not user:
        raise HTTPException(status_code=404, detail="Event or user not found")
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("Certificate of Participation", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Content
    content = f"""
    This is to certify that
    
    <b>{user.full_name}</b>
    
    has successfully participated in
    
    <b>{event.title}</b>
    
    held on {event.start_time.strftime('%B %d, %Y')}
    
    at {event.venue}
    
    Certificate ID: {registration.qr_code_data}
    """
    
    para = Paragraph(content, styles['Normal'])
    story.append(para)
    story.append(Spacer(1, 24))
    
    # Footer
    footer = Paragraph("CampusConnect - Smart College Event Management System", styles['Normal'])
    story.append(footer)
    
    doc.build(story)
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=certificate_{registration_id}.pdf"
        }
    )
