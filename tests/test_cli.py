import pytest

from relevos import __version__
from relevos.cli import main


def test_sin_argumentos_muestra_ayuda(capsys):
    assert main([]) == 0
    assert "relevos" in capsys.readouterr().out


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out
