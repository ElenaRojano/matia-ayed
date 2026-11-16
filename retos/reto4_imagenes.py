"""Reto 4 · Inventariar las imágenes y contarlas por código.

Primero el inventario con Bash, después el recuento con Python:
    bash herramienta/listar_archivos.sh "RUTA_IMAGENES" resultados/inventario.csv
    py -3 retos/reto4_imagenes.py
"""
import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "herramienta"))
import configuracion
from normalizar import codigo_de_nombre, pruebas_reto4
from utiles import barras_texto, escribir_csv, guardar_texto, tabla_texto

RUTA_INVENTARIO = os.path.join(configuracion.RESULTADOS, "inventario.csv")
EXT_IMAGEN = {"JPG", "JPEG", "PNG"}


def leer_inventario(ruta=RUTA_INVENTARIO):
    if not os.path.exists(ruta):
        raise SystemExit("No existe %s. Ejecutad antes: bash herramienta/listar_archivos.sh RUTA resultados/inventario.csv" % ruta)
    with open(ruta, encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


def analizar_inventario(inventario):
    """Recuento de imágenes y etiquetas por código, parejas y problemas de nombre."""
    # TODO: Para cada archivo a del inventario:
    #   - imagen: extensión en EXT_IMAGEN y subcarpeta 'images' -> añadid (carpeta, base) a bases_imagen
    #   - etiqueta: extensión TXT y subcarpeta 'labels' -> añadid (carpeta, base) a bases_etiqueta
    #   - el resto, ignoradlo
    #   - codigo_de_nombre(base): si es '', anotad el problema; si no, sumad 1 en su diccionario
    # Después, con diferencias de conjuntos: imágenes sin etiqueta y etiquetas sin imagen.
    return {}, {}, {}, []


def pruebas():
    pruebas_reto4()                              # pruebas de herramienta/normalizar.py
    inv = [{"carpeta": "train", "subcarpeta": "images", "nombre": "h-QA001R_1_JPG.JPG", "base": "h-QA001R_1_JPG", "extension": "JPG"},
           {"carpeta": "train", "subcarpeta": "labels", "nombre": "h-QA001R_1_JPG.txt", "base": "h-QA001R_1_JPG", "extension": "txt"},
           {"carpeta": "train", "subcarpeta": "images", "nombre": "suelta.JPG", "base": "suelta", "extension": "JPG"}]
    img, eti, split, prob = analizar_inventario(inv)
    assert img == {"QA001R": 1} and eti == {"QA001R": 1}                # presente
    assert img.get("QZ999R", 0) == 0                                    # ausente
    assert ("train", "suelta", "imagen sin etiqueta .txt") in prob      # imagen sin pareja
    assert analizar_inventario([]) == ({}, {}, {}, [])                  # vacío


if __name__ == "__main__":
    pruebas()
    configuracion.comprobar()
    inventario = leer_inventario()
    img, eti, split, problemas = analizar_inventario(inventario)
    motivos = {}
    for p in problemas:
        motivos[p[2]] = motivos.get(p[2], 0) + 1
    lineas = ["# Reto 4 · Imágenes por código", "",
              "Archivos en el inventario: %d · imágenes: %d" % (len(inventario), sum(split.values())), ""]
    lineas += tabla_texto(["Código del nombre", "Imágenes", "Etiquetas"],
                          [[c, img.get(c, 0), eti.get(c, 0)] for c in sorted(set(img) | set(eti), key=lambda c: -img.get(c, 0))])
    lineas += ["", "Imágenes por carpeta: " + " · ".join("%s %d" % (s, n) for s, n in sorted(split.items())), ""]
    lineas += tabla_texto(["Problema", "Archivos"], sorted(motivos.items(), key=lambda x: -x[1]) or [["—", 0]])
    lineas += ["", "```"] + barras_texto("Imágenes por código", sorted(img.items(), key=lambda x: -x[1])) + ["```"]
    print("\n".join(lineas))
    guardar_texto(os.path.join(configuracion.RESULTADOS, "reto4_imagenes.md"), lineas)
    escribir_csv(os.path.join(configuracion.RESULTADOS, "reto4_problemas_archivos.csv"), ["carpeta", "archivo", "motivo"], problemas)
