from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings

from api import router as api_router
from core.models import db_helper
from api.webhooks import webhooks_router


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    # webhooks=webhooks_router,
)
main_app.include_router(
    api_router,
)

main_app.webhooks.include_router(webhooks_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
