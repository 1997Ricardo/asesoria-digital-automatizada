from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers import factura, modelo_303

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(factura.router)
app.include_router(modelo_303.router)
@app.get("/", response_model=None)
def root():
    return {"mensaje": "Bienvenido a la API de Asesoría Digital"}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})