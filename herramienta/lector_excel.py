"""MatIA · Lector de archivos Excel (.xlsx) con la biblioteca estándar. NO hace falta modificarlo.

Un .xlsx es un archivo ZIP con varios XML dentro. Este módulo lo abre con zipfile y lee
las celdas con xml.etree. Así no hay que instalar nada ni exportar a CSV a mano.

    from lector_excel import nombres_hojas, leer_hoja
    nombres_hojas("datos.xlsx")                  # ['Materiales', 'Cajas', ...]
    filas = leer_hoja("datos.xlsx", "Materiales") # lista de diccionarios, una fila por diccionario

Importante: todos los valores se devuelven como TEXTO, tal y como están guardados.
- Una celda vacía es "".
- Un número entero se guarda como "8393184" (sin decimales).
- Una fecha se guarda como un número de días (por ejemplo "46252"): Excel cuenta días desde 1900.
- Una columna sin nombre en la cabecera se llama "columna_N" (N = su posición, empezando en 1).
"""
import xml.etree.ElementTree as ET
import zipfile

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "p": "http://schemas.openxmlformats.org/package/2006/relationships"}


def _letras_a_numero(referencia):
    """'A1' -> 0, 'C7' -> 2, 'AA3' -> 26: posición de la columna, empezando en 0."""
    numero = 0
    for letra in referencia:
        if letra.isalpha():
            numero = numero * 26 + (ord(letra.upper()) - ord("A") + 1)
        else:
            break
    return numero - 1


def _texto(elemento):
    """Junta el texto de todas las etiquetas <t> de un elemento (una celda puede tener varias)."""
    partes = []
    for t in elemento.iter("{%s}t" % NS["m"]):
        partes.append(t.text or "")
    return "".join(partes)


def _rutas_hojas(libro):
    """Diccionario nombre de hoja -> ruta del XML dentro del ZIP."""
    workbook = ET.fromstring(libro.read("xl/workbook.xml"))
    rels = ET.fromstring(libro.read("xl/_rels/workbook.xml.rels"))
    destino = {}
    for r in rels.findall("p:Relationship", NS):
        objetivo = r.get("Target").lstrip("/")
        if not objetivo.startswith("xl/"):
            objetivo = "xl/" + objetivo
        destino[r.get("Id")] = objetivo
    rutas = {}
    for hoja in workbook.find("m:sheets", NS):
        rutas[hoja.get("name")] = destino[hoja.get("{%s}id" % NS["r"])]
    return rutas


def nombres_hojas(ruta_excel):
    """Lista con los nombres de las hojas, en el orden del libro."""
    with zipfile.ZipFile(ruta_excel) as libro:
        return list(_rutas_hojas(libro))


def leer_filas(ruta_excel, nombre_hoja):
    """Lista de listas: todas las filas de la hoja, como texto, incluida la cabecera."""
    with zipfile.ZipFile(ruta_excel) as libro:
        compartidos = []
        if "xl/sharedStrings.xml" in libro.namelist():
            for si in ET.fromstring(libro.read("xl/sharedStrings.xml")).findall("m:si", NS):
                compartidos.append(_texto(si))
        rutas = _rutas_hojas(libro)
        if nombre_hoja not in rutas:
            raise KeyError("No existe la hoja %r. Hojas: %s" % (nombre_hoja, list(rutas)))
        hoja = ET.fromstring(libro.read(rutas[nombre_hoja]))
    filas = []
    for fila in hoja.iter("{%s}row" % NS["m"]):
        valores = {}
        for celda in fila.findall("m:c", NS):
            tipo = celda.get("t")
            v = celda.find("m:v", NS)
            if tipo == "s":                                   # texto compartido
                valor = compartidos[int(v.text)]
            elif tipo == "inlineStr":                         # texto dentro de la celda
                valor = _texto(celda)
            elif v is None:                                   # celda vacía con formato
                valor = ""
            else:                                             # número, fórmula o booleano
                valor = v.text or ""
                if valor.endswith(".0"):
                    valor = valor[:-2]
            valores[_letras_a_numero(celda.get("r"))] = valor
        if valores:
            ancho = max(valores) + 1
            filas.append([valores.get(i, "") for i in range(ancho)])
        else:
            filas.append([])
    return filas


def leer_hoja(ruta_excel, nombre_hoja):
    """Lista de diccionarios: la primera fila es la cabecera. Las filas vacías se ignoran."""
    filas = leer_filas(ruta_excel, nombre_hoja)
    if not filas:
        return []
    cabecera = []
    for i, nombre in enumerate(filas[0]):
        cabecera.append(nombre.strip() if nombre.strip() else "columna_%d" % (i + 1))
    resultado = []
    for fila in filas[1:]:
        if all(str(v).strip() == "" for v in fila):
            continue
        registro = {}
        for i, nombre in enumerate(cabecera):
            registro[nombre] = fila[i] if i < len(fila) else ""
        resultado.append(registro)
    return resultado


assert _letras_a_numero("A1") == 0
assert _letras_a_numero("C7") == 2
assert _letras_a_numero("AA3") == 26

if __name__ == "__main__":
    import sys
    ruta = sys.argv[1]
    for nombre in nombres_hojas(ruta):
        print(nombre, "->", len(leer_hoja(ruta, nombre)), "filas")
