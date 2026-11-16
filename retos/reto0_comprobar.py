"""Reto 0 · Comprobar que todo funciona. YA ESTÁ HECHO: solo hay que ejecutarlo.

Desde la raíz del repositorio:
    Windows (Git Bash): py -3 retos/reto0_comprobar.py
    macOS/Linux:        python3 retos/reto0_comprobar.py
"""
import os
import sys

# Los módulos comunes están en la carpeta herramienta/: le decimos a Python que busque también allí.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "herramienta"))

import configuracion
from lector_excel import leer_hoja, nombres_hojas

configuracion.comprobar()
print()
print("Hojas del Excel:")
for nombre in nombres_hojas(configuracion.RUTA_EXCEL):
    print("  %-28s %4d filas" % (nombre, len(leer_hoja(configuracion.RUTA_EXCEL, nombre))))
print()
archivos = 0
for raiz, carpetas, ficheros in os.walk(configuracion.RUTA_IMAGENES):
    archivos += len(ficheros)
print("Archivos en la carpeta de imágenes:", archivos)
print()
print("Todo listo. Siguiente paso: docs/RETOS.md, reto 1.")
