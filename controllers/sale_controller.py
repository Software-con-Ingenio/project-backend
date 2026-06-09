from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.sale_service import SaleService
from pydantic import BaseModel
from typing import List
from datetime import date
from fastapi.responses import FileResponse
from controllers.auth_controller import obtener_usuario_actual

router = APIRouter()

class DetalleItem(BaseModel):
    id_juego: int
    cantidad: int

class VentaRequest(BaseModel):
    id_usuario: int
    detalles: List[DetalleItem]


@router.get("/ventas/reporte/pdf/diario/{fecha}")
def descargar_reporte_diario(fecha: date, db: Session = Depends(get_db), current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador":
        raise HTTPException(status_code=403, detail="No autorizado")
    service = SaleService(db)
    resumen = service.obtener_resumen_diario(fecha)
    archivo = f"reporte_diario_{fecha}.pdf"
    service.generar_pdf_reporte(f"Reporte Diario: {fecha}", resumen['ventas'], resumen['total_recaudado'], archivo)
    return FileResponse(archivo, media_type='application/pdf', filename=archivo)

@router.get("/ventas/reporte/pdf/mensual/{anio}/{mes}")
def descargar_reporte_mensual(anio: int, mes: int, db: Session = Depends(get_db), current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador":
        raise HTTPException(status_code=403, detail="No autorizado")
    service = SaleService(db)
    resumen = service.obtener_resumen_mensual(anio, mes)
    archivo = f"reporte_mensual_{anio}_{mes}.pdf"
    service.generar_pdf_reporte(f"Reporte Mensual: {mes}/{anio}", resumen['ventas'], resumen['total_recaudado'], archivo)
    return FileResponse(archivo, media_type='application/pdf', filename=archivo)

@router.get("/ventas/reporte/pdf/total")
def descargar_reporte_total(db: Session = Depends(get_db), current_user: dict = Depends(obtener_usuario_actual)):
    if current_user.get("rol") != "Administrador":
        raise HTTPException(status_code=403, detail="No autorizado")
    service = SaleService(db)
    resumen = service.obtener_resumen_total()
    archivo = "reporte_historico_total.pdf"
    service.generar_pdf_reporte("Reporte Histórico Total", resumen['ventas'], resumen['total_recaudado'], archivo)
    return FileResponse(archivo, media_type='application/pdf', filename=archivo)


@router.get("/ventas")
def listar_ventas(db: Session = Depends(get_db), current_user: dict = Depends(obtener_usuario_actual)):
    # Sólo administradores pueden consultar el historial completo
    if current_user.get("rol") != "Administrador" and current_user.get("id_rol") != 1 and str(current_user.get("id_rol")) != "1":
        raise HTTPException(status_code=403, detail="No autorizado")
    service = SaleService(db)
    return service.obtener_historial_ventas()

@router.get("/ventas/diarias/{fecha}")
def obtener_ventas_diarias(fecha: date, db: Session = Depends(get_db)):
    service = SaleService(db)
    return service.obtener_resumen_diario(fecha)

@router.post("/ventas")
def realizar_venta(venta_data: dict, db: Session = Depends(get_db)):
    try:
        service = SaleService(db)
        venta = service.registrar_venta(venta_data)
        return {"message": "Venta realizada con éxito", "id_venta": venta.id_venta}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al procesar la venta")

@router.post("/ventas/calcular")
def calcular_resumen(venta: VentaRequest, db: Session = Depends(get_db)):
    try:
        service = SaleService(db)
        resumen = service.calcular_resumen_venta(venta.detalles)
        return resumen
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    