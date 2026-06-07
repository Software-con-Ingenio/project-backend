from sqlalchemy.orm import Session
from domain.models import Platform

class PlatformRepository:
    def __init__(self, db: Session):
        self.db = db
    def obtener_todos(self):
        return self.db.query(Platform).all()
    
    def crear(self, nombre: str):
        nueva_plataforma = Platform(nombre_plataforma=nombre)
        self.db.add(nueva_plataforma)
        self.db.commit()
        self.db.refresh(nueva_plataforma)
        return nueva_plataforma