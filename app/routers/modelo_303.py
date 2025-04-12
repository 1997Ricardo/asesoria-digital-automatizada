from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import date
from app.database.database import SessionLocal
from app.models.factura import Factura
from app.services.pdf_303 import generar_pdf_modelo_303

router = APIRouter(prefix="/modelo", tags=["Modelo 303"])

# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para calcular rango de fechas de un trimestre
def obtener_rango_trimestre(anio: int, trimestre: int):
    if trimestre == 1:
        return date(anio, 1, 1), date(anio, 3, 31)
    elif trimestre == 2:
        return date(anio, 4, 1), date(anio, 6, 30)
    elif trimestre == 3:
        return date(anio, 7, 1), date(anio, 9, 30)
    elif trimestre == 4:
        return date(anio, 10, 1), date(anio, 12, 31)
    else:
        raise ValueError("Trimestre inválido (1-4)")

# Endpoint JSON: resumen fiscal del Modelo 303
@router.get("/303")
def calcular_modelo_303(
    anio: int = Query(..., description="Año fiscal, ej. 2025"),
    trimestre: int = Query(..., description="Trimestre fiscal (1 a 4)"),
    db: Session = Depends(get_db)
):
    fecha_inicio, fecha_fin = obtener_rango_trimestre(anio, trimestre)

    ingresos = db.query(Factura).filter(
        Factura.tipo == "ingreso",
        Factura.fecha >= fecha_inicio,
        Factura.fecha <= fecha_fin
    ).all()

    gastos = db.query(Factura).filter(
        Factura.tipo == "gasto",
        Factura.fecha >= fecha_inicio,
        Factura.fecha <= fecha_fin
    ).all()

    iva_repercutido = sum(f.iva for f in ingresos)
    iva_soportado = sum(f.iva for f in gastos)
    resultado = iva_repercutido - iva_soportado
    situacion = "A ingresar" if resultado > 0 else "A compensar o devolver"

    return {
        "trimestre": trimestre,
        "anio": anio,
        "iva_repercutido": round(iva_repercutido, 2),
        "iva_soportado": round(iva_soportado, 2),
        "resultado": round(resultado, 2),
        "situacion": situacion
    }

# Endpoint PDF: descarga del Modelo 303 en PDF
@router.get("/303/pdf")
def descargar_modelo_303_pdf(
    anio: int = Query(...),
    trimestre: int = Query(...),
    db: Session = Depends(get_db)
):
    fecha_inicio, fecha_fin = obtener_rango_trimestre(anio, trimestre)

    ingresos = db.query(Factura).filter(
        Factura.tipo == "ingreso",
        Factura.fecha >= fecha_inicio,
        Factura.fecha <= fecha_fin
    ).all()

    gastos = db.query(Factura).filter(
        Factura.tipo == "gasto",
        Factura.fecha >= fecha_inicio,
        Factura.fecha <= fecha_fin
    ).all()

    iva_repercutido = sum(f.iva for f in ingresos)
    iva_soportado = sum(f.iva for f in gastos)
    resultado = iva_repercutido - iva_soportado
    situacion = "A ingresar" if resultado > 0 else "A compensar o devolver"

    pdf_stream = generar_pdf_modelo_303(anio, trimestre, iva_repercutido, iva_soportado, resultado, situacion)

    return StreamingResponse(pdf_stream, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=modelo_303_T{trimestre}_{anio}.pdf"
    })

