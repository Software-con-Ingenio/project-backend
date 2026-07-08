import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from services.sale_service import SaleService


def test_calcular_resumen_venta_correcto():
    juego = SimpleNamespace(
        id_juego=1,
        nombre="Gears of War 3",
        precio=70000
    )

    db = Mock()
    db.query.return_value.filter.return_value.first.return_value = juego

    service = SaleService(db)

    item = SimpleNamespace(
        id_juego=1,
        cantidad=2
    )

    resultado = service.calcular_resumen_venta([item])

    assert resultado["total_a_pagar"] == 140000.0
    assert resultado["items"][0]["nombre"] == "Gears of War 3"
    assert resultado["items"][0]["subtotal"] == 140000.0


def test_calcular_resumen_varios_juegos():
    gears = SimpleNamespace(
        id_juego=1,
        nombre="Gears of War 3",
        precio=70000
    )

    minecraft = SimpleNamespace(
        id_juego=2,
        nombre="Minecraft",
        precio=50000
    )

    db = Mock()

    db.query.return_value.filter.return_value.first.side_effect = [
        gears,
        minecraft
    ]

    service = SaleService(db)

    items = [
        SimpleNamespace(id_juego=1, cantidad=2),
        SimpleNamespace(id_juego=2, cantidad=1)
    ]

    resultado = service.calcular_resumen_venta(items)

    assert resultado["total_a_pagar"] == 190000.0


def test_calcular_resumen_juego_no_existente():
    db = Mock()
    db.query.return_value.filter.return_value.first.return_value = None

    service = SaleService(db)

    item = SimpleNamespace(
        id_juego=999,
        cantidad=1
    )

    with pytest.raises(ValueError):
        service.calcular_resumen_venta([item])
        
        
        
def test_registrar_venta_sin_detalles():
    db = Mock()

    service = SaleService(db)

    data = {
        "id_usuario": 1,
        "detalles": []
    }

    with pytest.raises(ValueError, match="La venta debe tener al menos un detalle"):
        service.registrar_venta(data)


def test_registrar_venta_juego_no_existe():
    db = Mock()

    db.query.return_value.filter.return_value.first.return_value = None

    service = SaleService(db)

    data = {
        "id_usuario": 1,
        "detalles": [
            {
                "id_juego": 999,
                "cantidad": 1
            }
        ]
    }

    with pytest.raises(ValueError, match="no existe"):
        service.registrar_venta(data)


def test_registrar_venta_correcta():
    juego = SimpleNamespace(
        id_juego=1,
        nombre="Gears of War 3",
        precio=100,
        stock_local=10
    )

    db = Mock()

    db.query.return_value.filter.return_value.first.return_value = juego

    service = SaleService(db)

    service.sale_repo.crear_venta = Mock()
    service.sale_repo.crear_detalle = Mock()

    data = {
        "id_usuario": 1,
        "detalles": [
            {
                "id_juego": 1,
                "cantidad": 2
            }
        ]
    }

    service.registrar_venta(data)

    assert juego.stock_local == 8

    service.sale_repo.crear_venta.assert_called_once()
    service.sale_repo.crear_detalle.assert_called_once()
    
    
def test_obtener_resumen_diario():
    from datetime import date
    from types import SimpleNamespace

    db = Mock()
    service = SaleService(db)

    venta1 = SimpleNamespace(
        id_venta=1,
        total=100,
        fecha=date(2025, 6, 1)
    )

    venta2 = SimpleNamespace(
        id_venta=2,
        total=200,
        fecha=date(2025, 6, 1)
    )

    service.sale_repo.obtener_ventas_por_fecha = Mock(
        return_value=[venta1, venta2]
    )

    resultado = service.obtener_resumen_diario(
        date(2025, 6, 1)
    )

    assert resultado["cantidad_ventas"] == 2
    assert resultado["total_recaudado"] == 300.0
    assert len(resultado["ventas"]) == 2