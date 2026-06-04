from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.usuario_service import UsuarioService

router = APIRouter()

@router.post("/usuarios")
def crear_usuario(data: dict, db: Session = Depends(get_db)):
    try:
        service = UsuarioService(db)
        usuario = service.registrar_usuario(data)
        return {"message": "Usuario creado con éxito", "id": usuario.id_usuario}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    service = UsuarioService(db)
    return service.listar_usuarios()