"""Lectura de vídeos y marcas de tiempo reales de cada fotograma.

Muchos móviles graban con frecuencia variable (VFR), así que el resto del código
debe usar siempre estas marcas de tiempo, nunca `índice / fps`.
"""

from dataclasses import dataclass, field
from pathlib import Path

import cv2
import numpy as np

# Un intervalo entre fotogramas que se aleja más de esto de la mediana indica
# frecuencia variable o fotogramas perdidos.
TOLERANCIA_VFR = 0.10
# Por debajo de estos fps reales la medida de la reacción pierde precisión.
FPS_MINIMOS = 50.0
# Diferencia relativa admitida entre los fps que declara el fichero y los reales.
TOLERANCIA_FPS_NOMINAL = 0.05


class ErrorVideo(Exception):
    """El vídeo no se puede abrir, no tiene fotogramas suficientes o sus marcas de tiempo
    no son válidas."""


@dataclass
class InfoVideo:
    ruta: Path
    ancho: int
    alto: int
    fotogramas: int
    fps_nominal: float
    """Fps que declara el fichero; OpenCV devuelve 0 si no los conoce."""
    timestamps: np.ndarray = field(repr=False)
    """Marca de tiempo de cada fotograma, en segundos desde el primero.

    Se comprueba al crear el objeto: al menos 2, todas finitas y con la mediana de los
    intervalos positiva (si no, no se pueden calcular los fps). Las marcas repetidas o
    desordenadas sueltas se admiten y se avisan como frecuencia variable.
    """

    def __post_init__(self):
        self.timestamps = np.asarray(self.timestamps, dtype=float)
        if len(self.timestamps) < 2:
            raise ErrorVideo(f"El vídeo tiene menos de 2 fotogramas: {self.ruta}")
        if not np.all(np.isfinite(self.timestamps)):
            raise ErrorVideo(f"Marcas de tiempo no válidas (no numéricas): {self.ruta}")
        if np.median(np.diff(self.timestamps)) <= 0:
            raise ErrorVideo(
                f"Marcas de tiempo no válidas: la mayoría están repetidas o a cero: {self.ruta}"
            )

    @property
    def intervalos(self) -> np.ndarray:
        return np.diff(self.timestamps)

    @property
    def marcas_no_crecientes(self) -> int:
        """Número de fotogramas cuya marca de tiempo repite o retrocede respecto a la anterior."""
        return int(np.sum(self.intervalos <= 0))

    @property
    def fps_real(self) -> float:
        """Fps a partir de la mediana de los intervalos reales entre fotogramas."""
        return 1.0 / float(np.median(self.intervalos))

    @property
    def duracion(self) -> float:
        """Duración en segundos, incluyendo el último fotograma."""
        return float(self.timestamps.max() - self.timestamps.min()) + 1.0 / self.fps_real

    @property
    def es_vfr(self) -> bool:
        return es_frecuencia_variable(self.timestamps)

    def avisos(self) -> list[str]:
        avisos = []
        if self.marcas_no_crecientes:
            avisos.append(
                f"{self.marcas_no_crecientes} fotograma(s) con la marca de tiempo repetida o "
                "desordenada: las medidas en esos fotogramas no serán fiables."
            )
        if self.es_vfr:
            avisos.append(
                "Frecuencia variable (VFR) o fotogramas perdidos: usa siempre las "
                "marcas de tiempo reales, no índice / fps."
            )
        if self.fps_real < FPS_MINIMOS:
            aviso = (
                f"Solo {self.fps_real:.1f} fps reales; para medir la reacción hacen falta 60 fps."
            )
            if self.fps_real < 35:
                aviso += " Si lo grabaste en cámara lenta, puede haberse exportado a 30 fps."
            avisos.append(aviso)
        if (
            self.fps_nominal > 0
            and abs(self.fps_nominal - self.fps_real) / self.fps_real > TOLERANCIA_FPS_NOMINAL
        ):
            avisos.append(
                f"El fichero declara {self.fps_nominal:.2f} fps pero los reales son "
                f"{self.fps_real:.2f}: no te fíes de los fps nominales."
            )
        return avisos


def es_frecuencia_variable(timestamps: np.ndarray, tolerancia: float = TOLERANCIA_VFR) -> bool:
    """True si algún intervalo entre fotogramas se aleja de la mediana más que la tolerancia.

    Con menos de 3 fotogramas solo hay un intervalo y no hay con qué compararlo: devuelve
    False. Intervalos nulos o negativos (marcas repetidas o desordenadas) cuentan como
    frecuencia variable.
    """
    intervalos = np.diff(timestamps)
    if len(intervalos) < 2:
        return False
    if np.any(intervalos <= 0):
        return True
    mediana = np.median(intervalos)
    return bool(np.any(np.abs(intervalos - mediana) > tolerancia * mediana))


def leer_timestamps(captura: cv2.VideoCapture) -> np.ndarray:
    """Recorre el vídeo sin decodificar las imágenes y devuelve la marca de tiempo de cada
    fotograma en segundos, relativa al primero.

    Si el vídeo está truncado, devuelve los fotogramas que se han podido leer hasta el
    primer fallo, que pueden ser menos de los que declara el fichero.
    """
    marcas = []
    while captura.grab():
        marcas.append(captura.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
    timestamps = np.asarray(marcas, dtype=float)
    if len(timestamps):
        timestamps -= timestamps[0]
    return timestamps


def info_video(ruta: str | Path) -> InfoVideo:
    ruta = Path(ruta)
    if not ruta.is_file():
        raise ErrorVideo(f"No existe el fichero: {ruta}")
    captura = cv2.VideoCapture(str(ruta))
    try:
        if not captura.isOpened():
            raise ErrorVideo(f"No se puede abrir el vídeo: {ruta}")
        ancho = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
        alto = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps_nominal = float(captura.get(cv2.CAP_PROP_FPS))
        timestamps = leer_timestamps(captura)
    finally:
        captura.release()
    return InfoVideo(
        ruta=ruta,
        ancho=ancho,
        alto=alto,
        fotogramas=len(timestamps),
        fps_nominal=fps_nominal,
        timestamps=timestamps,
    )
