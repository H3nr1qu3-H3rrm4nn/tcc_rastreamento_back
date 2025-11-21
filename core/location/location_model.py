from typing import Optional
from core.abstract.abstract_model import AbstractModel
from utils.base import Base
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime


class Location(Base, AbstractModel):
    __tablename__ = "location"
    vehicle_id = Column(Integer, ForeignKey("vehicle.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    velocity = Column(Float, nullable=False)  # km/h
    timestamp = Column(DateTime, default=datetime.now, nullable=False)

    vehicle = relationship("Vehicle", back_populates="locations")

class LocationCreate(BaseModel):
    vehicle_id : int
    latitude: Optional[float]
    longitude: Optional[float]
    localizacao: Optional[str]
    velocidade: Optional[float]
    status: Optional[str]
    timestamp: Optional[datetime]

class LocationUpdate(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
    localizacao: Optional[str]
    velocidade: Optional[float]
    status: Optional[str]
    timestamp: Optional[datetime]
