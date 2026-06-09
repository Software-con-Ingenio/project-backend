from repositories.platform_repository import PlatformRepository
from sqlalchemy.orm import Session

class PlatformService:
    def __init__(self, db: Session):
        self.repo = PlatformRepository(db)

    def listar_plataformas(self):
        return self.repo.obtener_todos()
    
    def eliminar_plataforma(self, id_plataforma: int):
        return self.repo.eliminar(id_plataforma)
