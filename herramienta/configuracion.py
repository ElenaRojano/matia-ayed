"""MatIA · Configuración: dónde están el Excel y las imágenes. NO hace falta modificarlo.

Busca en la raíz del repositorio:
  1. config_local.py   -> vuestras rutas a los datos REALES (Git lo ignora: no se sube nunca)
  2. config_ejemplo.py -> los datos de ejemplo inventados que vienen con el repositorio
Para trabajar con los datos reales: copiad config_ejemplo.py como config_local.py y cambiad las rutas.
"""
import importlib.util
import os
import sys

# En Windows la terminal no siempre usa UTF-8: sin esta línea, las tildes y las barras dan error.
sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
RESULTADOS = os.path.join(RAIZ, "resultados")


def _cargar(nombre):
    ruta = os.path.join(RAIZ, nombre + ".py")
    if not os.path.exists(ruta):
        return None
    especificacion = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)
    return modulo


def _ruta(valor):
    """Las rutas relativas se entienden desde la raíz del repositorio."""
    return valor if os.path.isabs(valor) else os.path.join(RAIZ, valor)


_config = _cargar("config_local")
ORIGEN = "config_local.py (datos reales)"
if _config is None:
    _config = _cargar("config_ejemplo")
    ORIGEN = "config_ejemplo.py (datos de EJEMPLO inventados)"

RUTA_EXCEL = _ruta(_config.RUTA_EXCEL)
RUTA_IMAGENES = _ruta(_config.RUTA_IMAGENES)
os.makedirs(RESULTADOS, exist_ok=True)


def comprobar():
    """Avisa con un mensaje claro si alguna ruta no existe."""
    print("Configuración:", ORIGEN)
    print("  Excel:   ", RUTA_EXCEL)
    print("  Imágenes:", RUTA_IMAGENES)
    errores = []
    if not os.path.isfile(RUTA_EXCEL):
        errores.append("No existe el Excel: " + RUTA_EXCEL)
    if not os.path.isdir(RUTA_IMAGENES):
        errores.append("No existe la carpeta de imágenes: " + RUTA_IMAGENES)
    if errores:
        for e in errores:
            print("ERROR:", e)
        print("Revisad las rutas de config_local.py (o borradlo para usar los datos de ejemplo).")
        raise SystemExit(1)
