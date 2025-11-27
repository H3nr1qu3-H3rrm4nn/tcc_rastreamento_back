import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from core.abstract.abstract_controller import AbstractController
from core.location.location_model import Location, LocationCreate, LocationUpdate
from core.location.location_service import LocationService
from core.token.token_service import TokenService
from utils.response_model import ResponseModel

logger = logging.getLogger(__name__)

location_service = LocationService()

class LocationController(AbstractController):
    def __init__(self):
        super().__init__(
            model=Location,
            model_create=LocationCreate,
            model_update=LocationUpdate,
            prefix="/location",
            service=location_service,
            tags=["Location"],
            token_service=TokenService(),
        )
        self.public_route = APIRouter(prefix="/location", tags=["Location"])
        self.get_all()
        self.get_all_paginated()
        self.find_by_id()
        self.save()
        self.update_by_id()
        self.delete_by_id()
        self.deactivate_by_id()
        self.activate_by_id()
        self.route.get("/list_by_vehicle_id/{vehicle_id}")(self.list_by_vehicle_id)
        self.route.get("/last_by_vehicle_id/{vehicle_id}")(self.last_by_vehicle_id)
        self.route.get("/list_by_vehicle_and_range/{vehicle_id}/{start_timestamp}/{end_timestamp}")(self.list_by_vehicle_and_range)
        self.public_route.websocket("/websocket")(self.websocket_location)

    async def list_by_vehicle_id(self, vehicle_id: int):
        """
        Rota para listar todas as localizações de um veículo específico.
        """
        response = await LocationService().list_by_vehicle_id(vehicle_id=vehicle_id)
        return ResponseModel(
            success=True,
            message=f"Localizações do veículo {vehicle_id} listadas com sucesso",
            object=response,
        ).model_response()
    
    async def last_by_vehicle_id(self, vehicle_id: int):
        """
        Rota para obter a última localização de um veículo específico.
        """
        response = await LocationService().last_by_vehicle_id(vehicle_id=vehicle_id)
        return ResponseModel(
            success=True,
            message=f"Última localização do veículo {vehicle_id} obtida com sucesso",
            object=response,
        ).model_response()
    
    async def list_by_vehicle_and_range(self, vehicle_id: int, start_timestamp: str, end_timestamp: str):
        """
        Rota para listar todas as localizações de um veículo específico em um intervalo de tempo.
        """
        response = await LocationService().list_by_vehicle_and_range(
            vehicle_id=vehicle_id,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        return ResponseModel(
            success=True,
            message=f"Localizações do veículo {vehicle_id} no intervalo especificado listadas com sucesso",
            object=response,
        ).model_response()
    
    
    async def websocket_location(self, websocket: WebSocket):
        """
        Rota WebSocket para receber localizações em tempo real.
        """
        token_header = websocket.headers.get("authorization")
        try:
            await self.token_service.validate_token(token_header)
        except Exception as exc:
            logger.warning("websocket_auth_failed: %s", exc)
            await websocket.close(code=4401)
            return

        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                payload = json.loads(data)

                # Mensagens de handshake/autenticação são ignoradas após validação do header
                if payload.get("type") == "auth":
                    continue

                location_in = LocationCreate(**payload)

                location_obj = await location_service.save(
                    model=Location,
                    new_data=location_in,
                )
                await websocket.send_text(
                    json.dumps(
                        {
                            "success": True,
                            "location_id": location_obj.id,
                            "timestamp": str(location_obj.timestamp),
                        }
                    )
                )
        except WebSocketDisconnect:
            logger.info("websocket_client_disconnected")
        except Exception as exc:
            logger.error("websocket_location_error: %s", exc)
            if websocket.application_state == WebSocketState.CONNECTED:
                await websocket.send_text(json.dumps({"success": False, "error": str(exc)}))
        finally:
            if websocket.application_state == WebSocketState.CONNECTED:
                await websocket.send_text(
                    json.dumps(
                        {
                            "success": False,
                            "message": "connection_closed",
                        }
                    )
                )
                await websocket.close()