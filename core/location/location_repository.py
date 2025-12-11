from datetime import datetime

from sqlalchemy import select
from core.abstract.abstract_repository import AbstractRepository
from core.location.location_model import Location
from core.vehicle.vehicle_model import Vehicle
from utils.contexts import conditional_session
from sqlalchemy.ext.asyncio import AsyncSession


class LocationRepository(AbstractRepository):
    
    async def list_by_vehicle_id(self, vehicle_id: int, session: AsyncSession = None):
        """
        Repositório para listar todas as localizações de um veículo específico.
        """
        async with conditional_session(session) as db:
            try:

                query = select(Location).where(Location.vehicle_id == vehicle_id)
                result = await db.execute(query)
                data = result.scalars().all()

                return data
            
            except Exception as e:
                raise e
            
    async def last_by_vehicle_id(self, vehicle_id: int, session: AsyncSession = None):
        """
        Repositório para obter a última localização de um veículo específico.
        """
        async with conditional_session(session) as db:
            try:

                query = select(Location).where(Location.vehicle_id == vehicle_id).order_by(Location.timestamp.desc()).limit(1)
                result = await db.execute(query)
                data = result.scalars().first()

                return data
            
            except Exception as e:
                raise e
            
    async def list_by_vehicle_and_range(self, vehicle_id: int, start_timestamp: datetime, end_timestamp: datetime, session: AsyncSession = None):
        """
        Repositório para listar todas as localizações de um veículo específico em um intervalo de tempo.
        """
        async with conditional_session(session) as db:
            try:

                query = select(Location).where(
                    Location.vehicle_id == vehicle_id,
                    Location.timestamp >= start_timestamp,
                    Location.timestamp <= end_timestamp
                )
                result = await db.execute(query)
                data = result.scalars().all()

                return data
            
            except Exception as e:
                raise e