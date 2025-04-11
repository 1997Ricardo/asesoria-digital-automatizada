from app.database.database import engine, Base
from app.models.factura import Factura

print("Creando base de datos...")
Base.metadata.create_all(bind=engine)
print("¡Base de datos creada!")
