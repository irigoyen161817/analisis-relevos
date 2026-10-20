"""Punto de entrada de la línea de comandos `relevos`."""

import argparse
import json
import sys

from relevos import __version__
from relevos.video import ErrorVideo, info_video


def comando_info(args: argparse.Namespace) -> int:
    try:
        info = info_video(args.video)
    except ErrorVideo as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        datos = {
            "ruta": str(info.ruta),
            "ancho": info.ancho,
            "alto": info.alto,
            "fotogramas": info.fotogramas,
            "duracion_s": info.duracion,
            "fps_nominal": info.fps_nominal,
            "fps_real": info.fps_real,
            "vfr": info.es_vfr,
            "avisos": info.avisos(),
        }
        print(json.dumps(datos, ensure_ascii=False, indent=2, allow_nan=False))
        return 0

    print(f"Vídeo:        {info.ruta}")
    print(f"Resolución:   {info.ancho}x{info.alto}")
    print(f"Duración:     {info.duracion:.2f} s")
    print(f"Fotogramas:   {info.fotogramas}")
    print(f"Fps nominal:  {info.fps_nominal:.2f}")
    print(f"Fps reales:   {info.fps_real:.2f}")
    print(f"Frecuencia:   {'variable (VFR)' if info.es_vfr else 'constante'}")
    avisos = info.avisos()
    if avisos:
        print()
        for aviso in avisos:
            print(f"AVISO: {aviso}")
    return 0


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="relevos",
        description="Análisis en vídeo de las entregas del 4x100.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="comando", metavar="COMANDO")

    info = subparsers.add_parser("info", help="Muestra los fps reales y los metadatos de un vídeo.")
    info.add_argument("video", help="Ruta del vídeo.")
    info.add_argument("--json", action="store_true", help="Salida en formato JSON.")
    info.set_defaults(funcion=comando_info)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = crear_parser()
    args = parser.parse_args(argv)
    if args.comando is None:
        parser.print_help()
        return 0
    return args.funcion(args)


if __name__ == "__main__":
    raise SystemExit(main())
