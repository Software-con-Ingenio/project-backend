from sqlalchemy.orm import Session
from domain.models import Sale, DetalleVenta, Videojuego
from repositories.sale_repository import SaleRepository
from datetime import datetime, date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class SaleService:
    def __init__(self, db: Session):
        self.db = db
        self.sale_repo = SaleRepository(db)
        
    def obtener_historial_ventas(self):
        # Retorna todas las ventas con sus detalles cargados
        ventas = self.sale_repo.obtener_todas()
        resultado = []
    
        for v in ventas:
            resultado.append({
                "id_venta": v.id_venta,
                "total": float(v.total or 0),
                "fecha": str(v.fecha) if v.fecha else "Sin fecha",
                "usuario": v.id_usuario if v.id_usuario else "N/A",
                "detalles": [
                    {
                        "nombre_juego": d.juego.nombre, # <--- ¡Gracias a la relación, esto ya funciona!
                        "cantidad": d.cantidad,
                        "precio": float(d.precio_unitario)
                    } for d in v.detalles
                ]
            })
        return resultado
    
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
            
    def obtener_resumen_diario(self, fecha_busqueda: date):
        # 1. Obtenemos las ventas (esto debería funcionar si el repo está bien)
        ventas = self.sale_repo.obtener_ventas_por_fecha(fecha_busqueda)        
        # 2. Convertimos a una lista simple de diccionarios manualmente
        ventas_data = []
        total_recaudado = 0.0
        
        for v in ventas:
            # Aseguramos que el total sea float y no Decimal o None
            total = float(v.total) if v.total else 0.0
            total_recaudado += total
            
            ventas_data.append({
                "id_venta": v.id_venta,
                "total": total,
                "fecha": str(v.fecha) # Convertimos el objeto fecha a string
            })
        
        # 3. Retornamos el diccionario plano
        return {
            "fecha": str(fecha_busqueda),
            "cantidad_ventas": len(ventas),
            "total_recaudado": total_recaudado,
            "ventas": ventas_data
        }
    # --- Lógica de Reportes PDF ---
    def generar_pdf_reporte(self, titulo, ventas, total, nombre_archivo):
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, titulo)
        c.setFont("Helvetica", 12)
        y = 700
        for v in ventas:
            c.drawString(50, y, f"ID: {v['id_venta']} | Fecha: {v['fecha']} | Total: ${v['total']:.2f}")
            y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y - 20, f"TOTAL: ${total:.2f}")
        c.save()

    def obtener_resumen_diario_pdf(self, fecha_busqueda: date):
        ventas = self.sale_repo.obtener_ventas_por_fecha(fecha_busqueda)
        ventas_data = [{"id_venta": v.id_venta, "total": float(v.total or 0), "fecha": str(v.fecha)} for v in ventas]
        return {"fecha": str(fecha_busqueda), "total_recaudado": sum(v['total'] for v in ventas_data), "ventas": ventas_data}

    def obtener_resumen_mensual(self, anio: int, mes: int):
        ventas = self.sale_repo.obtener_ventas_por_mes(anio, mes)
        ventas_data = [{"id_venta": v.id_venta, "total": float(v.total or 0), "fecha": str(v.fecha)} for v in ventas]
        return {"periodo": f"{anio}-{mes}", "total_recaudado": sum(v['total'] for v in ventas_data), "ventas": ventas_data}

    def obtener_resumen_total(self):
        ventas = self.sale_repo.obtener_todas()
        ventas_data = [{"id_venta": v.id_venta, "total": float(v.total or 0), "fecha": str(v.fecha)} for v in ventas]
        return {"periodo": "Histórico Total", "total_recaudado": sum(v['total'] for v in ventas_data), "ventas": ventas_data}