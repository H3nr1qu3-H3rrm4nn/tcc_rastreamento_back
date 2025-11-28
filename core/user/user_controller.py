import logging
import logging.config

from fastapi import APIRouter, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.abstract.abstract_controller import AbstractController
from core.token.token_service import TokenService
from core.user.user_model import User, UserLogin, UserCreate, UserUpdate
from core.user.user_service import UserService
import yaml

from utils.response_model import ResponseModel
from utils.context_vars import user_id as context_user_id


logger = logging.getLogger(__name__)

user_service = UserService()
bearer_scheme = HTTPBearer(auto_error=True)

class UserController(AbstractController):
    def __init__(self):
        super().__init__(
            model=User,
            model_create=UserCreate,
            model_update=UserUpdate,
            prefix="/user",
            service=user_service,
            tags=["User"],
            token_service=TokenService(),
        )
        self.public_route = APIRouter(prefix="/user", tags=["User"])

        self.get_all()
        self.get_all_paginated()
        self.find_by_id()
        self.update_by_id()
        self.delete_by_id()
        self.deactivate_by_id()
        self.activate_by_id()
        self.audit()

        self.public_route.post("/save")(self.save)
        self.public_route.post("/login")(self.login)
        self.route.get("/find_user_by_token")(self.find_user_by_token)

    async def save(self, new_data: UserCreate):
        """
        Rota save sobrescrita para garantir que a senha seja encriptada.
        """
        
        response = await user_service.save(
            model=User,
            new_data=new_data
        )
        return ResponseModel(
            success=True,
            message="Usuário criado com sucesso com senha encriptada",
            object=response,
        ).model_response()

    async def login(self, user: UserLogin, req: Request):
        logger.info("login_attempt email=%s", user.email)
        dados_autenticacao = await user_service.login(user=user, req=req)
        return ResponseModel(
            success=True,
            message="Login realizado com sucesso",
            object=dados_autenticacao
        ).model_response()

    async def find_user_by_token(
        self,
        credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    ):
        logger.info("find_user_by_token_request_received", extra={
            "has_credentials": credentials is not None,
            "scheme": getattr(credentials, "scheme", None),
        })
        token = credentials.credentials if credentials else None
        logger.info("find_user_by_token_extracted_token", extra={
            "token_present": bool(token),
        })
        # validate_token também popula context vars se necessário
        await self.token_service.validate_token(f"Bearer {token}")
        logger.info("find_user_by_token_token_validated")
        response = await user_service.find_by_token(token)
        logger.info("find_user_by_token_user_loaded", extra={
            "user_found": bool(response),
        })
        return ResponseModel(
            success=True,
            message="Usuário retornado com sucesso",
            object=response
        ).model_response()

