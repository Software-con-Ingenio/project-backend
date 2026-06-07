from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.platform_repository import PlatformRepository
from controllers.auth_controller import obtener_usuario_actual
from services.platform_service import PlatformService
router = APIRouter()


@router.get("/platforms")

def listar_plataformas(db: Session = Depends(get_db)):
    service = PlatformService(db)
    return service.listar_plataformas()

@router.post("/platforms")
def crear_plataforma(nombre: str, db: Session = Depends(get_db), current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador":
        raise HTTPException(status_code=403, detail="No autorizado")
    repo = PlatformRepository(db)
    return repo.crear(nombre)