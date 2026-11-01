# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

`relevos` analiza en vídeo las entregas del 4x100 (móvil fijo a 60 fps + rejilla de 21 platillos
sobre la pista) y recomienda la marca de salida del receptor en pies. Todo el proyecto (código,
identificadores, docs, issues, commits) está en **español**; mantenerlo así.

Objetivo de producto: subir un vídeo **sin rellenar nada** y obtener la evaluación. Todo lo que se
pueda sacar del vídeo (sentido de carrera, calibración con los primeros fotogramas de pista vacía,
marca usada, resultado de la entrega, si la cámara se movió) se infiere; solo la pareja de atletas
y la longitud del pie son opcionales. La hoja de ruta va primero en manual (F3–F5: calibración y
eventos con clics) y automatiza después (F6 «Análisis automático», F8 «Historial y extras»).

**Contexto del proyecto**: `docs/decisiones.md` recoge el estado actual, la hoja de ruta, las
decisiones técnicas (D-001…), los parámetros vigentes y las preguntas abiertas. Léelo al empezar
una sesión. Cuando se tome una decisión, cambie un parámetro o se cierre una issue, actualízalo
en la misma rama (decisión nueva en vez de borrar la antigua; línea en la bitácora).

## Comandos

```bash
python -m venv venv && venv\Scripts\activate     # Windows (Linux/macOS: source venv/bin/activate)
pip install -e ".[dev]"                          # extra [deteccion] = ultralytics, para la fase 6
pre-commit install                               # instala hooks pre-commit, commit-msg y pre-push

ruff check . && ruff format --check .
pytest                                           # todos los tests
pytest tests/test_video.py::test_nombre -q       # un solo test
pre-commit run --all-files

relevos info VIDEO [--json]                      # fps reales, VFR y avisos de un vídeo
```

El hook de pre-push ejecuta `python -m pytest` con `language: system`: necesita el venv en el
PATH, o falla con «No module named pytest». La CI (`.github/workflows/ci.yml`) repite ruff y
pytest en Python 3.10–3.12.

## Arquitectura

Paquete en layout `src/` (`src/relevos/`), CLI con argparse en `cli.py`: cada subcomando es una
función `comando_<nombre>(args) -> int` registrada con `set_defaults(funcion=...)`. Los errores
esperados se lanzan como excepciones propias (p. ej. `ErrorVideo`) y la CLI los convierte en
mensaje a stderr y código 1. Las salidas `--json` usan `ensure_ascii=False, allow_nan=False`.

`video.py` es la base de todo lo demás:
- **Marcas de tiempo reales**: `leer_timestamps` hace `grab()` y lee `CAP_PROP_POS_MSEC` de cada
  fotograma. El resto del código debe usar siempre `InfoVideo.timestamps`, **nunca `índice / fps`**
  (los móviles graban con frecuencia variable).
- `InfoVideo` valida en `__post_init__` (≥2 marcas, finitas, mediana de intervalos > 0) y lo
  dudoso (marcas repetidas sueltas, VFR, < 50 fps, fps nominales distintos de los reales) se
  devuelve como avisos en `avisos()`, no como error.

Diseño previsto para las fases siguientes (ver issues por milestone): homografía por tramos de la
rejilla a coordenadas de pista (s, d), `solvePnP` para la pose de la cámara (no se mide a mano),
suavizado Savitzky-Golay de trayectorias, y modelo de marca
`T = tr + t_receptor(L)`, `marca = v·T − L + d_libre`.

Tests con vídeos sintéticos generados en el propio test (`cv2.VideoWriter`, mp4v) y datos
sintéticos; no hay vídeos reales en el repo.

## Convenciones del repo

- Una issue por unidad de trabajo, con milestone (F1–F8) y en el Project «Relevos».
- Ramas `feat|fix|docs/<n>-slug` desde `main`; nunca push directo a `main`.
- Mensajes de commit y títulos de PR: `[#<issue>] <descripción corta>` (imperativo, sin punto
  final). El hook commit-msg los rechaza si no; solo se permite squash merge, así que el título
  de la PR acaba siendo el commit en `main`. PR con `Closes #n`.
- PRs dependientes se apilan con `gh stack` (extensión gh-stack).
- Skills del proyecto en `.claude/skills/` (antislop: núcleo, comentarios de código y textos;
  ver su README). Aplican también a lo que se escribe en español.
- Para revisar una PR usar el subagente `revisor-pr` (`.claude/agents/revisor-pr.md`); no
  publica comentarios en GitHub salvo que se pida.
- El repo es **público**: vídeos, sesiones y nombres reales van solo en `data/` (ignorado por
  git); en el repo solo alias (ATL1, ATL2…). `.gitignore` también excluye `*.mp4`, `*.mov`, `*.pt`.
- Protocolo de grabación en `docs/protocolo.md` (iPhone 4K60, sin hoja de registro).
- Windows: `core.autocrlf=true` (no añadir `mixed-line-ending --fix=lf`); en Git Bash los
  acentos de la salida por tubería se ven mal, PowerShell los muestra bien.
