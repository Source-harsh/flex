from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .db import Base
import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="renter")
    properties = relationship("Property", back_populates="provider")
    bookings = relationship("Booking", back_populates="renter")


class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    price_per_hour = Column(Float, nullable=True)
    dimensions = Column(String, nullable=True)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = relationship("User", back_populates="properties")
    bookings = relationship("Booking", back_populates="property")


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    property = relationship("Property", back_populates="bookings")
    renter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    renter = relationship("User", back_populates="bookings")
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="booked")
