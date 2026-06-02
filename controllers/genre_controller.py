from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.genre_service import GenreService
from repositories.genre_repository import GenreRepository

router = APIRouter()

@router.get("/genres")
def listar_generos(db: Session = Depends(get_db)):
    service = GenreService(db)
    return service.listar_generos()

@router.post("/genres")
def crear_genero(nombre: str, db: Session = Depends(get_db)):
    repo = GenreRepository(db)
    return repo.crear(nombre)