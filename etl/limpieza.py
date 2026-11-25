"""Lee el CSV y separa las filas válidas de las rechazadas."""
import csv
import math
from datetime import date


def limpiar(filas):
    validas, rechazadas, vistas = [], [], set()
    for numero, fila in enumerate(filas, start=2):  # la línea 1 es la cabecera
        try:
            dia = date.fromisoformat(fila["fecha"])
        except ValueError:
            rechazadas.append((numero, "fecha no válida"))
            continue
        try:
            valor = float(fila["valor"])
        except ValueError:
            rechazadas.append((numero, "valor no numérico"))
            continue
        if not math.isfinite(valor) or valor < -10:
            rechazadas.append((numero, "valor fuera de rango"))
            continue
        clave = (dia, fila["estacion"], fila["contaminante"])
        if clave in vistas:
            rechazadas.append((numero, "duplicada"))
            continue
        vistas.add(clave)
        validas.append((*clave, valor))
    return validas, rechazadas


def leer(ruta):
    with open(ruta, encoding="utf-8", newline="") as f:
        return limpiar(csv.DictReader(f))
