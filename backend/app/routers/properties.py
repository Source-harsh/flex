from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas, auth
from typing import List

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("/", response_model=List[schemas.PropertyOut])
def list_properties(db: Session = Depends(get_db)):
    props = db.query(models.Property).all()
    return props


@router.get("/my-properties", response_model=List[schemas.PropertyOut])
def my_properties(current_user=Depends(auth.get_current_user), db: Session = Depends(get_db)):
    props = db.query(models.Property).filter(models.Property.provider_id == current_user.id).all()
    return props


@router.post("/", response_model=schemas.PropertyOut)
def create_property(p: schemas.PropertyCreate, current_user=Depends(auth.get_current_user), db: Session = Depends(get_db)):
    prop = models.Property(
        title=p.title,
        description=p.description,
        address=p.address,
        latitude=p.latitude,
        longitude=p.longitude,
        price_per_hour=p.price_per_hour,
        dimensions=p.dimensions,
        provider_id=current_user.id,
    )
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop
