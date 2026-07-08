from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
from services.juego_service import JuegoService
from controllers.auth_controller import obtener_usuario_actual

router = APIRouter()



@router.get("/juegos")
def listar_juegos(
    busqueda: Optional[str] = Query(None, description="Palabra clave para filtrar por nombre"),
    db: Session = Depends(get_db)
):
    service = JuegoService(db)
    return service.listar_juegos(busqueda)

@router.post("/juegos")
def crear_juego(data: dict, db: Session = Depends(get_db), current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador":
        raise HTTPException(status_code=403, detail="No autorizado")
    service = JuegoService(db)
    return service.registrar_juego(data)


@router.put("/juegos/{id_juego}")
def actualizar_juego(id_juego: int, data: dict, db: Session = Depends(get_db)):
    try:
        service = JuegoService(db)
        juego = service.actualizar_juego(id_juego, data)
        return {"message": "Juego actualizado correctamente", "juego": {"id": juego.id_juego, "precio": juego.precio, "stock": juego.stock_local}}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))