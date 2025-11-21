from fastapi import Depends
from core.abstract.abstract_controller import AbstractController
from core.token.token_service import TokenService, get_user_id_from_token
from core.vehicle.vehicle_model import Vehicle, VehicleCreate, VehicleUpdate
from core.vehicle.vehicle_service import VehicleService
from utils.response_model import ResponseModel

vehicle_service = VehicleService()

class VehicleController(AbstractController):
    def __init__(self):
        super().__init__(
            model=Vehicle,
            model_create=VehicleCreate,
            model_update=VehicleUpdate,
            prefix="/vehicle",
            service=vehicle_service,
            tags=["Vehicle"],
            token_service=TokenService(),
        )
        self.get_all()
        self.get_all_paginated()
        self.find_by_id()
        self.save()
        self.update_by_id()
        self.delete_by_id()
        self.deactivate_by_id()
        self.activate_by_id()
        self.route.get("/list_by_user_id/{user_id}")(self.list_by_user_id)

    async def list_by_user_id(self, user_id:int = Depends(int(get_user_id_from_token))):
        """
        Rota para listar todos os veículos de um usuário específico.
        """
        response = await VehicleService().list_by_user_id(user_id=user_id)
        return ResponseModel(
            success=True,
            message=f"Veículos do usuário {user_id} listados com sucesso",
            object=response,
        ).model_response()

    async def list_online(self):
        """
        Rota para listar todos os veículos online.
        """
        response = await VehicleService().list_online()
        return ResponseModel(
            success=True,
            message="Veículos online listados com sucesso",
            object=response,
        ).model_response()
    
    async def stats(self):
        """
        Rota para obter estatísticas dos veículos.
        """
        response = await VehicleService().stats()

        return ResponseModel(
            success=True,
            message="Estatísticas dos veículos obtidas com sucesso",
            object=response,
        ).model_response()