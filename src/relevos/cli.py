"""Punto de entrada de la línea de comandos `relevos`."""

import argparse

from relevos import __version__


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="relevos",
        description="Análisis en vídeo de las entregas del 4x100.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_subparsers(dest="comando", metavar="COMANDO")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = crear_parser()
    args = parser.parse_args(argv)
    if args.comando is None:
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
