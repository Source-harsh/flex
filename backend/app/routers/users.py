from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = auth.get_password_hash(user_in.password)
    user = models.User(name=user_in.name, email=user_in.email, phone=user_in.phone, hashed_password=hashed, role=user_in.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"user_id": user.id}, expires_delta=60 * 60 * 24)
    return {"token": token, "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}
