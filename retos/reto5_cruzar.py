"""Reto 5 · Cruzar la tabla con las imágenes.

    py -3 retos/reto5_cruzar.py            (necesita resultados/inventario.csv del reto 4)
Compara los códigos de la hoja Materiales con los códigos de los nombres de archivo usando conjuntos,
y genera las tablas y gráficos del diagnóstico.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "herramienta"))
import configuracion
from lector_excel import leer_hoja
from normalizar import normalizar_codigo
from reto4_imagenes import analizar_inventario, leer_inventario
from utiles import barras_texto, escribir_csv, guardar_texto, pct, tabla_texto


def cruzar(codigos_tabla, codigos_archivo):
    """Devuelve (en_ambos, solo_tabla, solo_archivos) como listas ordenadas."""
    # TODO: Con operaciones de conjuntos: & (en los dos) y - (solo en uno). Devolved listas ordenadas.
    return [], [], []


def pruebas():
    assert cruzar({"A", "B"}, {"B", "C"}) == (["B"], ["A"], ["C"])
    assert cruzar({"A"}, set()) == ([], ["A"], [])
    assert cruzar(set(), set()) == ([], [], [])


if __name__ == "__main__":
    pruebas()
    configuracion.comprobar()
    materiales = leer_hoja(configuracion.RUTA_EXCEL, "Materiales")
    indice = {}
    for m in materiales:
        c = normalizar_codigo(m["codigo_material"])
        if c != "":
            indice.setdefault(c, m)
    img, eti, split, problemas = analizar_inventario(leer_inventario())
    en_ambos, solo_tabla, solo_archivos = cruzar(set(indice), set(img) | set(eti))
    n_img = sum(split.values())
    img_conectadas = sum(img.get(c, 0) for c in en_ambos)

    filas = []
    for c in sorted(set(indice) | set(img) | set(eti)):
        m = indice.get(c, {})
        fotos = m.get("fotos", "").strip()
        filas.append([c, "sí" if c in indice else "no", "sí" if c in img or c in eti else "no",
                      m.get("id_material", ""), " ".join(m.get("Descripcion_material", "").split())[:50],
                      fotos, img.get(c, 0), eti.get(c, 0)])
    escribir_csv(os.path.join(configuracion.RESULTADOS, "reto5_cruce_por_codigo.csv"),
                 ["codigo", "en_tabla", "en_archivos", "id_material", "descripcion", "fotos_segun_tabla", "imagenes", "etiquetas"], filas)

    lineas = ["# Reto 5 · Tabla frente a imágenes", ""]
    lineas += tabla_texto(["Indicador", "Valor", "%"], [
        ["Códigos distintos en la tabla", len(indice), ""],
        ["Códigos distintos en los nombres de archivo", len(set(img) | set(eti)), ""],
        ["Códigos en los dos", len(en_ambos), pct(len(en_ambos), len(indice))],
        ["Códigos de la tabla sin ninguna imagen", len(solo_tabla), pct(len(solo_tabla), len(indice))],
        ["Códigos de los nombres que no están en la tabla", len(solo_archivos), ""],
        ["Imágenes", n_img, ""],
        ["Imágenes cuyo código está en la tabla", img_conectadas, pct(img_conectadas, n_img)],
    ])
    lineas += ["", "Códigos en los dos: " + (", ".join(en_ambos) or "—"),
               "Códigos de los nombres que no están en la tabla: " + (", ".join(solo_archivos) or "—"), ""]
    lineas += tabla_texto(["Código del nombre", "¿En la tabla?", "Imágenes", "Fotos según la tabla"],
                          [[f[0], f[1], f[6], f[5] or "—"] for f in filas if f[2] == "sí"])
    lineas += ["", "```"]
    lineas += barras_texto("Códigos de la tabla", [("con imágenes", len(en_ambos)), ("sin imágenes", len(solo_tabla))])
    lineas += [""] + barras_texto("Imágenes", [("con código de la tabla", img_conectadas), ("sin código de la tabla", n_img - img_conectadas)])
    lineas += ["```"]
    print("\n".join(lineas))
    guardar_texto(os.path.join(configuracion.RESULTADOS, "reto5_cruce.md"), lineas)
