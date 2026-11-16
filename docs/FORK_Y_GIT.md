# Fork y Git para trabajar en grupo

## ¿Qué es un fork y para qué sirve?

Un **fork** es una **copia de un repositorio de GitHub en tu cuenta**, que recuerda de dónde viene.

```
repositorio de la docente  ──fork──▶  fork del grupo (en la cuenta de la persona responsable)
     (solo lectura)                         │
                                            ├──clone──▶ ordenador de la persona 1
                                            ├──clone──▶ ordenador de la persona 2
                                            └──clone──▶ ordenador de la persona 3
```

- **No podéis escribir** en el repositorio de la docente; en vuestro fork, sí.
- Cada grupo tiene **su propio fork**: los grupos no se pisan entre sí.
- El fork sigue **conectado** al original: si la docente publica una corrección, la traéis con **Sync fork**.
- La docente ve vuestro trabajo (y quién ha hecho cada commit) entrando en vuestro fork.

**Solo una persona por grupo hace el fork.** Las otras dos trabajan en ese mismo fork como colaboradoras.

## Paso a paso

### Persona responsable (5 minutos)

1. Abre el repositorio de la docente en GitHub y pulsa **Fork** (arriba a la derecha).
2. *Owner*: tu cuenta. *Repository name*: `matia-ayed`. Pulsa **Create fork**.
3. En **tu** fork: **Settings → Collaborators → Add people**. Añade a tus dos compañeros y a la docente.

### Compañeros

4. Aceptad la invitación (correo o la campana de notificaciones de GitHub).

### Las tres personas

```bash
git clone URL_DEL_FORK_DEL_GRUPO        # la URL del fork, NO la del repositorio de la docente
cd matia-ayed
git remote -v                           # origin debe ser el fork del grupo
py -3 retos/reto0_comprobar.py
```

Después de `git clone` **no** ejecutéis `git init` ni `git remote add`.

## Trabajar los tres sin conflictos: turnos

Todo el grupo trabaja en los mismos archivos, así que **solo teclea una persona cada vez**. Los papeles rotan en cada reto:

| Papel | Qué hace |
|---|---|
| Conductor | Teclea el código del reto |
| Copiloto | Razona en voz alta qué hay que escribir y vigila los errores |
| Revisor | Escribe y comprueba los `assert`, y compara con los valores esperados |

Al terminar cada reto, el **conductor**:

```bash
git status                              # NO debe aparecer el Excel, config_local.py ni resultados/
git add herramienta/ retos/ docs/ GRUPO.md
git commit -m "Reto 1: recuento con diccionario"
git push
```

El siguiente conductor, **antes de teclear**:

```bash
git pull
```

Si `git push` se rechaza: `git pull` y otra vez `git push`. Si aparece un conflicto, no borréis nada y avisad a la docente.

## Traer las novedades de la docente (Sync fork)

1. En la página de **vuestro fork**, pulsad **Sync fork → Update branch**.
2. En cada ordenador: `git pull`.
