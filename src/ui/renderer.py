import time

from src.ui.graphics import Graphics


class Renderer:
    """The class that handles the rendering of the application (drawing in screen)."""

    def __init__(self, graphics: Graphics) -> None:
        self._graphics = graphics
        self._last_time = time.time()

    @property
    def graphics(self) -> Graphics:
        return self._graphics

    @property
    def last_time(self) -> float:
        return self._last_time

    def get_time_elapsed(self) -> float:
        current_time = time.time()
        elapsed_time = current_time - self._last_time
        self._last_time = current_time
        return elapsed_time