"""MatIA · Utilidades para presentar resultados. NO hace falta modificarlo.

    pct(1, 3)                         -> '33,3 %'
    tabla_texto(cabecera, filas)      -> líneas de una tabla Markdown
    barras_texto(titulo, pares)       -> líneas de un gráfico de barras con caracteres
    escribir_csv(ruta, cabecera, filas)
    guardar_texto(ruta, lineas)       -> guarda las líneas en un archivo .md o .txt
"""
import csv
import sys

# En Windows la terminal no siempre usa UTF-8: sin esta línea, las barras y las tildes dan error.
sys.stdout.reconfigure(encoding="utf-8")


def pct(parte, total):
    """Porcentaje con coma decimal."""
    valor = round(100 * parte / total, 1) if total else 0.0
    return str(valor).replace(".", ",") + " %"


def tabla_texto(cabecera, filas):
    """Tabla Markdown: se lee bien en la terminal y se pega tal cual en el informe."""
    lineas = ["| " + " | ".join(str(c) for c in cabecera) + " |", "|" + "---|" * len(cabecera)]
    for f in filas:
        lineas.append("| " + " | ".join(str(v) for v in f) + " |")
    return lineas


def barras_texto(titulo, pares, ancho=40):
    """Gráfico de barras con caracteres. pares = [(etiqueta, valor), ...]."""
    lineas = [titulo]
    maximo = 0
    for _, v in pares:
        if v > maximo:
            maximo = v
    for etiqueta, v in pares:
        largo = round(ancho * v / maximo) if maximo else 0
        lineas.append("  %-34s %s %d" % (str(etiqueta)[:34], "█" * largo, v))
    return lineas


def escribir_csv(ruta, cabecera, filas):
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        w = csv.writer(archivo)
        w.writerow(cabecera)
        for f in filas:
            w.writerow(f)


def guardar_texto(ruta, lineas):
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")


assert pct(1, 3) == "33,3 %" and pct(0, 0) == "0,0 %"
assert tabla_texto(["a"], [[1]]) == ["| a |", "|---|", "| 1 |"]
