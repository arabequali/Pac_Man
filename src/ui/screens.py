from abc import ABC, abstractmethod
from typing import Any

from src.ui.renderer import Renderer


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
    def draw(self, renderer: Renderer) -> None:
        """Draw the screen using the renderer."""
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

    def draw(self, renderer: Renderer) -> None:
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

    def draw(self, renderer: Renderer) -> None:

        renderer.graphics.clear_window((0, 0, 0))  # Clear the window with black color

        window_w, window_h = renderer.graphics.get_window_size()

        for i, option in enumerate(self._options):

            color = (255, 255, 255) if i == self._selected_option else (100, 100, 100)
            x_placement = window_w // 2 - renderer.graphics.get_string_size(option, 30)[0] // 2
            y_placement = window_h // 2 + i * (renderer.graphics.get_string_size(option, 30)[1] + 15)

            renderer.graphics.draw_string(x_placement, y_placement, option, font_size=30, color=color)


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

    def draw(self, renderer: Renderer) -> None:
        renderer.graphics.clear_window((0, 0, 0))  # Clear the window with black color
        for i, score in enumerate(self._highscores):
            renderer.graphics.draw_string(50, 50 + i * 30, score, font_size=24, color=(255, 255, 255))


class OptionsScreen(Screen):
    """The options screen of the application."""

    def __init__(self) -> None:
        super().__init__()
        self._selected_option = 0
        self._options = ["Option 1", "Option 2", "Back"]

    def handle_actions(self, action: Any) -> str | None:

        if action == "KEYDOWN_UP":
            self._selected_option = (self._selected_option - 1) % len(self._options)
        elif action == "KEYDOWN_DOWN":
            self._selected_option = (self._selected_option + 1) % len(self._options)
        elif action == "KEYDOWN_RETURN":
            if self._selected_option == self._options.index("Back"):
                return "main_menu"  # Go back to the main menu
        elif action == "KEYDOWN_ESCAPE":
            return "main_menu"  # Go back to the main menu

        return None

    def update(self, time_elapsed: float) -> None:
        pass

    def draw(self, renderer: Renderer) -> None:
        renderer.graphics.clear_window((0, 0, 0))  # Clear the window with black color
        for i, option in enumerate(self._options):
            color = (255, 255, 255) if i == self._selected_option else (100, 100, 100)
            renderer.graphics.draw_string(50, 50 + i * 30, option, font_size=24, color=color)


class GameScreen(Screen):
    """The game screen of the application."""

    def __init__(self) -> None:
        super().__init__()
        # Initialize game state here

    def handle_actions(self, action: Any) -> str | None:

        if action == "KEYDOWN_ESCAPE":
            return "main_menu"  # Go back to the main menu

        return None

    def update(self, time_elapsed: float) -> str | None:
        # Update game state here
        return None

    def draw(self, renderer: Renderer) -> None:
        renderer.graphics.clear_window((0, 0, 0))  # Clear the window with black color
        # Draw game elements here
