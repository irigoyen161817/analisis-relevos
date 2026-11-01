import importlib.util
from pathlib import Path

import pytest

RUTA = Path(__file__).parents[1] / "scripts" / "disponibilidad.py"
spec = importlib.util.spec_from_file_location("disponibilidad", RUTA)
disponibilidad = importlib.util.module_from_spec(spec)
spec.loader.exec_module(disponibilidad)

CUERPO = """## Objetivo
Algo que cita #99 fuera de la sección.

## Depende de
- #10
- #9, y otra vez #10

## Notas
Ver #5.
"""


def test_lee_solo_la_seccion_depende_de():
    assert disponibilidad.leer_dependencias(CUERPO) == [10, 9]


def test_seccion_al_final_del_cuerpo():
    assert disponibilidad.leer_dependencias("## Depende de\n- #4\n- #8") == [4, 8]


@pytest.mark.parametrize(
    "cuerpo",
    [None, "", "## Objetivo\nNada que ver con #3", "## Depende de\n<!-- - #n -->\n\n## Notas"],
)
def test_sin_dependencias(cuerpo):
    assert disponibilidad.leer_dependencias(cuerpo) == []


@pytest.mark.parametrize(
    ("estado", "dependencias", "esperado"),
    [
        ("CLOSED", ["OPEN"], "Hecha"),
        ("OPEN", [], "Lista"),
        ("OPEN", ["CLOSED", "CLOSED"], "Lista"),
        ("OPEN", ["CLOSED", "OPEN"], "Bloqueada"),
    ],
)
def test_calcular_disponibilidad(estado, dependencias, esperado):
    assert disponibilidad.calcular_disponibilidad(estado, dependencias) == esperado
