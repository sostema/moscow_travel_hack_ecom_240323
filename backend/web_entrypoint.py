from logging import _nameToLevel

import uvicorn
from presentation.web.main import create_app
from shared.base import logger
from shared.settings import app_settings

uvicorn_app = create_app()

if __name__ == "__main__":
    logger.info(
        "starting server on {}:{} with {} workers",
        app_settings.uvicorn_host,
        app_settings.uvicorn_port,
        app_settings.uvicorn_workers,
    )
    if not app_settings.uvicorn_ssl:
        app_settings.uvicorn_ssl_keyfile = None
        app_settings.uvicorn_ssl_certfile = None

    uvicorn.run(
        "web_entrypoint:uvicorn_app",
        host=app_settings.uvicorn_host,
        port=app_settings.uvicorn_port,
        workers=app_settings.uvicorn_workers,
        log_level=_nameToLevel[app_settings.uvicorn_log_level],
        ssl_keyfile=app_settings.uvicorn_ssl_keyfile,
        ssl_certfile=app_settings.uvicorn_ssl_certfile,
    )
