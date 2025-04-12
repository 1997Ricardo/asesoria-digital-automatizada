from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generar_pdf_modelo_303(anio: int, trimestre: int, iva_repercutido: float, iva_soportado: float, resultado: float, situacion: str):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle(f"Modelo 303 - T{trimestre} {anio}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 800, f"Resumen Modelo 303 - Trimestre {trimestre} / {anio}")

    c.setFont("Helvetica", 12)
    c.drawString(100, 760, f"IVA repercutido (ingresos): {iva_repercutido:.2f} €")
    c.drawString(100, 740, f"IVA soportado (gastos): {iva_soportado:.2f} €")
    c.drawString(100, 720, f"Resultado: {resultado:.2f} €")
    c.drawString(100, 700, f"Situación: {situacion}")

    c.save()
    buffer.seek(0)
    return buffer