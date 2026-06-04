from sqlalchemy.orm import Session
from domain.models import Usuario

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def existe_email(self, email: str):
        return self.db.query(Usuario).filter(Usuario.email == email).first() is not None

    def crear(self, nombre, email, password_hash, id_rol):
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            contrasena=password_hash,
            id_rol=id_rol,
            activo=True
        )
        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)
        return nuevo_usuario
    
    def obtener_todos(self):
        return self.db.query(Usuario).all()