from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import AuthService
from domain.models import Usuario

router = APIRouter()
# Esta variable habilita el candado en Swagger
security = HTTPBearer()

# Dependencia para obtener el usuario actual
def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    auth_service = AuthService(db)
    payload = auth_service.verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return payload

@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    try:
        service = AuthService(db)
        # 1. Obtenemos el token
        token = service.autenticar_usuario(data['email'], data['contrasena'])
        
        # 2. OBTENEMOS EL USUARIO (para sacar su rol)
        # Necesitas una forma de buscar al usuario en la BD por su email
        user = db.query(Usuario).filter(Usuario.email == data['email']).first()
        
        # 3. Retornamos el token Y el id_rol
        return {
            "access_token": token, 
            "token_type": "bearer",
            "id_rol": user.id_rol, # <--- AQUÍ ESTÁ LA MAGIA
            "nombre_usuario": user.nombre
        }
    except ValueError:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
@router.get("/perfil")
def obtener_perfil(current_user: dict = Depends(obtener_usuario_actual), db: Session = Depends(get_db)):
    # Imprime esto para ver exactamente qué claves tiene tu diccionario
    print(f"DEBUG: Contenido de current_user: {current_user}")
    
    # Intenta usar 'id_usuario' si es como se llama en tu modelo
    usuario_id = current_user.get("id_usuario") or current_user.get("id") or current_user.get("sub")
    
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    return {
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rol": usuario.rol.nombre_rol if usuario.rol else "Sin rol",
        "total_ventas": len(usuario.ventas)
    }