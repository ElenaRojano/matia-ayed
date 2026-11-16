"""Reto 3 · Contar piezas por caja.

    py -3 retos/reto3_cajas.py
Lee las hojas «Caja …», resuelve cada referencia (id_material o código) y cuenta
piezas por caja y unidades por material. Anota todas las incidencias.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "herramienta"))
import configuracion
from lector_excel import leer_hoja, nombres_hojas
from normalizar import normalizar_codigo, pruebas_reto2
from utiles import barras_texto, escribir_csv, guardar_texto, tabla_texto


def construir_indices(materiales):
    """Dos diccionarios: id -> material y código normalizado -> lista de materiales."""
    # TODO: Dos diccionarios. por_id[id sin espacios] = material.
    # por_codigo[código normalizado] = LISTA de materiales (para detectar códigos repetidos).
    return {}, {}


def resolver(referencia, por_id, por_codigo):
    """Devuelve (material o None, motivo). Prueba primero el id y después el código."""
    # TODO: 1) ¿Está la referencia (sin espacios) en por_id?  2) Si no, buscad su código normalizado en
    # por_codigo: 1 candidato -> ese material; varios -> ambigua; ninguno -> no existe.
    return None, "TODO: resolver sin hacer"


def cantidad_valida(texto):
    """'2' -> True ; '0', '', '-1', 'uno' -> False."""
    # TODO: Verdadero solo si, sin espacios, son todo cifras y el número es mayor que 0.
    return False


def pruebas():
    pruebas_reto2()                              # pruebas de herramienta/normalizar.py
    m = [{"id_material": "e1", "codigo_material": "QA001R"}, {"id_material": "e2", "codigo_material": " qa002r"}]
    pi, pc = construir_indices(m)
    assert resolver("e1", pi, pc)[0]["id_material"] == "e1"            # por id
    assert resolver("QA002R", pi, pc)[0]["id_material"] == "e2"        # por código normalizado
    assert resolver("QZ999R", pi, pc)[0] is None                       # ausente
    assert construir_indices([]) == ({}, {})                            # vacío
    assert cantidad_valida("2") and not cantidad_valida("0") and not cantidad_valida("") and not cantidad_valida("uno")


if __name__ == "__main__":
    pruebas()
    configuracion.comprobar()
    ruta = configuracion.RUTA_EXCEL
    materiales = leer_hoja(ruta, "Materiales")
    por_id, por_codigo = construir_indices(materiales)
    cajas_declaradas = {}
    for c in leer_hoja(ruta, "Cajas"):
        k = normalizar_codigo(c["codigo_caja"])
        cajas_declaradas[k] = cajas_declaradas.get(k, 0) + 1

    piezas_por_caja, lineas_por_caja, total_escrito = {}, {}, {}
    unidades_material, cajas_material = {}, {}
    incidencias = []                                  # (hoja, fila, caja, referencia, motivo)
    for hoja in nombres_hojas(ruta):
        if not hoja.startswith("Caja "):
            continue
        filas = leer_hoja(ruta, hoja)
        if not filas:
            incidencias.append((hoja, "", "", "", "hoja vacía"))
            continue
        caja_actual = normalizar_codigo(hoja[5:])            # si la columna viene vacía, la del nombre de la hoja
        vistas = set()
        for n, f in enumerate(filas, start=2):
            caja = normalizar_codigo(f["codigo_caja"])
            if caja == "":
                caja = caja_actual
            elif caja != f["codigo_caja"]:
                incidencias.append((hoja, n, caja, "", "código de caja con espacios o minúsculas"))
            caja_actual = caja
            ref = f["codigo_material"]
            if ref.strip() == "":
                if f["cantidad"].strip().isdigit():          # fila de TOTAL escrita a mano en la hoja
                    total_escrito[caja] = int(f["cantidad"])
                    incidencias.append((hoja, n, caja, "", "fila de total mezclada con los datos: %s" % f["cantidad"]))
                else:
                    incidencias.append((hoja, n, caja, "", "fila sin referencia de material"))
                continue
            material, motivo = resolver(ref, por_id, por_codigo)
            if material is None:
                incidencias.append((hoja, n, caja, ref, motivo))
                continue
            mid = material["id_material"]
            if (caja, mid) in vistas:
                incidencias.append((hoja, n, caja, ref, "línea repetida en la misma caja"))
            vistas.add((caja, mid))
            if not cantidad_valida(f["cantidad"]):
                incidencias.append((hoja, n, caja, ref, "cantidad no válida: %r" % f["cantidad"]))
                continue
            q = int(f["cantidad"])
            piezas_por_caja[caja] = piezas_por_caja.get(caja, 0) + q
            lineas_por_caja[caja] = lineas_por_caja.get(caja, 0) + 1
            unidades_material[mid] = unidades_material.get(mid, 0) + q
            cajas_material.setdefault(mid, set()).add(caja)

    no_declaradas = sorted(c for c in piezas_por_caja if c not in cajas_declaradas)
    repetidas = sorted(c for c, n in cajas_declaradas.items() if n > 1)
    sin_caja = [m["id_material"] for m in materiales if m["id_material"] not in unidades_material]
    motivos = {}
    for inc in incidencias:
        clave = inc[4].split(":")[0]
        motivos[clave] = motivos.get(clave, 0) + 1

    lineas = ["# Reto 3 · Piezas por caja", ""]
    lineas += tabla_texto(["Caja", "Líneas válidas", "Piezas calculadas", "Total escrito en la hoja", "¿Está en la hoja Cajas?"],
                          [[c, lineas_por_caja[c], piezas_por_caja[c], total_escrito.get(c, "—"),
                            "sí" if c in cajas_declaradas else "no"]
                           for c in sorted(piezas_por_caja, key=lambda c: -piezas_por_caja[c])])
    lineas += ["", "Total de piezas: %d · materiales en alguna caja: %d de %d · sin caja: %d" % (
        sum(piezas_por_caja.values()), len(unidades_material), len(materiales), len(sin_caja)),
        "Códigos de caja repetidos en la hoja Cajas: %s" % (", ".join(repetidas) or "ninguno"),
        "Cajas con composición que no están en la hoja Cajas: %s" % (", ".join(no_declaradas) or "ninguna"), ""]
    lineas += ["## Incidencias por motivo", ""] + tabla_texto(["Motivo", "Filas"], sorted(motivos.items(), key=lambda x: -x[1]))
    top = sorted(unidades_material.items(), key=lambda x: -x[1])[:8]
    lineas += ["", "```"] + barras_texto("Materiales con más unidades en el conjunto de cajas", top) + ["```"]
    print("\n".join(lineas))
    guardar_texto(os.path.join(configuracion.RESULTADOS, "reto3_cajas.md"), lineas)
    escribir_csv(os.path.join(configuracion.RESULTADOS, "reto3_incidencias.csv"), ["hoja", "fila", "caja", "referencia", "motivo"], incidencias)
    escribir_csv(os.path.join(configuracion.RESULTADOS, "reto3_unidades_por_material.csv"), ["id_material", "unidades", "cajas"],
                 [(mid, q, " ".join(sorted(cajas_material[mid]))) for mid, q in sorted(unidades_material.items())])
