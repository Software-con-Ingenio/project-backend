from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from repositories.usuario_repository import UsuarioRepository

# Configuración de seguridad
SECRET_KEY = "tu_clave_secreta_super_segura"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class AuthService:
    def __init__(self, db):
        self.repo = UsuarioRepository(db)

    def autenticar_usuario(self, email, contrasena):
        usuario = self.repo.obtener_por_email(email) # Asegúrate de tener este método en tu repo
        if not usuario or not pwd_context.verify(contrasena, usuario.contrasena):
            raise ValueError("Credenciales inválidas")
        
        # Crear token
        payload = {
            "sub": str(usuario.id_usuario), 
            "rol": usuario.rol.nombre_rol,
            "exp": datetime.utcnow() + timedelta(hours=8)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def verificar_token(self, token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            return None