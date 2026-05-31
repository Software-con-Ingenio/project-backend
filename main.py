from fastapi import FastAPI
from database import engine, Base
from domain import models

# Esto crea las tablas si no existen
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "El backend está vivo"}