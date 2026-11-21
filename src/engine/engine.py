from src.engine.level import Level
from src.engine.objects import ObjectSet, GhostLook

from src.maze.generator import MazeGenerator
from src.maze.maze import Maze, Direction

from src.config.models import Config


class GameEngine:

    def __init__(self, config: Config):
        """Initialize the GameEngine with the given level."""

        maze = MazeGenerator(config.level_1_size, seed=config.level_1_seed)
        self.current_level = Level(Maze(maze.maze), config, 0, config.lives)
        self.level_number = 1
        self.object_set = ObjectSet(self.current_level.maze)
        self.current_level.cell_visited(self.object_set.pacman.x, self.object_set.pacman.y)  # Make the pacman case visited

    def reload_level(self, config: Config) -> None:

        maze = MazeGenerator(config.level_1_size, seed=config.level_1_seed)
        self.current_level = Level(Maze(maze.maze), config, 0, config.lives)
        self.object_set = ObjectSet(self.current_level.maze)

    def is_corner(self, x: int, y: int) -> bool:
        if x == 0 and (y == 0 or y == len(self.current_level.maze._maze_grid) - 1):
            return True
        elif x == len(self.current_level.maze.maze_grid) - 1 and (y == 0 or y == len(self.current_level.maze.maze_grid) - 1):
            return True
        return False

    def start_routines(self, cell_size: int, pac_dir: Direction = None) -> None:

        for ghost in self.object_set.ghosts:
            ghost.routine(self.object_set.pacman, self.current_level.maze)

        self.object_set.pacman.routine(self.current_level.maze, cell_size, pac_dir)  # Pacman routine launched

        if self.object_set.pacman.state == "dead":
            self.current_level.lives -= 1

        x = self.object_set.pacman.x
        y = self.object_set.pacman.y
        if not self.current_level.visited[y][x] and not self.is_corner(x, y):  # Make the pacman case visited and add score
            self.current_level.cell_visited(x, y)
            self.current_level.add_pacgum()
        elif not self.current_level.visited[y][x] and self.is_corner(x, y):
            self.current_level.cell_visited(x, y)
            self.current_level.add_super()
            self.current_level.super_timer = self.current_level.timer
            for ghost in self.object_set.ghosts:
                ghost.state = GhostLook.EDIBLE

    def remove_power(self) -> None:
        self.current_level.super_timer = None
        for ghost in self.object_set.ghosts:
            ghost.state = GhostLook.NORMAL

    def next_level(self, config: Config) -> None:

        if self.level_number < config.level_count:
            new_size = [config.level_1_size[0] + config.level_size_increase * (self.level_number - 1), config.level_1_size[1] + config.level_size_increase * (self.level_number - 1)]
            self.current_level = Level(Maze(MazeGenerator(new_size).maze), config, self.current_level.score, self.current_level.lives)
            self.object_set = ObjectSet(self.current_level.maze)

    def timer_substract(self, time_elapsed: int) -> None:

        self.current_level.timer -= time_elapsed

    def pacman_died(self) -> None:

        obj_set = self.object_set
        obj_set.pacman.x, obj_set.pacman.y = obj_set.pacman.startx, obj_set.pacman.starty

        for ghost in obj_set.ghosts:
            ghost.x, ghost.y = ghost.startx, ghost.starty

        obj_set.pacman.state = "normal"

    def ghost_died(self) -> None:

        pacman = self.object_set.pacman
        for ghost in self.object_set.ghosts:
            if ghost.x == pacman.x and ghost.y == pacman.y:
                ghost.state = GhostLook.EATEN
                self.current_level.score += self.current_level.add_ghost()