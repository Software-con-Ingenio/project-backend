
from fastapi import APIRouter, Depends, Query, HTTPException
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


@router.put("/juegos/{id_juego}/stock")
def actualizar_stock(id_juego: int, nueva_cantidad: int, db: Session = Depends(get_db)):
    try:
        service = JuegoService(db)
        juego = service.actualizar_stock_local(id_juego, nueva_cantidad)
        return {"message": "Stock actualizado con éxito", "id_juego": juego.id_juego, "nuevo_stock": juego.stock_local}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al actualizar el stock")