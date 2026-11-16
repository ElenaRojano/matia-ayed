"""MatIA · Gráficos PNG de los resultados (OPCIONAL, ya está hecho). Necesita matplotlib.

    py -3 -m pip install matplotlib        (una sola vez)
    py -3 herramienta/graficos.py          (después de los retos 3 y 5)
Lee los CSV de resultados/ y guarda los PNG en la misma carpeta.
Si no queréis instalar nada, los retos ya dibujan los gráficos con texto.
"""
import csv
import os

import matplotlib.pyplot as plt

import configuracion

AZUL, NARANJA, GRIS = "#0060AB", "#D9822B", "#C3CCD5"


def leer(nombre):
    ruta = os.path.join(configuracion.RESULTADOS, nombre)
    if not os.path.exists(ruta):
        return None
    with open(ruta, encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


def barras(etiquetas, valores, colores, titulo, eje, archivo):
    """Barras horizontales con el valor escrito al final de cada barra."""
    fig, ax = plt.subplots(figsize=(7, 0.45 * len(etiquetas) + 1.3))
    posiciones = list(range(len(etiquetas)))[::-1]          # la primera etiqueta, arriba
    ax.barh(posiciones, valores, color=colores)
    ax.set_yticks(posiciones, etiquetas)
    for y, v in zip(posiciones, valores):
        ax.text(v, y, " %d" % v, va="center")
    ax.set_xlim(0, max(valores) * 1.15 if valores and max(valores) else 1)
    ax.set_title(titulo, loc="left")
    ax.set_xlabel(eje)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(configuracion.RESULTADOS, archivo), dpi=150)
    plt.close(fig)
    print("Guardado resultados/" + archivo)


cruce = leer("reto5_cruce_por_codigo.csv")
if cruce:
    con = [f for f in cruce if f["en_archivos"] == "sí"]
    con.sort(key=lambda f: -int(f["imagenes"]))
    barras([f["codigo"] for f in con], [int(f["imagenes"]) for f in con],
           [AZUL if f["en_tabla"] == "sí" else NARANJA for f in con],
           "Imágenes por código (naranja = no está en la tabla)", "Imágenes", "g1_imagenes_por_codigo.png")
    de_tabla = [f for f in cruce if f["en_tabla"] == "sí"]
    n_con = sum(1 for f in de_tabla if f["en_archivos"] == "sí")
    barras(["Con imágenes", "Sin imágenes"], [n_con, len(de_tabla) - n_con], [AZUL, NARANJA],
           "Códigos de la tabla que aparecen en las imágenes", "Códigos", "g2_codigos_tabla.png")
unidades = leer("reto3_unidades_por_material.csv")
if unidades:
    unidades.sort(key=lambda f: -int(f["unidades"]))
    top = unidades[:10]
    barras([f["id_material"] for f in top], [int(f["unidades"]) for f in top], [GRIS] * len(top),
           "Los 10 materiales con más unidades en las cajas", "Unidades", "g3_unidades_por_material.png")
if not cruce and not unidades:
    print("No hay resultados todavía: ejecutad antes los retos 3 y 5.")
