import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import articles_router
from app.utils.scheduler import start_scheduler, shutdown_scheduler

# Configure logging for production
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    start_scheduler()
    logger.info("Application startup complete")
    yield
    shutdown_scheduler()
    logger.info("Application shutdown complete")


app = FastAPI(title="Bright World News API", lifespan=lifespan)
app.include_router(articles_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS enabled for origins: {settings.cors_origins_list}")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
