from passlib.context import CryptContext
from repositories.usuario_repository import UsuarioRepository

# Cambiamos a argon2id
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class UsuarioService:
    def __init__(self, db):
        self.repo = UsuarioRepository(db)

    def registrar_usuario(self, data: dict):
        if self.repo.existe_email(data['email']):
            raise ValueError("El correo electrónico ya está registrado.")
        
        # Argon2id no tiene el límite de 72 bytes, así que simplemente hasheamos
        hashed_password = pwd_context.hash(data['contrasena'])
        
        return self.repo.crear(
            nombre=data['nombre'],
            email=data['email'],
            password_hash=hashed_password,
            id_rol=data['id_rol']
        )
        
    def listar_usuarios(self):
        usuarios = self.repo.obtener_todos()
        # Filtramos la contraseña antes de retornar la lista
        return [
            {
                "id_usuario": u.id_usuario,
                "nombre": u.nombre,
                "email": u.email,
                "id_rol": u.id_rol,
                "activo": u.activo
            } for u in usuarios
        ]