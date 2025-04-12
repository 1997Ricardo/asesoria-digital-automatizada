from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.database.database import SessionLocal
from app.models.factura import Factura
from app.services.lector_pdf import extraer_datos_desde_pdf

router = APIRouter(prefix="/facturas", tags=["Facturas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/subir")
async def subir_factura(file: UploadFile = File(...), db: Session = Depends(get_db)):
    datos = extraer_datos_desde_pdf(file.file)
    nueva_factura = Factura(**datos)
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    return {"mensaje": "Factura guardada con datos reales", "datos": datos}
from typing import List
from app.models.factura import Factura
from sqlalchemy.orm import Session

@router.get("/", response_model=List[dict])
def listar_facturas(db: Session = Depends(get_db)):
    facturas = db.query(Factura).all()
    return [
        {
            "id": f.id,
            "proveedor": f.proveedor,
            "fecha": f.fecha,
            "base_imponible": f.base_imponible,
            "iva": f.iva,
            "total": f.total,
            "tipo": f.tipo
        } for f in facturas
    ]