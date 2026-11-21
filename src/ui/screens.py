from abc import ABC, abstractmethod
from typing import Any

from src.config.models import Config

from src.maze.maze import Cell, Direction

from src.ui.graphics import Graphics
from src.ui.renderer import MazeLayout
from src.ui.sprites import SpriteSet

from src.engine.engine import GameEngine
from src.engine.objects import ObjectSet, GhostLook

from src.scores.highscores import HighscoreManager


MOVE_INTERVAL = 0.15


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
        self._options = ["Start Game", "Highscores", "Instructions", "Options", "Exit"]

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
            elif self._selected_option == self._options.index("Instructions"):
                 return "instructions"
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

    def __init__(
              self,
              highscore_manager: HighscoreManager
    ) -> None:
        super().__init__()
        self._highscores_manager = highscore_manager
        self._highscores_manager.load()
        self.entries = self._highscores_manager.entries

    def handle_actions(self, action: Any) -> str | None:
        if action == "KEYDOWN_ESCAPE":
            return "main_menu"  # Go back to the main menu
        return None

    def update(self, time_elapsed: float) -> None:
        pass

    def draw(self, graphics: Graphics) -> None:

        graphics.draw_string(50, 50, "Highscores :", font_size=40, color=(255, 255, 255))
        for i, score in enumerate(self.entries):
            score_str = f"{i + 1}. {score.name}: {score.score}"
            graphics.draw_string(50, 75 + (i + 1) * 50, score_str, font_size=24, color=(255, 255, 255))

    def on_enter(self):
         self._highscores_manager.load()
         self.entries = self._highscores_manager.entries


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
            if self._selected_option == self._options.index("Back"):
                return "main_menu"  # Go back to the main menu
        elif action == "KEYDOWN_ESCAPE":
            return "main_menu"  # Go back to the main menu

        return None

    def config_change(self, action: Any,) -> None:

        #  level_1_seed
        if self._selected_option == self._options.index("level_1_seed"):
            self._config.change_level_1_seed(action == "KEYDOWN_RIGHT")

        #  level_1_size
        elif self._selected_option == self._options.index("level_1_size"):
            self._config.change_level_1_size(action == "KEYDOWN_RIGHT")

        elif self._selected_option == self._options.index("level_size_increase"):
            self._config.change_level_size_increase(action == "KEYDOWN_RIGHT")

        #  level_count
        elif self._selected_option == self._options.index("level_count"):
            self._config.change_level_count(action == "KEYDOWN_RIGHT")

        #  level_max_time
        elif self._selected_option == self._options.index("level_max_time"):
            self._config.change_level_max_time(action == "KEYDOWN_RIGHT")

        #  lives
        elif self._selected_option == self._options.index("lives"):
            self._config.change_lives(action == "KEYDOWN_RIGHT")

        #  points_per_pacgum
        elif self._selected_option == self._options.index("points_per_pacgum"):
            self._config.change_points_per_pacgum(action == "KEYDOWN_RIGHT")

        #  points_per_super_pacgum
        elif self._selected_option == self._options.index("points_per_super_pacgum"):
                    self._config.change_points_per_super_pacgum(action == "KEYDOWN_RIGHT")
        
        #  points_per_ghosts
        elif self._selected_option == self._options.index("points_per_ghosts"):
                    self._config.change_points_per_ghosts(action == "KEYDOWN_RIGHT")

        #  power_duration
        elif self._selected_option == self._options.index("power_duration"):
                    self._config.change_power_duration(action == "KEYDOWN_RIGHT")

        #  ghost_respawn_time
        elif self._selected_option == self._options.index("ghost_respawn_time"):
                    self._config.change_ghost_respawn_time(action == "KEYDOWN_RIGHT")

        #  cheat_mode
        elif self._selected_option == self._options.index("cheat_mode"):
                    self._config.change_cheat_mode()

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
            maze_layout: MazeLayout,
            sprite_set: SpriteSet,
        ) -> None:
        super().__init__()
        self._config = config
        self._game_engine = game_engine
        self.maze_layout = maze_layout
        self.sprite_set = sprite_set
        self.current_action = None
        self.next_direction = None
        self.timer = 0.0

    def set_maze_layout(self, maze_layout: MazeLayout) -> None:

         self.maze_layout = maze_layout

    def set_sprite_set(self, sprite_set: SpriteSet) -> None:

         self.sprite_set = sprite_set

    def set_config(self, config: Config) -> None:
        self._config = config

    def handle_actions(self, action: Any) -> str | None:

        if action == "KEYDOWN_ESCAPE":
            return "main_menu"

        directions = {
            "KEYDOWN_UP": Direction.NORTH,
            "KEYDOWN_RIGHT": Direction.EAST,
            "KEYDOWN_DOWN": Direction.SOUTH,
            "KEYDOWN_LEFT": Direction.WEST,
        }

        if action in directions:
            self.next_direction = directions[action]

        return None

    def update(self, time_elapsed: float) -> str | None:
        # Update game state here
        self.timer += time_elapsed
        self._game_engine.timer_substract(time_elapsed)
        if self._game_engine.current_level.timer <= 0 or self._game_engine.current_level.lives <= 0:
             return "lose"
        if self._game_engine.current_level.super_timer and self._game_engine.current_level.super_timer - self._game_engine.current_level.timer >= self._config.power_duration:
             self._game_engine.remove_power()

        for ghost in self._game_engine.object_set.ghosts:
             if ghost.eaten_timer:
                  ghost.eaten_timer += time_elapsed
                  if ghost.eaten_timer >= self._config.ghost_respawn_time:
                    ghost.state = GhostLook.NORMAL

        if self.timer >= MOVE_INTERVAL:
            self.timer -= MOVE_INTERVAL

            if self.current_action == "KEYDOWN_N" and self._config.cheat_mode:
                for row in range(len(self._game_engine.current_level.visited)):
                      for cell in range(len(self._game_engine.current_level.visited[0])):
                           self._game_engine.current_level.visited[row][cell] = True

            if self._game_engine.current_level.all_visited():
                 if self._game_engine.level_number == 10:
                      return "win"
                 self._game_engine.level_number += 1
                 self._game_engine.next_level(self._config)
                 return "level"

            if self._game_engine.object_set.pacman.state != "dead":
                self._game_engine.start_routines(
                    self.maze_layout.cell_size,
                    self.next_direction
                )
            else:
                self._game_engine.pacman_died()
            self._game_engine.object_set.pacman.mouth_open = not self._game_engine.object_set.pacman.mouth_open

        return None

    def draw(
            self,
            graphics: Graphics
        ) -> None:
        """Draw the whole game."""

        object_set = self._game_engine.object_set

        #  Drawing the maze
        maze_image = self.maze_layout.maze_image
        width_offset = self.maze_layout.width_offset // 2
        height_offset = self.maze_layout.height_offset // 2
        graphics.put_image(maze_image, width_offset, height_offset)

        white = (255, 255, 255)

        score_str = f"Score: {self._game_engine.current_level.score}"
        score_size_x = graphics.get_string_size(score_str, 30)[0]

        level_str = f"Level: {self._game_engine.level_number}"
        level_size_x = graphics.get_string_size(level_str, 30)[0]

        timer_str = f"Timer: {int(self._game_engine.current_level.timer)}"
        timer_size_x = graphics.get_string_size(timer_str, 30)[0]

        lives_str = f"Lives: {self._game_engine.current_level.lives}"

        graphics.draw_string(width_offset, height_offset // 2, f"Score: {self._game_engine.current_level.score}", 30, white)
        graphics.draw_string(width_offset + 2 * score_size_x, height_offset // 2, level_str, 30, white)
        graphics.draw_string(width_offset + 2 * score_size_x + 2 * level_size_x, height_offset // 2, timer_str, 30, white)
        graphics.draw_string(width_offset + 2 * score_size_x + 2 * level_size_x + 2 * timer_size_x, height_offset // 2, lives_str, 30, white)

        graphics.draw_string(width_offset, graphics.window.get_size()[1] - height_offset // 2, "Cheat commands: Next Level - N", 30, (255, 255, 255))

        #  Drawing PacGums
        for pacgum in object_set.pacgums:
                pacgum_pos_x, pacgum_pos_y = self.maze_layout.convert_maze_coordinates(pacgum.x, pacgum.y)
                if not self._game_engine.current_level.visited[pacgum.y][pacgum.x]:
                    graphics.put_image(self.sprite_set.pacgum, pacgum_pos_x, pacgum_pos_y)

        #  Drawing Super Pacgums
        for super_pacgum in object_set.super_pacgums:
             s_pacgum_x, s_pacgum_y = self.maze_layout.convert_maze_coordinates(super_pacgum.x, super_pacgum.y)
             if not self._game_engine.current_level.visited[super_pacgum.y][super_pacgum.x]:
                 graphics.put_image(self.sprite_set.super_pacgum, s_pacgum_x, s_pacgum_y)

        #  Drawing PacMan RIDING THE WAVE
        pacman = object_set.pacman

        progress = min(self.timer / MOVE_INTERVAL, 1.0)

        if pacman.state == "dead":
            pacman_draw_x = pacman.x
            pacman_draw_y = pacman.y
        else:
            pacman_draw_x = (
                pacman.previous_x
                + (pacman.x - pacman.previous_x) * progress
            )

            pacman_draw_y = (
                pacman.previous_y
                + (pacman.y - pacman.previous_y) * progress
            )

        pacman_pos_x, pacman_pos_y = self.maze_layout.convert_maze_coordinates(
            pacman_draw_x,
            pacman_draw_y
        )

        graphics.put_image(
            self.sprite_set.get_pacman(
                pacman.direction,
                pacman.mouth_open
            ),
            round(pacman_pos_x),
            round(pacman_pos_y)
        )

        #  Drawing Ghosts RIDING THE WAVE TOOOOO
        for ghost in object_set.ghosts:
            ghost_draw_x = (
                ghost.previous_x
                + (ghost.x - ghost.previous_x) * progress
            )

            ghost_draw_y = (
                ghost.previous_y
                + (ghost.y - ghost.previous_y) * progress
            )
            ghost_pos_x, ghost_pos_y = self.maze_layout.convert_maze_coordinates(
                        ghost_draw_x,
                        ghost_draw_y
                    )
            graphics.put_image(
                        self.sprite_set.get_ghost(
                            ghost.color,
                            ghost.state,
                            ghost.direction
                        ),
                        round(ghost_pos_x),
                        round(ghost_pos_y)
                    )

    def on_enter(
            self,
        ) -> None:
        pass  #  Initialize game state when entering the game screen


class WinScreen(Screen):

     def __init__(
               self,
               score: int,
               highscore_manager: HighscoreManager
     ) -> None:

          self.score = score
          self.highscore_manager = highscore_manager
          self.current_action = None
          self.string_buffer: str = ""

     def handle_actions(self, action: Any) -> str | None:

        if action == "KEYDOWN_ESCAPE":
           return "main_menu"
        elif action == "KEYDOWN_RETURN" and self.highscore_manager.qualifies(self.score) and len(self.string_buffer):
             self.highscore_manager.add(self.string_buffer, self.score)
             return "main_menu"
        elif action == "KEYDOWN_BACKSPACE":
            self.string_buffer = self.string_buffer[:-1]
        elif action.startswith("KEYDOWN_") and len(self.string_buffer) <= 10:
             self.typing_name(action)

     def typing_name(self, action: Any) -> None:

          if action == "KEYDOWN_SPACE":
               self.string_buffer += " "
               return
          letter_pressed = str(action).replace("KEYDOWN_", "")
          if len(letter_pressed) == 1:
              self.string_buffer += letter_pressed

     def update(self, time_elapsed: float) -> None:
          pass

     def draw(self, graphics: Graphics) -> None:

          if not self.current_action:
               
               window_x, window_y = graphics.window.get_size()

               win_str_size = graphics.get_string_size("You won !", 100)
               win_str_x = window_x // 2 - win_str_size[0] // 2
               win_str_y = window_y // 2 - win_str_size[1]

               score_str = f"Score: {self.score}"
               score_str_size = graphics.get_string_size(score_str, 100)
               score_str_x = window_x // 2 - score_str_size[0] // 2
               score_str_y = window_y // 2 - score_str_size[1]

               username_str_size = graphics.get_string_size(self.string_buffer, 90)
               username_str_x = window_x // 2 - username_str_size[0] // 2
               username_str_y = window_y // 2 - username_str_size[1] + win_str_size[1] * 2

               commands_str = "Escape to quit without saving | Enter to save your name" if self.highscore_manager.qualifies(self.score) else "Escape to quit"
               commands_str_size = graphics.get_string_size(commands_str, 60)
               commands_str_x = window_x // 2 - commands_str_size[0] // 2
               commands_str_y = window_y // 2 - username_str_size[1] + win_str_size[1] * 2 + username_str_size[1] * 2

               graphics.draw_string(win_str_x, window_y // 2 - win_str_y, "You won !", 100, (255, 255, 0))
               graphics.draw_string(score_str_x, score_str_y, score_str, 100, (255, 255, 255))
               if self.highscore_manager.qualifies(self.score):
                   graphics.draw_string(username_str_x, username_str_y, self.string_buffer, 90, (255, 255, 255))
               else:
                    test_str = "You are not in the top 10!"
                    test_str_size = graphics.get_string_size(test_str, 90)
                    graphics.draw_string(window_x // 2 - test_str_size[0] // 2, window_y // 2 - test_str_size[1] + win_str_size[1] * 2, test_str, 90, (255, 255, 255))
               graphics.draw_string(commands_str_x, commands_str_y, commands_str, 60, (255, 255, 255))


class LoseScreen(Screen):

     def __init__(
               self,
               score: int,
               highscore_manager
     ) -> None:

          self.score = score
          self.highscore_manager = highscore_manager
          self.current_action = None
          self.string_buffer: str = ""

     def handle_actions(self, action: Any) -> str | None:

        if action == "KEYDOWN_ESCAPE":
           return "main_menu"
        elif action == "KEYDOWN_RETURN":
             self.highscore_manager.add(self.string_buffer, self.score)
             return "main_menu"
        elif action == "KEYDOWN_BACKSPACE":
            self.string_buffer = self.string_buffer[:-1]
        elif action.startswith("KEYDOWN_") and len(self.string_buffer) <= 10:
             self.typing_name(action)

     def typing_name(self, action: Any) -> None:

          if action == "KEYDOWN_SPACE":
               self.string_buffer += " "
               return
          letter_pressed = str(action).replace("KEYDOWN_", "")
          if len(letter_pressed) == 1:
              self.string_buffer += letter_pressed

     def update(self, time_elapsed: float) -> None:
          pass

     def draw(self, graphics: Graphics) -> None:

        window_x, window_y = graphics.window.get_size()

        win_str_size = graphics.get_string_size("Game Over...", 100)
        win_str_x = window_x // 2 - win_str_size[0] // 2
        win_str_y = window_y // 2 - win_str_size[1]

        score_str_size = graphics.get_string_size(f"Score: {self.score}", 100)
        score_str_x = window_x // 2 - score_str_size[0] // 2
        score_str_y = window_y // 2 - score_str_size[1]

        username_str_size = graphics.get_string_size(self.string_buffer, 90)
        username_str_x = window_x // 2 - username_str_size[0] // 2
        username_str_y = window_y // 2 - username_str_size[1] + win_str_size[1] * 2

        commands_str = "Escape to quit without saving | Enter to save your name"
        commands_str_size = graphics.get_string_size(commands_str, 60)
        commands_str_x = window_x // 2 - commands_str_size[0] // 2
        commands_str_y = window_y // 2 - username_str_size[1] + win_str_size[1] * 2 + username_str_size[1] * 2

        graphics.draw_string(win_str_x, window_y // 2 - win_str_y, "Game Over...", 100, (255, 255, 0))
        graphics.draw_string(score_str_x, score_str_y, f"Score: {self.score}", 100, (255, 255, 255))
        graphics.draw_string(username_str_x, username_str_y, self.string_buffer, 90, (255, 255, 255))
        graphics.draw_string(commands_str_x, commands_str_y, commands_str, 60, (255, 255, 255))


class InstructionScreen(Screen):

    def __init__(self) -> None:
          super().__init__()
          self.strings = [
               "Move up: up_arrow",
               "Move right: right_arrow",
               "Move down: down_arrow",
               "Move left: left_arrow",
               "Other commands are given in game."
          ]

    def handle_actions(self, action: Any) -> str | None:
        if action == "KEYDOWN_ESCAPE":
             return "main_menu"

    def update(self, time_elapsed: float) -> None:
        pass

    def draw(self, graphics: Graphics) -> None:

        window_size = graphics.window.get_size()
        for i, string in enumerate(self.strings):
            string_size_x = graphics.get_string_size(string, 30)[0]
            graphics.draw_string(window_size[0] // 2 - string_size_x // 2, 50 + i * 30, string, 30, (255, 255, 255))