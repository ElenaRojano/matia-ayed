# Retos MatIA

Los retos van en orden: cada uno usa lo que habéis construido en el anterior. En cada uno:

1. Leed el enunciado y **predecid** qué vais a encontrar.
2. Completad los `TODO` (el archivo os dice dónde).
3. Ejecutad: las **pruebas** (`assert`) se lanzan solas al principio. Hasta que no pasen, el reto no sigue.
4. Comparad con los **valores esperados con los datos de ejemplo**.
5. Cambiad a los **datos reales** (`config_local.py`) y anotad en el informe lo que encontréis.
6. **Commit y push** de quien haya conducido.

Ejecutad siempre desde la raíz del repositorio: `py -3 retos/retoN_….py`

---

## Reto 0 · Comprobar que todo funciona (hecho)

`py -3 retos/reto0_comprobar.py` muestra la configuración, las hojas del Excel con sus filas y los archivos de la carpeta de imágenes.
**Commit:** completad `GRUPO.md` con vuestros nombres y usuarios de GitHub.

---

## Reto 1 · Contar los elementos de la tabla de forma eficiente

**Archivo:** `retos/reto1_contar.py`

**Problema.** ¿Cuántas veces aparece cada id, cada código y cada categoría en la hoja «Materiales»? Contar parece trivial, pero el algoritmo importa: `contar_ingenuo` (ya hecho) recorre la lista entera **por cada valor distinto**.

**Diseñad:**
- `contar_diccionario(valores)`: el recuento en **una sola pasada** con un diccionario.
- `repetidos(recuento)`: los valores que aparecen más de una vez (sin contar el vacío).

**Valores esperados con los datos de ejemplo:** 19 registros · id_material: 18 distintos, repetido `ej013` · codigo_material: 17 distintos, 1 vacío, repetido `QF200R` · el recuento ingenuo hace 508 comparaciones con los ids y el diccionario, 19 pasos.

**Para el informe:** ¿cuántas comparaciones hace cada algoritmo con la tabla real? ¿Cuánto más rápido es el diccionario? ¿Por qué hay categorías «repetidas» que no son un error?

---

## Reto 2 · Depurar antes de contar

**Archivos:** `herramienta/normalizar.py` (`normalizar_codigo`, `normalizar_texto`, `es_codigo_fabricante`) y `retos/reto2_depurar.py` (`agrupar_variantes`, `parecidas`).

**Problema.** `'QC102R '`, `'qh110r'` y `'Mosquito curvo'` frente a `'MOSQUITO CURVO'`: el mismo dato escrito de formas distintas se cuenta como datos distintos. Además hay erratas (`CLAN` por `CLAMP`) que normalizar no arregla.

**Diseñad:**
- Las tres funciones de `normalizar.py`.
- `agrupar_variantes(valores, normalizar)`: qué formas originales se convierten en la misma forma normalizada (diccionario de conjuntos).
- `parecidas(textos, umbral)`: parejas de textos muy parecidos con `SequenceMatcher(None, a, b).ratio()`, contando comparaciones.

**Valores esperados con los datos de ejemplo:** cambian al normalizar `QC102R` (espacio) y `QH110R` (minúsculas) · categorías distintas: 16 antes y 14 después · variantes: `MOSQUITO CURVO` y `PINZA DISECCION` · parecidas: `CLAMP VASCULAR`–`CLAN VASCULAR` (0,89) y `TIJERA MAYO CURVA`–`TIJERAS MAYO CURVA` (0,97) · formato distinto: `8393184` · descripción repetida: ej006 y ej009.

**Para el informe:** ¿qué parejas parecidas son erratas y cuáles son instrumentos distintos (por ejemplo, «con dientes» y «sin dientes»)? ¿Quién debe decidirlo? ¿Qué erratas no puede encontrar este método?

---

## Reto 3 · Contar piezas por caja

**Archivo:** `retos/reto3_cajas.py` (`construir_indices`, `resolver`, `cantidad_valida`).

**Problema.** Cada hoja «Caja …» dice qué material lleva una caja y cuántas unidades. Pero unas líneas citan el `id_material` y otras el código, el código de caja solo está en la primera fila, hay referencias que no existen y la última fila es un **total escrito a mano**.

**Diseñad** los índices (diccionarios) y la búsqueda de cada referencia. El recorrido de las hojas ya está hecho: leedlo y explicadlo.

**Valores esperados con los datos de ejemplo:** CG-A: 8 piezas (el total escrito dice 12) · CG-B: 7 piezas (escrito: 8) · CG-A repetida en la hoja Cajas · CG-B no está en la hoja Cajas (allí pone CGB) · incidencias: 2 referencias que no existen, 2 cantidades no válidas, 2 filas de total, 1 referencia ambigua, 1 código de caja con espacios, 1 línea repetida.

**Para el informe:** ¿coincide el total escrito con la suma? Cuando no coincide, ¿qué explica la diferencia? ¿Qué materiales no están en ninguna caja?

---

## Reto 4 · Inventariar las imágenes

**Archivos:** `herramienta/listar_archivos.sh` (Bash), `codigo_de_nombre` en `herramienta/normalizar.py` y `analizar_inventario` en `retos/reto4_imagenes.py`.

```bash
bash herramienta/listar_archivos.sh datos_ejemplo/dataset_mini resultados/inventario.csv
py -3 retos/reto4_imagenes.py
```
Con los datos reales, cambiad la carpeta por la vuestra, entre comillas: `bash herramienta/listar_archivos.sh "C:/…/dataset_clean" resultados/inventario.csv`.

**Valores esperados con los datos de ejemplo:** 22 archivos y 11 imágenes · QB003R: 3 imágenes y 3 etiquetas · QH110R: 3 y 2 · QC101R: 1 y 2 · 2 imágenes sin etiqueta, 1 nombre sin patrón y 1 etiqueta sin imagen.

**Para el informe:** ¿qué códigos aparecen en los nombres? ¿Cuántas imágenes no tienen etiqueta?

---

## Reto 5 · Cruzar la tabla con las imágenes

**Archivo:** `retos/reto5_cruzar.py` (`cruzar`). Necesita el inventario del reto 4.

**Problema.** ¿Qué materiales de la tabla tienen imágenes? ¿Qué códigos de las imágenes no existen en la tabla? Es una pregunta de **conjuntos**.

**Valores esperados con los datos de ejemplo:** 17 códigos en la tabla · 6 en los nombres · 4 en los dos (QB003R, QC101R, QF200R, QH110R) · 13 de la tabla sin imágenes · IMG y NB114R no están en la tabla · 8 de 11 imágenes con un código de la tabla.

**Gráficos en PNG (opcional):** `py -3 -m pip install matplotlib` y `py -3 herramienta/graficos.py`.

---

## Reto 6 · Informe de fallos y propuestas de mejora

Completad [`INFORME_FALLOS_MEJORAS.md`](INFORME_FALLOS_MEJORAS.md) con los resultados **de los datos reales**: cada fallo con su evidencia, el número de elementos afectados, su gravedad y una propuesta de mejora que se pueda comprobar con vuestra herramienta.

Pegad solo **cifras y tablas resumen**: no copiéis filas completas del Excel del hospital.

## Ampliaciones

- Detectar los `.txt` vacíos (hay que abrirlos).
- Detectar huecos en la numeración de las fotos (`…_1_JPG`, `…_2_JPG`, `…_4_JPG`: ¿y la 3?).
- Medir con `time` cuánto tarda cada reto con los datos reales.
