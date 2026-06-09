from sqlalchemy.orm import Session
from domain.models import Platform, Videojuego

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
    
    def eliminar(self, id_plataforma: int):
        plataforma = self.db.query(Platform).filter(Platform.id_plataforma == id_plataforma).first()
        if plataforma:
            # Desasociamos videojuegos para evitar que la eliminación falle por clave foránea.
            self.db.query(Videojuego).filter(Videojuego.id_plataforma == id_plataforma).update(
                {Videojuego.id_plataforma: None},
                synchronize_session=False,
            )
            self.db.delete(plataforma)
            self.db.commit()
            return True
        return False