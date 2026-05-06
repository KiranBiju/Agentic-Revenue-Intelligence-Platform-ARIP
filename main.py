import pydantic
import dotenv
from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import setup_logging

setup_logging()

app=FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"ARIP running"}
