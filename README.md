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
relevos info video.mp4          # resolución, duración, fps nominales y reales, avisos
relevos info video.mp4 --json
```

`relevos info` lee la marca de tiempo real de cada fotograma y avisa si el vídeo tiene
frecuencia variable (VFR) o fotogramas perdidos, si tiene menos de 60 fps reales (por
ejemplo, cámara lenta exportada a 30 fps) o si los fps que declara el fichero no son los reales.
Úsalo con el primer vídeo de cada móvil para comprobar que sirve para medir.

### Grabar una sesión

Sigue el [protocolo de grabación](docs/protocolo.md): ajustes del iPhone, colocación de la
rejilla de platillos, encuadre y procedimiento. No hace falta rellenar ninguna hoja: se prepara
la pista, se graba un vídeo por intento y el resto se saca del propio vídeo.

## Desarrollo

Activa los hooks una vez tras instalar (con el venv activado):

```bash
pre-commit install
```

A partir de ahí, cada `git commit` pasa ruff (lint y formato) y bloquea ficheros grandes
como vídeos, y cada `git push` ejecuta los tests. Para pasarlos a mano sobre todo el repo:
`pre-commit run --all-files`.

Los mensajes de commit deben seguir el formato `[#<issue>] <descripción corta>`,
por ejemplo `[#4] Comando info con los fps reales`. El hook rechaza el commit si no es así.

Comandos sueltos:

```bash
ruff check .
ruff format .
pytest
```

El trabajo se organiza con issues, milestones (una por fase de la hoja de ruta) y PRs.
Ver [CONTRIBUTING.md](CONTRIBUTING.md).

Los vídeos y sesiones se guardan en `data/`, que no se versiona.
