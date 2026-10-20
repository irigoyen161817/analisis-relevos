# analisis-relevos

[![CI](https://github.com/irigoyen161817/analisis-relevos/actions/workflows/ci.yml/badge.svg)](https://github.com/irigoyen161817/analisis-relevos/actions/workflows/ci.yml)

Herramienta que analiza en vídeo las entregas del 4x100, grabadas con un móvil fijo,
mide cómo se hace cada pase y recomienda a qué distancia poner la marca de salida del receptor.

Resultado tras cada intento (objetivo):

```
marca usada: 28 pies · pase a 21 m de la zona · recomendación: alejar 1,5 pies
```

## Instalación

Requiere Python 3.10 o superior.

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -e ".[dev]"
```

Para la detección automática de atletas (fase 6): `pip install -e ".[deteccion]"`.

## Uso

```bash
relevos --help
```

## Desarrollo

Activa los hooks una vez tras instalar (con el venv activado):

```bash
pre-commit install
```

A partir de ahí, cada `git commit` pasa ruff (lint y formato) y bloquea ficheros grandes
como vídeos, y cada `git push` ejecuta los tests. Para pasarlos a mano sobre todo el repo:
`pre-commit run --all-files`.

Comandos sueltos:

```bash
ruff check .
ruff format .
pytest
```

El trabajo se organiza con issues, milestones (una por fase de la hoja de ruta) y PRs.
Ver [CONTRIBUTING.md](CONTRIBUTING.md).

Los vídeos y sesiones se guardan en `data/`, que no se versiona.
