from src.engine.level import Level
from src.maze.generator import MazeGenerator
from src.maze.maze import Maze
from src.config.models import Config


class GameEngine:

    def __init__(self, config: Config):
        """Initialize the GameEngine with the given level."""

        maze = MazeGenerator(config.level_1_size, seed=config.level_1_seed)
        self.current_level = Level(Maze(maze.maze))

    def reload_level(self, config: Config) -> None:

        maze = MazeGenerator(config.level_1_size, seed=config.level_1_seed)
        self.current_level = Level(Maze(maze.maze))