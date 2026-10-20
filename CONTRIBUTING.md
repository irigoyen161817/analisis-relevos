# Flujo de trabajo

## Issues
- Cada unidad de trabajo es una issue con objetivo y criterios de aceptación (usar las plantillas).
- Cada issue pertenece a un milestone (fase de la hoja de ruta, F1–F8) y lleva etiquetas de tipo
  (`feature`, `bug`, `docs`, `chore`, `research`) y de área (`calibracion`, `eventos`, `metricas`,
  `deteccion`, `visualizacion`, `infra`, `datos`).
- `bloqueado-hardware` marca lo que depende de grabar en pista o comprar material.
- El estado se sigue en el tablero del Project «Relevos».

## Ramas
Una rama por issue, creada desde `main`:

```
feat/<n>-descripcion-corta
fix/<n>-descripcion-corta
docs/<n>-descripcion-corta
```

## Commits
Formato del mensaje: `[#<issue>] <descripción corta>`, en imperativo y sin punto final.

```
[#4] Mostrar los fps reales del vídeo
[#10] Calcular el error de reproyección por platillo
```

El hook `commit-msg` de pre-commit rechaza los mensajes que no siguen el formato
(se permiten los que genera git: `Merge`, `Revert`, `fixup!`, `squash!`).

## Pull requests
- El título de la PR sigue el mismo formato (`[#n] descripción`), porque con squash merge
  se convierte en el mensaje del commit en `main`.
- PRs pequeñas, contra `main`, con `Closes #n` en la descripción.
- La CI (ruff + pytest) debe estar en verde antes de mergear.
- Se mergea con **squash merge** y se borra la rama.
- No se hace push directo a `main`.

## Código
- Python >= 3.10, `ruff` para lint y formato.
- Tests con `pytest`; usar datos sintéticos (homografías, trayectorias) cuando no haya vídeos reales.
- Los vídeos y sesiones van en `data/`, fuera del repositorio.
- Usar siempre la marca de tiempo real de cada fotograma, nunca `índice / fps`.
