from sqlalchemy.orm import Session
from domain.models import Sale, DetalleVenta
from sqlalchemy.orm import joinedload

class SaleRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_venta(self, venta: Sale):
        self.db.add(venta)
        self.db.commit()
        self.db.refresh(venta)
        return venta

    def crear_detalle(self, detalle: DetalleVenta):
        self.db.add(detalle)
        self.db.commit()
        return detalle
    def __init__(self, db):
        self.db = db

    def obtener_todas(self):
        # joinedload permite traer la venta junto con sus detalles en un solo viaje a la BD
        return self.db.query(Sale).options(joinedload(Sale.detalles)).all()