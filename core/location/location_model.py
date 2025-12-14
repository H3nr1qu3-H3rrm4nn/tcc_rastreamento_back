from datetime import datetime
from typing import Optional

from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from core.abstract.abstract_model import AbstractModel
from utils.base import Base


class Location(Base, AbstractModel):
    __tablename__ = "location"
    vehicle_id = Column(Integer, ForeignKey("vehicle.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    velocity = Column(Float, nullable=False)  # km/h
    timestamp = Column(DateTime, default=datetime.now, nullable=False)

    vehicle = relationship("Vehicle", back_populates="locations")

class LocationCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vehicle_id: int
    latitude: float
    longitude: float
    velocity: Optional[float] = Field(default=None, alias="velocity")
    timestamp: Optional[datetime] = None

    @field_validator("velocity", mode="before")
    @classmethod
    def accept_velocidade_alias(cls, value, info):
        if value is not None:
            return value
        data = getattr(info, "data", None)
        if isinstance(data, dict):
            alias_value = data.get("velocidade")
            if alias_value is not None:
                return alias_value
        return value

    @field_validator("timestamp", mode="before")
    @classmethod
    def normalize_timestamp(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            parsed = value
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=ZoneInfo("UTC"))
        local_dt = parsed.astimezone(ZoneInfo("America/Sao_Paulo"))
        return local_dt.replace(tzinfo=None)


class LocationUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    latitude: Optional[float] = None
    longitude: Optional[float] = None
    velocity: Optional[float] = Field(default=None, alias="velocity")
    timestamp: Optional[datetime] = None

    @field_validator("velocity", mode="before")
    @classmethod
    def accept_velocidade_alias(cls, value, info):
        if value is not None:
            return value
        data = getattr(info, "data", None)
        if isinstance(data, dict):
            alias_value = data.get("velocidade")
            if alias_value is not None:
                return alias_value
        return value

    @field_validator("timestamp", mode="before")
    @classmethod
    def normalize_timestamp(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            parsed = value
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=ZoneInfo("UTC"))
        local_dt = parsed.astimezone(ZoneInfo("America/Sao_Paulo"))
        return local_dt.replace(tzinfo=None)
