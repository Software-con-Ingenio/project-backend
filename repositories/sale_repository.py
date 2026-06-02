from sqlalchemy.orm import Session
from domain.models import Sale, DetalleVenta

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