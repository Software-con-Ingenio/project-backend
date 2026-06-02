from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.sale_service import SaleService

router = APIRouter()

@router.get("/ventas")
def listar_ventas(db: Session = Depends(get_db)):
    service = SaleService(db)
    return service.obtener_historial_ventas()

@router.post("/ventas")
def realizar_venta(venta_data: dict, db: Session = Depends(get_db)):
    try:
        service = SaleService(db)
        # Aquí estamos asumiendo que el JSON trae { "total": 100, "id_usuario": 1, "detalles": [...] }
        venta = service.registrar_venta(venta_data)
        return {"message": "Venta realizada con éxito", "id_venta": venta.id_venta}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al procesar la venta")