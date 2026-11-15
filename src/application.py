import time

from src.config.loader import ConfigLoader
from src.ui.graphics import Graphics
from src.ui.renderer import Renderer
from src.ui.screens import Screen, GameScreen, MainMenuScreen, ExitScreen, HighscoreScreen, OptionsScreen


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
        self._running: bool = False
        self.screens = {
            "main_menu": MainMenuScreen(),
            "highscores": HighscoreScreen(),
            "options": OptionsScreen(),
            "game": GameScreen(),
            "exit": ExitScreen()
        }
        self.current_screen_name: str = "main_menu"
        self._last_time = time.time()

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

    def get_time_elapsed(self) -> float:
        current_time = time.time()
        elapsed_time = current_time - self._last_time
        self._last_time = current_time
        return elapsed_time

    def set_running(self, running: bool) -> None:
        self._running = running

    def run(self) -> None:
        """Run the application."""
        self.graphics.open_window()

        self.set_running(True)
        while self.running:
            # Handle events
            actions = self.graphics.get_actions()
            if len(actions) > 0:
                if actions[0] == "QUIT":
                    self.set_running(False)
                else:
                    new_screen = self.screens[self.current_screen_name].handle_actions(actions[0])
                    if new_screen is not None:
                        self.screens[self.current_screen_name].on_exit()
                        self.current_screen_name = new_screen
                        self.screens[self.current_screen_name].on_enter()

            if self.current_screen_name == "exit":
                self.set_running(False)

            # Update the current screen
            self.screens[self.current_screen_name].update(self.get_time_elapsed())

            # Draw the current screen
            self.graphics.clear_window((0, 0, 0))  # Clear the window with black color
            self.screens[self.current_screen_name].draw(self._renderer)
            self.graphics.update_window()
        self.graphics.close_window()