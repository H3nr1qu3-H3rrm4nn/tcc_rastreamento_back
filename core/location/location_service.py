from core.abstract.abstract_service import AbstractService
from core.location.location_repository import LocationRepository
from utils.contexts import conditional_session
from sqlalchemy.ext.asyncio import AsyncSession

from utils.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class LocationService(AbstractService):
    
    async def list_by_vehicle_id(self, vehicle_id: int, session: AsyncSession = None):
        """
        Serviço para listar todas as localizações de um veículo específico.
        """
        async with conditional_session(session) as db:
            try:

                response = await LocationRepository().list_by_vehicle_id(vehicle_id=vehicle_id, session=db)
                return response

            except Exception as e:
                logger.error(f"Erro ao listar localizações do veículo {vehicle_id}: {e}")
                raise e 
            
    async def last_by_vehicle_id(self, vehicle_id: int, session: AsyncSession = None):
        """
        Serviço para obter a última localização de um veículo específico.
        """
        async with conditional_session(session) as db:
            try:

                response = await LocationRepository().last_by_vehicle_id(vehicle_id=vehicle_id, session=db)
                return response

            except Exception as e:
                logger.error(f"Erro ao obter a última localização do veículo {vehicle_id}: {e}")
                raise e
            
    async def list_by_vehicle_and_range(self, vehicle_id: int, start_timestamp: str, end_timestamp: str, session: AsyncSession = None):
        """
        Serviço para listar todas as localizações de um veículo específico em um intervalo de tempo.
        """
        async with conditional_session(session) as db:
            try:

                data = await LocationRepository().list_by_vehicle_and_range(
                    vehicle_id=vehicle_id,
                    start_timestamp=start_timestamp,
                    end_timestamp=end_timestamp,
                    session=db
                )
                
                return data

            except Exception as e:
                logger.error(f"Erro ao listar localizações do veículo {vehicle_id} no intervalo {start_timestamp} - {end_timestamp}: {e}")
                raise e
            
        