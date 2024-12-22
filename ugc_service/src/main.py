from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ugc_service.src.api.v1 import events as v1_events
from ugc_service.src.api.v2 import events as v2_events
from ugc_service.src.core.settings import app_settings

app = FastAPI(
    title=app_settings.project_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=JSONResponse,
)

app.include_router(v1_events.router)
app.include_router(v2_events.router)
