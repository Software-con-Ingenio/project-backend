from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.usuario_service import UsuarioService
from controllers.auth_controller import obtener_usuario_actual

router = APIRouter()

@router.post("/usuarios")
def crear_usuario(data: dict, db: Session = Depends(get_db), current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador":
        raise HTTPException(status_code=403, detail="No autorizado")
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

@router.put("/usuarios/{id_usuario}")
def editar_usuario(id_usuario: int, data: dict, db: Session = Depends(get_db), current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador":
        raise HTTPException(status_code=403, detail="No autorizado")
    try:
        service = UsuarioService(db)
        service.actualizar_usuario(id_usuario, data)
        return {"message": "Usuario actualizado correctamente"}
    except ValueError as e:
        # Esto atrapará tu error de "Campo no permitido" y enviará un 400
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/usuarios/{id_usuario}")
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db), current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador":
         raise HTTPException(status_code=403, detail="No autorizado")
    try:
        service = UsuarioService(db)
        service.eliminar_usuario(id_usuario, borrado_fisico=True)
        return {"message": "Usuario eliminado físicamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
