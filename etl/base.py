"""Carga en PostgreSQL y consulta los resultados."""
import psycopg

TABLA = """
CREATE TABLE IF NOT EXISTS mediciones (
    fecha date, estacion text, contaminante text, valor numeric NOT NULL,
    PRIMARY KEY (fecha, estacion, contaminante)
)"""


def cargar(url, filas):
    """Devuelve cuántas filas había antes. Repetir la carga no duplica datos."""
    with psycopg.connect(url) as con:
        con.execute(TABLA)
        previas = con.execute("SELECT count(*) FROM mediciones").fetchone()[0]
        with con.cursor() as cur:
            cur.executemany(
                "INSERT INTO mediciones VALUES (%s, %s, %s, %s) "
                "ON CONFLICT (fecha, estacion, contaminante) "
                "DO UPDATE SET valor = EXCLUDED.valor",
                filas,
            )
    return previas


def resumen(url, estacion=None):
    with psycopg.connect(url) as con:
        return con.execute(
            "SELECT estacion, contaminante, count(*), round(avg(valor), 1), max(valor) "
            "FROM mediciones WHERE %s::text IS NULL OR estacion = %s "
            "GROUP BY estacion, contaminante ORDER BY estacion, contaminante",
            (estacion, estacion),
        ).fetchall()
