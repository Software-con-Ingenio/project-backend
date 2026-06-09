from repositories.juego_repository import JuegoRepository
from sqlalchemy.orm import Session

class JuegoService:
    def __init__(self, db: Session):
        self.repo = JuegoRepository(db)

    def listar_juegos(self, busqueda: str = None):
        juegos = self.repo.obtener_todos(busqueda)
        resultado = []
        for j in juegos:
            # Convertimos el objeto de SQLAlchemy a un diccionario para poder añadir el campo extra
            juego_dict = {
                "id_juego": j.id_juego,
                "nombre": j.nombre,
                "stock_local": j.stock_local,
                "precio": j.precio,
                "stock_global": j.stock_global, 
                # Lógica de la alerta: True si es menor a 3
                "alerta_stock": j.stock_local < 3,
                "es_historico": j.es_historico 
            }
            resultado.append(juego_dict)
        return resultado
    
    def registrar_juego(self, data: dict):
        return self.repo.crear(
            nombre=data['nombre'],
            id_plataforma=data['id_plataforma'],
            id_genero=data['id_genero'],
            precio=data['precio'],
            stock_local=data['stock_local'],
            stock_global=data['stock_global'],
            es_historico=data['es_historico'],
            imagen=data['imagen']
        )
        
    # En services/juego_service.py

# ... tus otros métodos ...

    def actualizar_juego(self, id_juego: int, data: dict):
        """
        Actualiza precio y/o stock de forma dinámica según lo que venga en 'data'.
        """
        juego = self.repo.obtener_por_id(id_juego)
        if not juego:
            raise ValueError(f"El juego con ID {id_juego} no existe.")

        # Actualizar stock si viene en el diccionario
        if 'stock_local' in data:
            if data['stock_local'] < 0:
                raise ValueError("El stock no puede ser un número negativo.")
            juego.stock_local = data['stock_local']

        # Actualizar precio si viene en el diccionario
        if 'precio' in data:
            if float(data['precio']) < 0:
                raise ValueError("El precio no puede ser negativo.")
            juego.precio = data['precio']

        self.repo.guardar_cambios()
        return juego