from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.juego_service import JuegoService

router = APIRouter()

@router.get("/juegos")
def listar_juegos(db: Session = Depends(get_db)):
    service = JuegoService(db)
    return service.listar_juegos()

@router.post("/juegos")
def crear_juego(data: dict, db: Session = Depends(get_db)):
    service = JuegoService(db)
    return service.registrar_juego(data)