import pydantic
import dotenv
from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import logger
from app.api.health import router as health_router
from app.schemas.analytics import router as analytics_router

app=FastAPI()

app.include_router(health_router)
app.include_router(analytics_router)


app.include_router(router)

@app.get("/")
def read_root():
    return {"ARIP running"}
