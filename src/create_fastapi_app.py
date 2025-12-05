from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from sqladmin import Admin

from redis.asyncio import Redis

from admin import register_admin_views

from core.models import db_helper
from core.config import settings
from errors_handlers import register_errors_handlers
from middlewares import register_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache,
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix,
    )
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

    admin = Admin(
        app=app,
        session_maker=db_helper.session_factory,
    )
    register_admin_views(admin)
    return app
