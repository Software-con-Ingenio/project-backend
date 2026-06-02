from sqlalchemy.orm import Session
from domain.models import Videojuego

class JuegoRepository:
    def __init__(self, db: Session):
        self.db = db

    # Añadimos 'busqueda: str = None' como parámetro opcional
    def obtener_todos(self, busqueda: str = None):
        query = self.db.query(Videojuego)
        if busqueda:
            query = query.filter(Videojuego.nombre.ilike(f"%{busqueda}%"))
        return query.all()


    def obtener_por_id(self, id_juego: int):
        return self.db.query(Videojuego).filter(Videojuego.id_juego == id_juego).first()

    # NUEVO: Método para persistir los cambios
    def guardar_cambios(self):
        self.db.commit()



    def crear(self, nombre: str, id_plataforma: int, id_genero: int, precio: float, stock_local: int, stock_global: int, es_historico: bool, imagen: str):
        nuevo_juego = Videojuego(
            nombre=nombre,
            id_plataforma=id_plataforma,
            id_genero=id_genero,
            precio=precio,
            stock_local=stock_local,
            stock_global=stock_global,
            es_historico=es_historico,
            imagen=imagen
        )
        self.db.add(nuevo_juego)
        self.db.commit()
        self.db.refresh(nuevo_juego)
        return nuevo_juego