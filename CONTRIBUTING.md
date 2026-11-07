# Flujo de trabajo

## Issues
- Cada unidad de trabajo es una issue con objetivo y criterios de aceptación (usar las plantillas).
- Cada issue pertenece a un milestone (fase de la hoja de ruta, F1–F8) y lleva etiquetas de tipo
  (`feature`, `bug`, `docs`, `chore`, `research`) y de área (`calibracion`, `eventos`, `metricas`,
  `deteccion`, `visualizacion`, `infra`, `datos`).
- `bloqueado-hardware` marca lo que depende de grabar en pista o comprar material.
- El estado se sigue en el tablero del Project «Relevos».
- Las dependencias se escriben en la sección «Depende de» de la issue (`- #n`). La Action
  `disponibilidad.yml` las convierte en dependencias de GitHub (*blocked by*) y rellena el campo
  «Disponibilidad»: **Lista** si no espera a ninguna issue abierta, **Bloqueada** si sí, **Hecha** si
  está cerrada. La pestaña «Disponibilidad» del Project agrupa por ese campo.
- Una dependencia que sobra se quita a mano en la issue (quitar la línea no la borra).
- La Action necesita el secret `PROJECT_TOKEN`: un token clásico con permisos `project` y
  `public_repo`. Si caduca, la Action falla; se renueva con `gh secret set PROJECT_TOKEN`.

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
- PRs pequeñas, contra `main`, con `Closes #n` en la descripción. Si la PR no termina la issue
  (por ejemplo, un diseño que se deja por escrito antes de implementarlo), `Refs #n`.
- Lo que se haga tiene que encajar con las decisiones y parámetros de
  [docs/decisiones.md](docs/decisiones.md); si cambia alguno, se actualiza en la misma PR.
- La CI (ruff + pytest) debe estar en verde antes de mergear.
- Se mergea con **squash merge** y se borra la rama.
- No se hace push directo a `main`.

## Código
- Python >= 3.10, `ruff` para lint y formato.
- Tests con `pytest`; usar datos sintéticos (homografías, trayectorias) cuando no haya vídeos reales.
- Los vídeos y sesiones van en `data/`, fuera del repositorio.
- Usar siempre la marca de tiempo real de cada fotograma, nunca `índice / fps`.
