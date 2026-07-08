from sqlalchemy.orm import Session
from domain.models import Genre, Videojuego

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
    
    def eliminar(self, id_genero: int):
        genero = self.db.query(Genre).filter(Genre.id_genero == id_genero).first()
        if genero:
            # Desasociamos videojuegos para evitar que la eliminación falle por clave foránea.
            self.db.query(Videojuego).filter(Videojuego.id_genero == id_genero).update(
                {Videojuego.id_genero: None},
                synchronize_session=False,
            )
            self.db.delete(genero)
            self.db.commit()
            return True
        return False