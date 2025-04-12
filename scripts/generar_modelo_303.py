import os
import sys
from datetime import datetime
import sys

# Añadir la raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.factura import Factura
from app.routers.modelo_303 import obtener_rango_trimestre
from app.services.pdf_303 import generar_pdf_modelo_303
from app.services.email import enviar_pdf_por_email

def generar_y_guardar_modelo(anio: int, trimestre: int):
    db: Session = SessionLocal()
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

    # Generar el PDF
    pdf = generar_pdf_modelo_303(anio, trimestre, iva_repercutido, iva_soportado, resultado, situacion)

    # Guardar archivo
    filename = f"modelo_303_T{trimestre}_{anio}.pdf"
    output_path = os.path.join("modelos", filename)
    with open(output_path, "wb") as f:
        f.write(pdf.read())

    print(f"Modelo 303 generado y guardado en: {output_path}")

    # Enviar por email
    enviar_pdf_por_email(
        output_path,
        asunto=f"Modelo 303 T{trimestre} / {anio}",
        mensaje="Adjunto el resumen fiscal del trimestre generado automáticamente por la asesoría digital."
    )

if __name__ == "__main__":
    ahora = datetime.now()
    # Cambia el trimestre si estás fuera del actual
    generar_y_guardar_modelo(anio=ahora.year, trimestre=2)