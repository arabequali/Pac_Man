from src.maze.maze import Maze


class Level:

    def __init__(
            self,
            maze: Maze
    ):
        """Initialize the Level with every needed component."""
        self.maze = maze