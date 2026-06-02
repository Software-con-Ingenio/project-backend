from sqlalchemy.orm import Session
from domain.models import Videojuego

class JuegoRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_todos(self):
        return self.db.query(Videojuego).all()

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