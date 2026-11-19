import time

from typing import Any

from src.config.models import Config

from src.ui.graphics import Graphics
from src.ui.renderer import Renderer
from src.ui.screens import GameScreen, WinScreen, MainMenuScreen, ExitScreen, HighscoreScreen, OptionsScreen
from src.ui.sprites import SpriteBuilder

from src.engine.engine import GameEngine
from src.engine.objects import ObjectSet


MAX_DT = 1 / 60


class Application:
    """The class where the display and the events are managed."""

    def __init__(
            self,
            config: Config,
            graphics: Graphics,
            renderer: Renderer,
        ) -> None:

        self._config = config
        self._graphics = graphics
        self._renderer = renderer
        self._game_engine = None
        self._running: bool = False
        self.screens = {
            "main_menu": MainMenuScreen(),
            "highscores": HighscoreScreen(),
            "options": OptionsScreen(self.config),
            "game": None,  # GameScreen will be initialized when the game starts
            "win": None,  # WinScreen will be initialized when the game is won
            "exit": ExitScreen()
        }
        self.current_screen_name: str = "main_menu"
        self._last_time = time.time()

    @property
    def config(self) -> Config:
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

    def handle_events(
            self,
            actions: Any
    ) -> None:
        if actions[0] == "QUIT":
            self.set_running(False)
        else:
            new_screen = self.screens[self.current_screen_name].handle_actions(actions[0])
            if new_screen == "game":
                if self._game_engine is None:
                    self._game_engine = GameEngine(self.config)
                else:
                    self._game_engine.reload_level(self.config)

                maze_width, maze_height = self._game_engine.current_level.maze.width, self._game_engine.current_level.maze.height
                maze_layout = self.renderer.get_maze_layout((maze_width, maze_height), self._game_engine)
                sprite_set = SpriteBuilder(self.graphics, maze_layout.cell_size).build()
                self.screens["game"] = GameScreen(self.config, self._game_engine, maze_layout, sprite_set)

            if new_screen is not None:
                self.screens[self.current_screen_name].on_exit()
                self.current_screen_name = new_screen
                self.screens[self.current_screen_name].on_enter()

    def draw_current_screen(self) -> None:

        current_screen = self.screens[self.current_screen_name]

        update_result = current_screen.update(self.get_time_elapsed())
        if update_result == "level":
            maze_width, maze_height = self._game_engine.current_level.maze.width, self._game_engine.current_level.maze.height
            maze_layout = self.renderer.get_maze_layout((maze_width, maze_height), self._game_engine)
            sprite_set = SpriteBuilder(self.graphics, maze_layout.cell_size).build()
            game_screen: GameScreen = self.screens.get("game")
            game_screen.set_maze_layout(maze_layout)
            game_screen.set_sprite_set(sprite_set)

        elif update_result == "win":
            self.current_screen_name = "win"
            self.screens[self.current_screen_name] = WinScreen()

        self.graphics.clear_window((0, 0, 0))  # Clear the window with black color.
        current_screen.draw(self.graphics)
        self.graphics.update_window()  # Display the new frame drawn before.
        
        if self.current_screen_name == "exit":
            self.set_running(False)

    def run(self) -> None:
        """Run the application."""

        self.graphics.open_window()
        self.set_running(True)
        while self.running:
            #  Handle events
            actions = self.graphics.get_actions()
            if len(actions) > 0:
                self.handle_events(actions)

            self.draw_current_screen()
            time.sleep(0.001)

        self.graphics.close_window()