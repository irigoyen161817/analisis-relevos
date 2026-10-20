import json
from pathlib import Path

import cv2
import numpy as np
import pytest

from relevos.cli import main
from relevos.video import ErrorVideo, InfoVideo, es_frecuencia_variable, info_video


def crear_video(ruta, fps, fotogramas, tamano=(64, 48)):
    """Genera un vídeo sintético con fps constantes."""
    ancho, alto = tamano
    escritor = cv2.VideoWriter(str(ruta), cv2.VideoWriter_fourcc(*"mp4v"), fps, (ancho, alto))
    assert escritor.isOpened()
    for i in range(fotogramas):
        escritor.write(np.full((alto, ancho, 3), i % 256, np.uint8))
    escritor.release()
    return ruta


@pytest.fixture
def video_60(tmp_path):
    return crear_video(tmp_path / "v60.mp4", fps=60, fotogramas=120)


@pytest.fixture
def video_30(tmp_path):
    return crear_video(tmp_path / "v30.mp4", fps=30, fotogramas=60)


def test_info_video_60fps(video_60):
    info = info_video(video_60)
    assert (info.ancho, info.alto) == (64, 48)
    assert info.fotogramas == 120
    assert info.fps_nominal == pytest.approx(60)
    assert info.fps_real == pytest.approx(60, rel=0.01)
    assert info.duracion == pytest.approx(2.0, rel=0.01)
    assert info.timestamps[0] == 0
    assert not info.es_vfr
    assert info.avisos() == []


def test_info_video_30fps_avisa(video_30):
    info = info_video(video_30)
    assert info.fps_real == pytest.approx(30, rel=0.01)
    avisos = " ".join(info.avisos())
    assert "60 fps" in avisos
    assert "cámara lenta" in avisos


def test_fichero_inexistente(tmp_path):
    with pytest.raises(ErrorVideo):
        info_video(tmp_path / "no_existe.mp4")


def test_fichero_que_no_es_video(tmp_path):
    ruta = tmp_path / "texto.mp4"
    ruta.write_text("no soy un vídeo")
    with pytest.raises(ErrorVideo):
        info_video(ruta)


def test_video_de_un_fotograma(tmp_path):
    ruta = crear_video(tmp_path / "v1.mp4", fps=60, fotogramas=1)
    with pytest.raises(ErrorVideo, match="menos de 2"):
        info_video(ruta)


def info_sintetica(timestamps, fps_nominal=60.0):
    return InfoVideo(
        ruta=Path("sintetico.mp4"),
        ancho=1920,
        alto=1080,
        fotogramas=len(timestamps),
        fps_nominal=fps_nominal,
        timestamps=np.asarray(timestamps, dtype=float),
    )


@pytest.mark.parametrize(
    "timestamps",
    [
        [],
        [0.0],
        [0.0, 0.0, 0.0],  # OpenCV devuelve POS_MSEC = 0 con algunos códecs
        [0.0, 0.1, 0.1, 0.1],  # marcas repetidas: mediana de intervalos 0
        [0.0, 0.2, 0.1],  # desordenadas
        [0.0, float("nan"), 0.2],
    ],
)
def test_marcas_de_tiempo_no_validas(timestamps):
    with pytest.raises(ErrorVideo):
        info_sintetica(timestamps)


def test_dos_fotogramas_son_validos():
    info = info_sintetica([0.0, 1 / 60])
    assert info.fps_real == pytest.approx(60)
    assert not info.es_vfr


def test_fps_nominal_desconocido_no_avisa():
    info = info_sintetica(np.arange(120) / 60, fps_nominal=0.0)
    assert info.avisos() == []


def test_fps_nominal_distinto_avisa():
    info = info_sintetica(np.arange(120) / 60, fps_nominal=30.0)
    assert any("declara" in aviso for aviso in info.avisos())


def test_frecuencia_constante():
    assert not es_frecuencia_variable(np.arange(100) / 60)


def test_frecuencia_variable_por_fotograma_perdido():
    t = np.arange(100) / 60
    t = np.delete(t, 50)  # un hueco del doble de lo normal
    assert es_frecuencia_variable(t)


def test_frecuencia_variable_por_jitter():
    rng = np.random.default_rng(0)
    intervalos = 1 / 60 * (1 + rng.uniform(-0.3, 0.3, 99))
    assert es_frecuencia_variable(np.concatenate([[0], np.cumsum(intervalos)]))


def test_marcas_repetidas_son_vfr():
    assert es_frecuencia_variable(np.array([0.0, 0.0, 1 / 60, 2 / 60]))


def test_un_solo_intervalo_no_es_vfr():
    assert not es_frecuencia_variable(np.array([0.0, 1 / 60]))


def test_pequeno_jitter_no_es_vfr():
    rng = np.random.default_rng(0)
    intervalos = 1 / 60 * (1 + rng.uniform(-0.02, 0.02, 99))
    assert not es_frecuencia_variable(np.concatenate([[0], np.cumsum(intervalos)]))


def test_cli_info(video_60, capsys):
    assert main(["info", str(video_60)]) == 0
    salida = capsys.readouterr().out
    assert "64x48" in salida
    assert "Fps reales:   60.00" in salida
    assert "AVISO" not in salida


def test_cli_info_json(video_30, capsys):
    assert main(["info", str(video_30), "--json"]) == 0
    datos = json.loads(capsys.readouterr().out)
    assert datos["fotogramas"] == 60
    assert datos["fps_real"] == pytest.approx(30, rel=0.01)
    assert datos["vfr"] is False
    assert datos["avisos"]


def test_cli_info_error(tmp_path, capsys):
    assert main(["info", str(tmp_path / "no_existe.mp4")]) == 1
    assert "Error" in capsys.readouterr().err
