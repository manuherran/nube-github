from etl.limpieza import leer, limpiar


def fila(fecha="2026-11-01", valor="40"):
    return {"fecha": fecha, "estacion": "Norte", "contaminante": "NO2", "valor": valor}


def test_acepta_fila_correcta():
    assert len(limpiar([fila()])[0]) == 1


def test_rechaza_con_motivo():
    malas = [fila(fecha="08/11/2026"), fila(valor=""), fila(valor="-5")]
    assert [m for _, m in limpiar(malas)[1]] == [
        "fecha no válida", "valor no numérico", "valor fuera de rango"]


def test_rechaza_duplicadas():
    validas, rechazadas = limpiar([fila(), fila()])
    assert len(validas) == 1 and rechazadas == [(3, "duplicada")]


def test_fichero_del_repositorio():
    validas, rechazadas = leer("datos/mediciones.csv")
    assert len(validas) == 42 and len(rechazadas) == 5
