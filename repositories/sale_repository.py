from sqlalchemy.orm import Session
from domain.models import Sale, DetalleVenta
from sqlalchemy.orm import joinedload
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
    def __init__(self, db):
        self.db = db

    def obtener_todas(self):
        # joinedload permite traer la venta junto con sus detalles en un solo viaje a la BD
        return self.db.query(Sale).options(joinedload(Sale.detalles)).all()
    
    def obtener_ventas_por_fecha(self, fecha_busqueda: date):
    # Esto compara solo la parte de la fecha, ignorando la hora
        return self.db.query(Sale).filter(
        func.date(Sale.fecha) == fecha_busqueda
    ).all()
        
    def obtener_ventas_por_mes(self, anio: int, mes: int):
        # Filtra ventas extrayendo año y mes de la columna fecha
        return self.db.query(Sale).filter(
            extract('year', Sale.fecha) == anio,
            extract('month', Sale.fecha) == mes
        ).all()