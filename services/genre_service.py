from repositories.genre_repository import GenreRepository
from sqlalchemy.orm import Session

class GenreService:
    def __init__(self, db: Session):
        self.repo = GenreRepository(db)

    def listar_generos(self):
        return self.repo.obtener_todos()

    def eliminar_genero(self, id_genero: int):
        return self.repo.eliminar(id_genero)