from core.abstract.abstract_repository import AbstractRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.vehicle.vehicle_model import Vehicle
from utils.contexts import conditional_session


class VehicleRepository(AbstractRepository):
    
    async def list_by_user_id(self, user_id: int, session: AsyncSession = None):
        """
        Repositório para listar todos os veículos de um usuário específico.
        """
        async with conditional_session(session) as db:
            try:

                query = select(Vehicle).where(Vehicle.user_id == user_id)
                result = await db.execute(query)
                data = result.scalars().all()

                return data
            
            except Exception as e:
                raise e
            
    async def list_online(self, session: AsyncSession = None):
        """
        Repositório para listar todos os veículos online.
        """
        async with conditional_session(session) as db:
            try:

                query = select(Vehicle).where(Vehicle.is_online == True)
                result = await db.execute(query)
                data = result.scalars().all()

                return data
            
            except Exception as e:
                raise e
            
    async def count_all(self, session: AsyncSession = None):
        """
        Repositório para contar todos os veículos.
        """
        async with conditional_session(session) as db:
            try:

                query = select(Vehicle)
                result = await db.execute(query)
                data = result.scalars().all()

                return len(data)
            
            except Exception as e:
                raise e

    async def set_online_status(self, vehicle_id: int, is_online: bool, session: AsyncSession = None):
        """Atualiza o status online/offline de um veículo específico."""
        async with conditional_session(session) as db:
            try:
                query = select(Vehicle).where(Vehicle.id == vehicle_id)
                result = await db.execute(query)
                vehicle = result.scalars().first()

                if not vehicle:
                    return None

                vehicle.is_online = is_online
                await db.flush()

                return vehicle
            except Exception as e:
                await db.rollback()
                raise e