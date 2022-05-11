from os.path import join as opj
from pathlib import Path
import logging


class Configuration:
    def __init__(self):
        self._home = str(Path.home())
        self._weather_dir = opj(self._home, '.fzj_weather_prometheus_exporter')


logging.basicConfig(level=logging.ERROR)  # external logging level
logger = logging.getLogger('weather')  # internal logging level
logger.setLevel(level=logging.INFO)

__params__ = Configuration()
__all__ = ['logger', '__version__', '__params__']
