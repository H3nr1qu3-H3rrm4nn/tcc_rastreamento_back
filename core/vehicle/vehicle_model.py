from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from core.abstract.abstract_model import AbstractModel
from utils.base import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Vehicle(Base, AbstractModel):
    __tablename__ = "veiculos"

    plate = Column(String(10), unique=True, nullable=False)
    type = Column(String(50), nullable=False)  # Caminhão, Van, Carro, Moto, etc
    is_online = Column(Boolean, default=False, nullable=False)  # Online, Offline
    last_location = Column(String(255), nullable=True)  # Município/Cidade
    driver_name = Column(String(255), nullable=True)  # Nome do motorista
    current_velocity = Column(Float, default=0)  # km/h
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 

    # Relacionamentos
    user = relationship("User", back_populates="vehicles")
    locations = relationship("Location", back_populates="vehicle", cascade="all, delete-orphan")

class VehicleCreate(BaseModel):
    name: str
    plate: str
    type: str
    is_online: Optional[bool]
    last_location: Optional[str]
    user_id: int

class VehicleUpdate(BaseModel):
    name: Optional[str]
    plate: Optional[str]
    type: Optional[str]
    is_online: Optional[bool]
    last_location: Optional[str]
    current_velocity: Optional[float]