
import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.security import HTTPBearer
from core.location.location_controller import LocationController
from core.vehicle.vehicle_controller import VehicleController
from middleware.jwt_middleware import JWTMiddleware
from utils.base import Base
from core.user.user_controller import UserController
from utils.connection_pool import ConnectionPool
from fastapi.middleware.cors import CORSMiddleware
from utils.logging_config import setup_logging
from utils.settings import Settings
from urllib.parse import urlsplit, urlunsplit

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

setup_logging()
logger = logging.getLogger(__name__)


def _mask_database_url(url: str) -> str:
    if not url:
        return ""
    parts = urlsplit(url)
    if not parts.username:
        return url
    netloc = parts.netloc.replace(f"{parts.username}:{parts.password}", f"{parts.username}:***") if parts.password else parts.netloc
    return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))


settings = Settings()
logger.info("Using database %s", _mask_database_url(settings.DATABASE_URL))


async def wait_for_db(engine, retries: int = 5, delay: float = 1.0) -> None:
    for attempt in range(1, retries + 1):
        try:
            async with engine.connect() as conn:
                await conn.exec_driver_sql("SELECT 1")
            logger.info("Database is ready.")
            return
        except Exception as exc:
            logger.warning("DB not ready (attempt %s/%s): %s", attempt, retries, exc)
            await asyncio.sleep(delay)
    raise RuntimeError("Database not available after retries")
# Cria as tabelas no banco de dados

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: cria tabelas
    engine = ConnectionPool.get_engine()
    await wait_for_db(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        # Shutdown: encerra conexões
        await engine.dispose()

app = FastAPI(
    title="API de Rastreamento de Frota",
    description="API para o TCC de Análise e Desenvolvimento de Sistemas.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # ou liste URLs específicas do seu front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    JWTMiddleware
)

user_controller = UserController()
vehicle_controller = VehicleController()
location_controller = LocationController()

app.include_router(user_controller.public_route)
app.include_router(user_controller.route)
app.include_router(vehicle_controller.route)
app.include_router(location_controller.public_route)
app.include_router(location_controller.route)



