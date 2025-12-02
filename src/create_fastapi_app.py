from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.models import db_helper
from errors_handlers import register_errors_handlers
from middlewares import register_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


def create_app(
    create_custom_static_urls: bool = False,
) -> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        # webhooks=webhooks_router,
    )
    if create_custom_static_urls:
        pass

    register_errors_handlers(app)
    register_middlewares(app)
    return app
