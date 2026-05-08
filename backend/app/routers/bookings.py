from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas, auth
from typing import List
from datetime import datetime

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=schemas.BookingOut)
def create_booking(b: schemas.BookingCreate, current_user=Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # check overlap
    start = b.start_time
    end = b.end_time
    overlaps = db.query(models.Booking).filter(
        models.Booking.property_id == b.property_id,
        models.Booking.status != "cancelled",
        ~((models.Booking.end_time <= start) | (models.Booking.start_time >= end)),
    ).first()
    if overlaps:
        raise HTTPException(status_code=409, detail="Time slot already booked")
    booking = models.Booking(property_id=b.property_id, renter_id=current_user.id, start_time=b.start_time, end_time=b.end_time, total_price=b.total_price, status="booked")
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/my-bookings", response_model=List[schemas.BookingOut])
def my_bookings(current_user=Depends(auth.get_current_user), db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).filter(models.Booking.renter_id == current_user.id).all()
    return bookings


@router.get("/provider-bookings", response_model=List[schemas.BookingOut])
def provider_bookings(current_user=Depends(auth.get_current_user), db: Session = Depends(get_db)):
    bookings = (
        db.query(models.Booking)
        .join(models.Property, models.Booking.property_id == models.Property.id)
        .filter(models.Property.provider_id == current_user.id)
        .all()
    )
    return bookings
