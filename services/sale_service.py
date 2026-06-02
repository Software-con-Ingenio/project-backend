from sqlalchemy.orm import Session
from domain.models import Sale, DetalleVenta, Videojuego
from repositories.sale_repository import SaleRepository
from repositories.juego_repository import JuegoRepository

class SaleService:
    def __init__(self, db: Session):
        self.db = db
        self.sale_repo = SaleRepository(db)
        self.juego_repo = JuegoRepository(db)

    def registrar_venta(self, data: dict):
        # 1. Validación inicial de datos
        detalles = data.get('detalles', [])
        if not detalles:
            raise ValueError("La venta debe tener al menos un detalle.")

        # 2. Validación de existencia y stock (Transacción segura)
        # Hacemos esto antes de guardar nada para evitar inconsistencias
        for item in detalles:
            juego = self.db.query(Videojuego).filter(Videojuego.id_juego == item['id_juego']).first()
            
            if not juego:
                raise ValueError(f"El juego con ID {item['id_juego']} no existe.")
                
            if juego.stock_local < item['cantidad']:
                raise ValueError(f"Stock insuficiente para {juego.nombre}. Disponible: {juego.stock_local}")

        # 3. Crear el encabezado de la venta
        nueva_venta = Sale(
            total=data['total'], 
            id_usuario=data['id_usuario']
        )
        self.sale_repo.crear_venta(nueva_venta)

        # 4. Procesar detalles y actualizar stock
        for item in detalles:
            # Crear el registro del detalle
            detalle = DetalleVenta(
                id_venta=nueva_venta.id_venta,
                id_juego=item['id_juego'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario']
            )
            self.sale_repo.crear_detalle(detalle)
            
            # Descontar stock del juego correspondiente
            juego = self.db.query(Videojuego).filter(Videojuego.id_juego == item['id_juego']).first()
            juego.stock_local -= item['cantidad']
        
        # Guardar todos los cambios en la base de datos
        self.db.commit()
        return nueva_venta