from sqlalchemy.orm import Session
from domain.models import Sale, DetalleVenta, Videojuego
from repositories.sale_repository import SaleRepository

class SaleService:
    def __init__(self, db: Session):
        self.db = db
        self.sale_repo = SaleRepository(db)

    def registrar_venta(self, data: dict):
        detalles = data.get('detalles', [])
        if not detalles:
            raise ValueError("La venta debe tener al menos un detalle.")

        total_calculado = 0
        lista_detalles = []

        for item in detalles:
            juego = self.db.query(Videojuego).filter(Videojuego.id_juego == item['id_juego']).first()
            
            if not juego:
                raise ValueError(f"El juego con ID {item['id_juego']} no existe.")
            
            # Verificación de nullidad para el precio
            if juego.precio is None:
                raise ValueError(f"El juego {juego.nombre} no tiene un precio definido.")
            
            if juego.stock_local < item['cantidad']:
                raise ValueError(f"Stock insuficiente para {juego.nombre}.")

            # Conversión segura a float
            precio_unitario = float(juego.precio)
            total_calculado += (item['cantidad'] * precio_unitario)

            lista_detalles.append({
                "juego": juego,
                "cantidad": item['cantidad'],
                "precio": precio_unitario
            })

        nueva_venta = Sale(total=total_calculado, id_usuario=data['id_usuario'])
        self.sale_repo.crear_venta(nueva_venta)

        for d in lista_detalles:
            detalle = DetalleVenta(
                id_venta=nueva_venta.id_venta,
                id_juego=d['juego'].id_juego,
                cantidad=d['cantidad'],
                precio_unitario=d['precio']
            )
            self.sale_repo.crear_detalle(detalle)
            d['juego'].stock_local -= d['cantidad']
        
        self.db.commit()
        return nueva_venta