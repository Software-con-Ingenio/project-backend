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
        
    def actualizar_usuario(self, id_usuario: int, data: dict):
        # 1. Definir los campos permitidos
        campos_permitidos = {'nombre', 'id_rol', 'activo', 'contrasena'}
        
        # 2. Verificar si hay llaves extra que no deberían estar ahí
        for llave in data.keys():
            if llave not in campos_permitidos:
                raise ValueError(f"Campo no permitido: '{llave}'")

        # 3. Buscar el usuario
        usuario = self.repo.obtener_por_id(id_usuario)
        if not usuario:
            raise ValueError(f"Usuario con ID {id_usuario} no encontrado.")
        
        # 4. Actualizar solo lo que viene en el dict
        if 'nombre' in data: usuario.nombre = data['nombre']
        if 'id_rol' in data: usuario.id_rol = data['id_rol']
        if 'activo' in data: usuario.activo = data['activo']
        if 'contrasena' in data:
            usuario.contrasena = pwd_context.hash(data['contrasena'])
            
        self.repo.guardar_cambios()
        return usuario
    
    def eliminar_usuario(self, id_usuario: int, borrado_fisico: bool = False):
        usuario = self.repo.obtener_por_id(id_usuario)
        if not usuario:
            raise ValueError(f"Usuario con ID {id_usuario} no encontrado.")
        
        if borrado_fisico:
            self.repo.eliminar_fisicamente(usuario)
        else:
            # Baja lógica: el usuario sigue existiendo pero ya no es "activo"
            usuario.activo = False
            self.repo.guardar_cambios()
        
        return True