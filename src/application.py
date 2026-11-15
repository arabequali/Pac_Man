from src.config.loader import ConfigLoader
from src.ui.graphics import Graphics
from src.ui.renderer import Renderer
from src.ui.screens import GameScreen, MainMenuScreen, ExitScreen


class Application:
    """The class where the display and the events are managed."""

    def __init__(
            self,
            config: ConfigLoader,
            graphics: Graphics,
            renderer: Renderer,
        ) -> None:
        self._config = config
        self._graphics = graphics
        self._renderer = renderer
        self._running = False
        self.current_screen = MainMenuScreen()

    @property
    def config(self) -> ConfigLoader:
        return self._config

    @property
    def graphics(self) -> Graphics:
        return self._graphics

    @property
    def renderer(self) -> Renderer:
        return self._renderer

    @property
    def running(self) -> bool:
        return self._running

    def set_running(self, running: bool) -> None:
        self._running = running

    def run(self) -> None:
        """Run the application."""
        self.graphics.open_window()

        self.set_running(True)
        while self.running:
            # Handle events
            actions = self.graphics.get_actions()
            for action in actions:
                if action == "QUIT":
                    self.set_running(False)
                else:
                    new_screen = self.current_screen.handle_actions(actions)
                    if new_screen is not None:
                        self.current_screen.on_exit()
                        self.current_screen = new_screen
                        self.current_screen.on_enter()
                        break  # Exit the loop to avoid processing further actions for the old screen

            if isinstance(self.current_screen, ExitScreen):
                self.set_running(False)

            # Update the current screen
            if isinstance(self.current_screen, GameScreen):
                self.current_screen.update(self._renderer.get_time_elapsed())

            # Draw the current screen
            self.graphics.clear_window((0, 0, 0))  # Clear the window with black color
            self.current_screen.draw(self._renderer)
            self.graphics.update_window()
        self.graphics.close_window()