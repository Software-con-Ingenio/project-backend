from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
from services.juego_service import JuegoService

router = APIRouter()



@router.get("/juegos")
def listar_juegos(
    # Agregamos busqueda como un parámetro opcional en la URL
    busqueda: Optional[str] = Query(None, description="Palabra clave para filtrar por nombre"),
    db: Session = Depends(get_db)
):
    service = JuegoService(db)
    # Pasamos el parámetro al servicio
    return service.listar_juegos(busqueda)
@router.post("/juegos")
def crear_juego(data: dict, db: Session = Depends(get_db)):
    service = JuegoService(db)
    return service.registrar_juego(data)
