import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from presentation.dependencies import container
from presentation.web.router import router

PARENT = Path(os.path.realpath(__file__)).parent
with open(PARENT / "rapidoc.html", "r") as f:
    _rapidoc_html = f.read()


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)

    @app.on_event("startup")
    async def startup() -> None:
        FastAPICache.init(
            RedisBackend(container.redis_repository.r), prefix="fastapi-cache"
        )

    @app.get("/rapidoc", response_class=HTMLResponse, include_in_schema=False)
    def rapidoc() -> str:
        return _rapidoc_html.format(openapi_url="/openapi.json")

    return app
