from fastapi import FastAPI
import pydantic
import dotenv

app=FastAPI()

@app.get("/")
def read_root():
    return {"ARIP running"}

