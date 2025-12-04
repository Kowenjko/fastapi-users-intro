import logging

import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse


from core.config import settings

from api import router as api_router

from api.webhooks import webhooks_router
from create_fastapi_app import create_app

from utils.templates import templates


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


main_app = create_app()

@main_app.get("/")
def index_page(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
    )


main_app.include_router(api_router)

main_app.webhooks.include_router(webhooks_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
