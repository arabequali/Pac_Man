from src.ui.graphics import Graphics


class Renderer:
    """The class that handles the rendering of the application (drawing in screen)."""

    def __init__(self, graphics: Graphics) -> None:
        self._graphics = graphics

    @property
    def graphics(self) -> Graphics:
        return self._graphics
