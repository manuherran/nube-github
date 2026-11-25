"""CSV -> limpieza -> PostgreSQL -> index.html y resumen.json.

Variables: DATABASE_URL (obligatoria), ESTACION, EJECUCION y SALIDA (opcionales).
"""
import json
import os
from datetime import datetime, timezone
from html import escape
from pathlib import Path

from etl.base import cargar, resumen
from etl.limpieza import leer


def pagina(filas, rechazadas, ejecucion, momento):
    celdas = "".join(
        "<tr>" + "".join(f"<td>{escape(str(c))}</td>" for c in fila) + "</tr>"
        for fila in filas
    )
    malas = "".join(f"<li>Línea {n}: {escape(m)}</li>" for n, m in rechazadas)
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Calidad del aire</title>
<style>body{{font-family:sans-serif;max-width:48rem;margin:2rem auto;padding:0 1rem}}
table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #bbb;padding:.4rem;text-align:left}}</style>
</head><body><h1>Calidad del aire (datos ficticios)</h1>
<p>Ejecución {escape(ejecucion)} · {momento}</p>
<table><tr><th>Estación</th><th>Contaminante</th><th>Mediciones</th><th>Media</th><th>Máximo</th></tr>{celdas}</table>
<h2>Filas rechazadas</h2><ul>{malas}</ul></body></html>
"""


def main():
    url = os.environ["DATABASE_URL"]
    estacion = os.environ.get("ESTACION") or None
    ejecucion = os.environ.get("EJECUCION") or "local"
    salida = Path(os.environ.get("SALIDA") or "salida")
    momento = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    validas, rechazadas = leer("datos/mediciones.csv")
    previas = cargar(url, validas)
    filas = resumen(url, estacion)
    if not filas:
        raise SystemExit(f"No hay datos para la estación {estacion!r}")

    salida.mkdir(parents=True, exist_ok=True)
    (salida / "index.html").write_text(
        pagina(filas, rechazadas, ejecucion, momento), encoding="utf-8")
    (salida / "resumen.json").write_text(
        json.dumps(filas, default=str, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Filas previas en la base: {previas}")
    print(f"Filas válidas: {len(validas)}")
    print(f"Filas rechazadas: {len(rechazadas)}")
    print(f"Filas del resumen: {len(filas)}")


if __name__ == "__main__":
    main()
