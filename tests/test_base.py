import os
from datetime import date

import pytest

from etl.base import cargar, resumen

URL = os.environ.get("DATABASE_URL")
pytestmark = pytest.mark.skipif(not URL, reason="sin DATABASE_URL")


def test_repetir_la_carga_no_duplica():
    filas = [(date(2026, 1, 1), "Prueba", "NO2", 10), (date(2026, 1, 2), "Prueba", "NO2", 20)]
    cargar(URL, filas)
    cargar(URL, filas)
    assert resumen(URL, "Prueba") == [("Prueba", "NO2", 2, 15, 20)]
