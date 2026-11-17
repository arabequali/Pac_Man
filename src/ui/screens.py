from abc import ABC, abstractmethod
from typing import Any

from src.config.models import Config

from src.maze.maze import Cell

from src.ui.graphics import Graphics
from src.ui.renderer import MazeLayout

from src.engine.engine import GameEngine


class Screen(ABC):
    """Base class for all screens in the application."""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def handle_actions(self, action: Any) -> Any | None:
        """Handle an action from the event loop."""
        pass

    @abstractmethod
    def update(self, time_elapsed: float) -> Any | None:
        """Update the screen state based on elapsed time."""
        pass

    @abstractmethod
    def draw(self, graphics: Graphics) -> None:
        """Draw the screen using the Graphics class."""
        pass

    def on_enter(self) -> None:
        """Called when the screen is entered."""
        pass

    def on_exit(self) -> None:
        """Called when the screen is exited."""
        pass


class ExitScreen(Screen):
    """A screen that indicates the application should exit."""

    def handle_actions(self, action: Any) -> None:
        return None

    def update(self, time_elapsed: float) -> None:
        pass

    def draw(self, graphics: Graphics) -> None:
        pass

    def on_enter(self) -> None:
        pass


class MainMenuScreen(Screen):
    """The main menu screen of the application."""

    def __init__(self) -> None:
        super().__init__()
        self._selected_option = 0
        self._options = ["Start Game", "Highscores","Options", "Exit"]

    def handle_actions(self, action: Any) -> str | None:

        if action == "KEYDOWN_UP" or action == "KEYDOWN_W":
            self._selected_option = (self._selected_option - 1) % len(self._options)

        elif action == "KEYDOWN_DOWN" or action == "KEYDOWN_S":
            self._selected_option = (self._selected_option + 1) % len(self._options)

        elif action == "KEYDOWN_RETURN":
            if self._selected_option == self._options.index("Start Game"):
                return "game"  # Transition to the game screen
            elif self._selected_option == self._options.index("Highscores"):
                return "highscores"  # Transition to the highscore screen
            elif self._selected_option == self._options.index("Options"):
                return "options"  # Transition to the options screen
            elif self._selected_option == self._options.index("Exit"):
                return "exit"  # Exit the application

        return None

    def update(self, time_elapsed: float) -> None:
        pass

    def draw(self, graphics: Graphics) -> None:

        window_w, window_h = graphics.get_window_size()

        for i, option in enumerate(self._options):

            color = (255, 255, 255) if i == self._selected_option else (100, 100, 100)
            x_placement = window_w // 2 - graphics.get_string_size(option, 30)[0] // 2
            y_placement = window_h // 2 + i * (graphics.get_string_size(option, 30)[1] + 15)

            graphics.draw_string(x_placement, y_placement, option, font_size=30, color=color)


class HighscoreScreen(Screen):
    """The highscore screen of the application."""

    def __init__(self) -> None:
        super().__init__()
        self._highscores = ["Player1: 1000", "Player2: 800", "Player3: 600"]

    def handle_actions(self, action: Any) -> str | None:
        if action == "KEYDOWN_ESCAPE":
            return "main_menu"  # Go back to the main menu
        return None

    def update(self, time_elapsed: float) -> None:
        pass

    def draw(self, graphics: Graphics) -> None:
        for i, score in enumerate(self._highscores):
            graphics.draw_string(50, 50 + i * 30, score, font_size=24, color=(255, 255, 255))


class OptionsScreen(Screen):
    """The options screen of the application."""

    def __init__(
            self,
            config: Config
        ) -> None:
        super().__init__()
        self._selected_option = 0
        self._options = [key[0] for key in config]
        self._options.append("Back")
        self._config = config

    def set_config(self, config: Config) -> None:
        self._config = config

    def handle_actions(self, action: Any) -> str | None:

        if action == "KEYDOWN_UP":
            self._selected_option = (self._selected_option - 1) % len(self._options)
        elif action == "KEYDOWN_DOWN":
            self._selected_option = (self._selected_option + 1) % len(self._options)
        elif action == "KEYDOWN_RIGHT" or action == "KEYDOWN_LEFT":
            self.config_change(action)
        elif action == "KEYDOWN_RETURN":
            if self._selected_option == self._options.index("highscore_filename_path"):
                self.highscore_path_change()
            elif self._selected_option == self._options.index("Back"):
                return "main_menu"  # Go back to the main menu
        elif action == "KEYDOWN_ESCAPE":
            return "main_menu"  # Go back to the main menu

        return None

    def highscore_path_change(self) -> None:
        print("But nobody came...")

    def config_change(self, action: Any,) -> None:

        attr_name = self._options[self._selected_option]
        attr_value = self._config.__getattribute__(attr_name)
        if self._selected_option == self._options.index("cheat_mode"):
            self._config.cheat_mode = not self._config.cheat_mode
        elif isinstance(attr_value, int):
            if action == "KEYDOWN_RIGHT":
                self._config.__setattr__(attr_name, attr_value + 1)
            elif action == "KEYDOWN_LEFT":
                self._config.__setattr__(attr_name, attr_value - 1)

    def update(self, time_elapsed: float) -> None:
        pass

    def draw(self, graphics: Graphics) -> None:
        for i, option in enumerate(self._options):
            color = (255, 255, 255) if i == self._selected_option else (100, 100, 100)
            text = f"{option.capitalize().replace("_", " ")}: {self.get_config_value(option)}" if option != "Back" else option
            graphics.draw_string(50, 50 + i * 30, text, font_size=24, color=color)

    def get_config_value(self, option: str) -> int | str | bool | None:
        return self._config.model_dump()[option]


class GameScreen(Screen):
    """The game screen of the application."""

    def __init__(
            self,
            config: Config,
            game_engine: GameEngine,
            maze_layout: MazeLayout
        ) -> None:
        super().__init__()
        self._config = config
        self._game_engine = game_engine
        self.maze_layout = maze_layout

    def set_config(self, config: Config) -> None:
        self._config = config

    def handle_actions(self, action: Any) -> str | None:

        if action == "KEYDOWN_ESCAPE":
            return "main_menu"  # Go back to the main menu

        return None

    def update(self, time_elapsed: float) -> str | None:
        # Update game state here
        return None

    def draw(
            self,
            graphics: Graphics
        ) -> None:
        """Draw the whole game."""

        maze_image = self.maze_layout.maze_image
        width_offset = self.maze_layout.width_offset // 2
        height_offset = self.maze_layout.height_offset // 2
        graphics.put_image(maze_image, width_offset, height_offset)
        # Draw game elements here

    def on_enter(
            self,
        ) -> None:
        pass  # Initialize game state when entering the game screen