from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ugc_service.src.api.v1 import events
from ugc_service.src.core.settings import app_settings
from ugc_service.src.services.kafka import KafkaService


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    kafka = KafkaService(
        AIOKafkaProducer(
            bootstrap_servers=[
                f"{app_settings.kafka_host}:{app_settings.kafka_port}"
            ],
        )
    )
    try:
        app.state.kafka = kafka
        await kafka.producer.start()
        yield
    finally:
        await kafka.producer.stop()


app = FastAPI(
    title=app_settings.project_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=JSONResponse,
    lifespan=lifespan,
)

app.include_router(events.router)
