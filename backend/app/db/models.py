import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password = Column(
        String,
        nullable=False,
    )

    full_name = Column(
        String,
        nullable=False,
    )

    role = Column(
        String,
        default="student",
    )

    roll_number = Column(String)
    department = Column(String)
    year = Column(Integer)

    phone_number = Column(String)
    profile_picture = Column(String)

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    events_organized = relationship(
        "Event",
        back_populates="organizer",
    )

    registrations = relationship(
        "Registration",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Event(Base):
    __tablename__ = "events"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    category = Column(
        String,
        nullable=False,
    )

    venue = Column(
        String,
        nullable=False,
        default="TBA",
    )

    organizer_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False,
    )

    start_time = Column(
        DateTime,
        nullable=False,
    )

    end_time = Column(
        DateTime,
        nullable=False,
    )

    capacity = Column(
        Integer,
        default=100,
        nullable=False,
    )

    status = Column(
        String,
        default="draft",
    )

    banner_url = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    organizer = relationship(
        "User",
        back_populates="events_organized",
    )

    registrations = relationship(
        "Registration",
        back_populates="event",
        cascade="all, delete-orphan",
    )


class Registration(Base):
    __tablename__ = "registrations"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "event_id",
            name="unique_user_event_registration",
        ),
    )

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True,
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False,
    )

    event_id = Column(
        String,
        ForeignKey("events.id"),
        nullable=False,
    )

    status = Column(
        String,
        default="confirmed",
    )

    qr_code_data = Column(
        String,
        unique=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    user = relationship(
        "User",
        back_populates="registrations",
    )

    event = relationship(
        "Event",
        back_populates="registrations",
    )