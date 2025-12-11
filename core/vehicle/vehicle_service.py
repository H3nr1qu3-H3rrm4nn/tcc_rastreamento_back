import logging
from core.abstract.abstract_service import AbstractService
import pytz
from sqlalchemy.ext.asyncio import AsyncSession
from core.vehicle.vehicle_repository import VehicleRepository
from utils.contexts import conditional_session

logger = logging.getLogger(__name__)
sp_tz = pytz.timezone("America/Sao_Paulo")

class VehicleService(AbstractService):

    async def list_by_user_id(self, user_id: int, session:AsyncSession=None):
        """
        Serviço para listar todos os veículos de um usuário específico.
        """
        async with conditional_session(session) as db:
            try:
                
                data = await VehicleRepository().list_by_user_id(user_id=user_id, session=db)
                
                logger.info(f"Veículos do usuário {user_id} listados com sucesso")
                
                return data

            except Exception as e:
                await db.rollback()
                logger.error(f"Erro ao listar veículos do usuário {user_id}: {e}")
                raise e
            
    async def list_online(self, session:AsyncSession=None):
        """
        Serviço para listar todos os veículos online.
        """
        async with conditional_session(session) as db:
            try:
                
                data = await VehicleRepository().list_online(session=db)
                
                logger.info("Veículos online listados com sucesso")
                
                return data

            except Exception as e:
                await db.rollback()
                logger.error(f"Erro ao listar veículos online: {e}")
                raise e
            
    async def stats(self, session:AsyncSession=None):
        """
        Serviço para obter estatísticas dos veículos.
        """
        async with conditional_session(session) as db:
            try:
                
                total_vehicles = await VehicleRepository().count_all(session=db)
                online_vehicles = len(await self.list_online(session=db))
                offline_vehicles = total_vehicles - online_vehicles
                
                stats = {
                    "total_vehicles": total_vehicles,
                    "online_vehicles": online_vehicles,
                    "offline_vehicles": offline_vehicles
                }
                
                logger.info("Estatísticas dos veículos obtidas com sucesso")
                
                return stats

            except Exception as e:
                await db.rollback()
                logger.error(f"Erro ao obter estatísticas dos veículos: {e}")
                raise e

    async def set_online_status(self, vehicle_id: int, is_online: bool, session: AsyncSession = None):
        """Atualiza o status online/offline de um veículo específico."""
        async with conditional_session(session) as db:
            try:
                vehicle = await VehicleRepository().set_online_status(
                    vehicle_id=vehicle_id,
                    is_online=is_online,
                    session=db,
                )

                if vehicle is None:
                    logger.warning(f"Veículo {vehicle_id} não encontrado para atualizar status online")
                    return None

                await db.commit()
                logger.info(f"Status do veículo {vehicle_id} atualizado para {'online' if is_online else 'offline'}")
                return vehicle
            except Exception as e:
                await db.rollback()
                logger.error(f"Erro ao atualizar status do veículo {vehicle_id}: {e}")
                raise e