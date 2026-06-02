from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from repositories.platform_repository import PlatformRepository

router = APIRouter()

@router.post("/platforms")
def crear_plataforma(nombre: str, db: Session = Depends(get_db)):
    repo = PlatformRepository(db)
    return repo.crear(nombre)