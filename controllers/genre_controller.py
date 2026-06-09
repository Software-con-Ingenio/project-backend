from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.genre_service import GenreService
from repositories.genre_repository import GenreRepository
from controllers.auth_controller import obtener_usuario_actual
router = APIRouter()

@router.get("/genres")
def listar_generos(db: Session = Depends(get_db)):
    service = GenreService(db)
    return service.listar_generos()

@router.post("/genres")
def crear_genero(nombre: str, db: Session = Depends(get_db), current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador":
        raise HTTPException(status_code=403, detail="No autorizado")
    repo = GenreRepository(db)
    return repo.crear(nombre)


@router.delete("/genres/{id}")
def eliminar_genero(id: int, db: Session = Depends(get_db), current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador":
        raise HTTPException(status_code=403, detail="No autorizado")

    service = GenreService(db)
    # Asegúrate de pasar el 'id' a tu servicio
    if service.eliminar_genero(id):
        return {"message": "Género eliminado correctamente"}
    
    raise HTTPException(status_code=404, detail="Género no encontrado")