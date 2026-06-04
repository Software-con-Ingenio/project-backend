from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import AuthService

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
        # Asegúrate de que los nombres de los campos en 'data' coincidan con tu JSON
        token = service.autenticar_usuario(data['email'], data['contrasena'])
        return {"access_token": token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")