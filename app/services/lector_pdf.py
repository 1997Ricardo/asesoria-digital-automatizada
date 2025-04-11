import pdfplumber
import re
from datetime import datetime

def extraer_datos_desde_pdf(file) -> dict:
    texto_completo = ""
    with pdfplumber.open(file) as pdf:
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + "\n"

    proveedor = extraer_proveedor(texto_completo)
    fecha = extraer_fecha(texto_completo)
    base = extraer_valor(texto_completo, r"Base imponible.*?([\d,.]+)")
    iva = extraer_valor(texto_completo, r"IVA.*?([\d,.]+)")
    total = extraer_valor(texto_completo, r"Total.*?([\d,.]+)")

    return {
        "proveedor": proveedor or "Desconocido",
        "fecha": fecha,
        "base_imponible": base,
        "iva": iva,
        "total": total,
        "tipo": "gasto"
    }

def extraer_proveedor(texto: str):
    lineas = texto.splitlines()
    return lineas[0].strip() if lineas else None

def extraer_fecha(texto: str):
    match = re.search(r"(\d{2}/\d{2}/\d{4})", texto)
    if match:
        return datetime.strptime(match.group(1), "%d/%m/%Y").date()
    return None

def extraer_valor(texto: str, patron: str):
    match = re.search(patron, texto, re.IGNORECASE)
    if match:
        return float(match.group(1).replace(",", "."))
    return 0.0
