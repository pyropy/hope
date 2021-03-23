from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
import uvicorn

from app.api.routes import router as api_router
from app.core import config, tasks

import logging

logger = logging.getLogger(__name__)

def get_application():
    
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    ) 

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    #@repeat_every(seconds=config.CDN_LINK_LIFESPAN)
    @app.on_event("startup")
    @repeat_every(seconds=5)
    async def update_cdn_sharing_links() -> None:
        pass

    app.include_router(api_router, prefix="/api")

    return app

app = get_application()
