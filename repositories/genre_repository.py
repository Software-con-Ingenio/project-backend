from sqlalchemy.orm import Session
from domain.models import Genre

class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_todos(self):
        return self.db.query(Genre).all()
    
    def crear(self, nombre: str):
        nuevo = Genre(nombre_genero=nombre)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo