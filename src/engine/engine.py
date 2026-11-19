from src.engine.level import Level
from src.engine.objects import ObjectSet

from src.maze.generator import MazeGenerator
from src.maze.maze import Maze, Direction

from src.config.models import Config


class GameEngine:

    def __init__(self, config: Config):
        """Initialize the GameEngine with the given level."""

        maze = MazeGenerator(config.level_1_size, seed=config.level_1_seed)
        self.current_level = Level(Maze(maze.maze), config, 0)
        self.level_number = 1
        self.object_set = ObjectSet(self.current_level.maze)
        self.current_level.cell_visited(self.object_set.pacman.x, self.object_set.pacman.y)  # Make the pacman case visited

    def reload_level(self, config: Config) -> None:

        maze = MazeGenerator(config.level_1_size, seed=config.level_1_seed)
        self.current_level = Level(Maze(maze.maze), config, 0)
        self.object_set = ObjectSet(self.current_level.maze)

    def start_routines(self, cell_size: int, pac_dir: Direction = None) -> None:

        self.object_set.pacman.routine(self.current_level.maze, cell_size, pac_dir)  # Pacman routine launched

        x = self.object_set.pacman.x
        y = self.object_set.pacman.y
        if not self.current_level.visited[y][x]:  # Make the pacman case visited and add score
            self.current_level.cell_visited(x, y)
            self.current_level.add_pacgum()

    def next_level(self, config: Config) -> None:

        if self.level_number < config.level_count:
            new_size = [config.level_1_size[0] + config.level_size_increase * (self.level_number - 1), config.level_1_size[1] + config.level_size_increase * (self.level_number - 1)]
            self.current_level = Level(Maze(MazeGenerator(new_size).maze), config, self.current_level.score)
            self.object_set = ObjectSet(self.current_level.maze)
