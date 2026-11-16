#!/usr/bin/env bash
# MatIA · Paso 1: inventario de NOMBRES de archivo de un directorio.
#
# Uso:   bash herramienta/listar_archivos.sh DIRECTORIO [SALIDA.csv]
# Ej.:   bash herramienta/listar_archivos.sh dataset_nombres resultados/inventario.csv
#
# Debe escribir un CSV con una fila por archivo:
#   carpeta,subcarpeta,nombre,base,extension
# Ejemplo de fila:
#   train,images,0b18-NB114R_18_JPG.rf.XYZ.JPG,0b18-NB114R_18_JPG.rf.XYZ,JPG

DIRECTORIO="$1"
SALIDA="${2:-resultados/inventario.csv}"      # si no se indica salida, usa esta

# 1. Comprobaciones
if [ -z "$DIRECTORIO" ]; then
    echo "Uso: bash herramienta/listar_archivos.sh DIRECTORIO [SALIDA.csv]"
    exit 1
fi
# TODO 1: si "$DIRECTORIO" no es una carpeta ([ ! -d … ]), avisa y termina con exit 1
mkdir -p "$(dirname "$SALIDA")"

# 2. Cabecera del CSV
echo "carpeta,subcarpeta,nombre,base,extension" > "$SALIDA"

# 3. Una fila por archivo. Recortes de texto de Bash (no lanzan programas, son rápidos):
#    ${var##*/}  lo que va después de la última /      ${var%/*}  lo que va antes de la última /
#    ${var##*.}  lo que va después del último punto    ${var%.*}  lo que va antes del último punto
#    ${var#"$DIRECTORIO"/}  quita el directorio del principio   ${var%%/*}  lo que va antes de la primera /
find "$DIRECTORIO" -type f | sort | while read -r ruta; do
    nombre=${ruta##*/}
    carpeta_archivo=${ruta%/*}
    subcarpeta=""      # TODO 2: el nombre de la carpeta donde está el archivo (images, labels…)
    relativa=${ruta#"$DIRECTORIO"/}
    carpeta=""         # TODO 3: la primera carpeta de la ruta relativa (train, valid, test)
    extension=""       # TODO 4
    base=""            # TODO 5: el nombre sin la extensión
    echo "$carpeta,$subcarpeta,$nombre,$base,$extension" >> "$SALIDA"
done

# 4. Resumen en la terminal
total=$(($(wc -l < "$SALIDA") - 1))
echo "Inventario guardado en $SALIDA ($total archivos)"
echo
echo "Archivos por extensión:"
# TODO 6: tail -n +2 (sin cabecera) | cut -d, -f5 (columna 5) | sort | uniq -c | sort -rn
echo
echo "Archivos por carpeta y subcarpeta:"
# TODO 7: lo mismo con las columnas 1 y 2
