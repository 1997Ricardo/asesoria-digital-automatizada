from sqlalchemy import Column, Integer, String, Float, Date
from app.database.database import Base

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    proveedor = Column(String)
    fecha = Column(Date)
    base_imponible = Column(Float)
    iva = Column(Float)
    total = Column(Float)
    tipo = Column(String)
