from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from domain.models import Sale, DetalleVenta
from datetime import date
from sqlalchemy import func, extract

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

    def obtener_todas(self):
        return self.db.query(Sale).options(joinedload(Sale.detalles)).all()

    def obtener_ventas_por_fecha(self, fecha_busqueda: date):
        return self.db.query(Sale).filter(
            func.date(Sale.fecha) == fecha_busqueda
        ).all()

    def obtener_ventas_por_mes(self, anio: int, mes: int):
        return self.db.query(Sale).filter(
            extract('year', Sale.fecha) == anio,
            extract('month', Sale.fecha) == mes
        ).all()