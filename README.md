# MatIA · Datos de instrumental quirúrgico con Python y Bash

Algoritmos y estructura de datos · 2.º Grado en Computación e Inteligencia Artificial · UAX Mare Nostrum · ULAB MatIA

El proyecto MatIA quiere contar el instrumental quirúrgico a partir de fotos. Antes de entrenar ningún modelo hay que **entender y depurar los datos**: la tabla de materiales del hospital (un Excel) y las imágenes con sus etiquetas. La tabla no está depurada y no todo coincide con las imágenes.

En este repositorio construiréis, reto a reto, una herramienta que **cuenta, depura y cruza** esos datos, y terminaréis con un **informe de fallos y propuestas de mejora**.

## Cómo se trabaja

1. **Una persona por grupo** (3 personas) hace **fork** de este repositorio y añade a sus dos compañeros como colaboradores. Guía paso a paso: [`docs/FORK_Y_GIT.md`](docs/FORK_Y_GIT.md).
2. Las tres personas **clonan el fork del grupo** (no este repositorio).
3. Completad **`GRUPO.md`** con vuestros nombres: será vuestro primer commit.
4. Seguid los retos en orden: [`docs/RETOS.md`](docs/RETOS.md).

## Puesta en marcha

```bash
git clone URL_DEL_FORK_DEL_GRUPO
cd matia-ayed
py -3 retos/reto0_comprobar.py          # macOS/Linux: python3 retos/reto0_comprobar.py
```

Funciona desde el primer momento con los **datos de ejemplo inventados** de `datos_ejemplo/`. Solo necesita Python 3 (biblioteca estándar) y Git Bash.

## Datos reales: nunca en GitHub

El Excel del hospital está en el **campus virtual** y las imágenes, en vuestro ordenador. Para usarlos:

```bash
cp config_ejemplo.py config_local.py     # y editad las dos rutas de config_local.py
py -3 retos/reto0_comprobar.py           # debe decir: config_local.py (datos reales)
```

`config_local.py`, los archivos Excel y la carpeta `resultados/` están en `.gitignore`: **no se suben**. Antes de cada `git add`, comprobad con `git status` que no aparece ninguno.

## Estructura

```
herramienta/   lector_excel.py, configuracion.py, utiles.py, graficos.py   (hechos: no hace falta tocarlos)
               normalizar.py, listar_archivos.sh                          (los completáis en los retos 2 y 4)
retos/         reto0_comprobar.py (hecho) · reto1 … reto5 (con TODO)
docs/          RETOS.md · FORK_Y_GIT.md · INFORME_FALLOS_MEJORAS.md
datos_ejemplo/ Excel e imágenes inventados para programar y probar
resultados/    lo que generan los retos (no se sube)
```

## Normas

- Bucles explícitos, una idea por función y `assert` de **presente, ausente y vacío**.
- Cada reto se cierra con un **commit** de quien ha escrito el código en ese turno.
- Pide a la IA que te **explique**, no que te **resuelva**. Y **nunca le pases datos del hospital**.
