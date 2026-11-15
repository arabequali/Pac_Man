from abc import ABC, abstractmethod
from typing import Any

from src.ui.renderer import Renderer


class Screen(ABC):
    """Base class for all screens in the application."""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def handle_actions(self, actions: list) -> Any | None:
        """Handle an action from the event loop."""
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

    def handle_actions(self, actions: list) -> None:
        return None

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

    def handle_actions(self, actions: list) -> Screen | None:

        for action in actions:

            if action == "KEYDOWN_UP":
                self._selected_option = (self._selected_option - 1) % len(self._options)

            elif action == "KEYDOWN_DOWN":
                self._selected_option = (self._selected_option + 1) % len(self._options)

            elif action == "KEYDOWN_RETURN":
                if self._selected_option == 0:
                    return GameScreen()  # Transition to the game screen
                elif self._selected_option == 1:
                    return OptionsScreen()  # Transition to the options screen
                elif self._selected_option == 2:
                    return ExitScreen()  # Exit the application

        return None

    def draw(self, renderer: Renderer) -> None:

        renderer.graphics.clear_window((0, 0, 0))  # Clear the window with black color

        window = renderer.graphics._window
        window_w = window.get_width()
        window_h = window.get_height()

        for i, option in enumerate(self._options):

            color = (255, 255, 255) if i == self._selected_option else (100, 100, 100)
            x_placement = window_w // 2 - renderer.graphics.get_string_size(option, 30)[0] // 2
            y_placement = window_h // 2 + i * (renderer.graphics.get_string_size(option, 30)[1] + 15)

            renderer.graphics.draw_string(window, x_placement, y_placement, option, font_size=30, color=color)


class HighscoreScreen(Screen):
    """The highscore screen of the application."""

    def __init__(self) -> None:
        super().__init__()
        self._highscores = ["Player1: 1000", "Player2: 800", "Player3: 600"]

    def handle_actions(self, actions: list) -> Screen | None:
        for action in actions:
            if action == "KEYDOWN_ESCAPE":
                return MainMenuScreen()  # Go back to the main menu
        return None

    def draw(self, renderer: Renderer) -> None:
        renderer.graphics.clear_window((0, 0, 0))  # Clear the window with black color
        for i, score in enumerate(self._highscores):
            renderer.graphics.draw_string(renderer.graphics._window, 50, 50 + i * 30, score, font_size=24, color=(255, 255, 255))


class OptionsScreen(Screen):
    """The options screen of the application."""

    def __init__(self) -> None:
        super().__init__()
        self._selected_option = 0
        self._options = ["Option 1", "Option 2", "Back"]

    def handle_actions(self, actions: list) -> Screen | None:
        for action in actions:
            if action == "KEYDOWN_UP":
                self._selected_option = (self._selected_option - 1) % len(self._options)
            elif action == "KEYDOWN_DOWN":
                self._selected_option = (self._selected_option + 1) % len(self._options)
            elif action == "KEYDOWN_RETURN":
                if self._selected_option == 2:
                    return MainMenuScreen()  # Go back to the main menu
        return None

    def draw(self, renderer: Renderer) -> None:
        renderer.graphics.clear_window((0, 0, 0))  # Clear the window with black color
        for i, option in enumerate(self._options):
            color = (255, 255, 255) if i == self._selected_option else (100, 100, 100)
            renderer.graphics.draw_string(renderer.graphics._window, 50, 50 + i * 30, option, font_size=24, color=color)


class GameScreen(Screen):
    """The game screen of the application."""

    def __init__(self) -> None:
        super().__init__()
        # Initialize game state here

    def handle_actions(self, actions: list) -> Screen | None:
        for action in actions:
            if action == "KEYDOWN_ESCAPE":
                return MainMenuScreen()  # Go back to the main menu
        return None

    def update(self, time_elapsed: float) -> Screen | None:
        # Update game state here
        return None

    def draw(self, renderer: Renderer) -> None:
        renderer.graphics.clear_window((0, 0, 0))  # Clear the window with black color
        # Draw game elements here