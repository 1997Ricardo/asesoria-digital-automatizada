from fastapi import FastAPI
from app.routers import factura

app = FastAPI()

app.include_router(factura.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de Asesoría Digital"}
