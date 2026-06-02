from sqlalchemy.orm import Session
from domain.models import Sale, DetalleVenta, Videojuego
from repositories.sale_repository import SaleRepository
from datetime import datetime

class SaleService:
    def __init__(self, db: Session):
        self.db = db
        self.sale_repo = SaleRepository(db)
        
    def obtener_historial_ventas(self):
        # Retorna todas las ventas con sus detalles cargados
        ventas = self.sale_repo.obtener_todas()
        return ventas
    
    def registrar_venta(self, data: dict):
        detalles = data.get('detalles', [])
        if not detalles:
            raise ValueError("La venta debe tener al menos un detalle.")

        total_calculado = 0
        lista_detalles = []

        # 1. Validación de disponibilidad y cálculo de precio
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

        # 2. Creación de la venta con la fecha actual
        nueva_venta = Sale(
            total=total_calculado, 
            id_usuario=data['id_usuario'],
            fecha=datetime.now() # <--- Fecha registrada al momento de la venta
        )
        self.sale_repo.crear_venta(nueva_venta)

        # 3. Creación de detalles y actualización de stock
        for d in lista_detalles:
            detalle = DetalleVenta(
                id_venta=nueva_venta.id_venta,
                id_juego=d['juego'].id_juego,
                cantidad=d['cantidad'],
                precio_unitario=d['precio']
            )
            self.sale_repo.crear_detalle(detalle)
            
            # Descuento de stock
            d['juego'].stock_local -= d['cantidad']
        
        self.db.commit()
        return nueva_venta
    
    def calcular_resumen_venta(self, detalles_solicitados: list):
            resumen = []
            total_general = 0

            for item in detalles_solicitados:
                # CAMBIO: Aquí accedemos con punto '.' en lugar de corchetes '[]'
                juego = self.db.query(Videojuego).filter(Videojuego.id_juego == item.id_juego).first()
                if not juego:
                    raise ValueError(f"Juego {item.id_juego} no encontrado")
                
                precio = float(juego.precio)
                subtotal = precio * item.cantidad 
                total_general += subtotal
                
                resumen.append({
                    "nombre": juego.nombre,
                    "cantidad": item.cantidad, 
                    "precio_unitario": precio,
                    "subtotal": subtotal
                })
                
            return {
                "items": resumen,
                "total_a_pagar": total_general
            }