from repositories.juego_repository import JuegoRepository
from sqlalchemy.orm import Session

class JuegoService:
    def __init__(self, db: Session):
        self.repo = JuegoRepository(db)

    def listar_juegos(self, busqueda: str = None):
        return self.repo.obtener_todos(busqueda)

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