from src.maze.maze import Maze
from src.config.models import Config


class Level:

    def __init__(
            self,
            maze: Maze,
            config: Config,
            score: int,
            lives: int
    ):
        """Initialize the Level with every needed component."""
        self.maze: Maze = maze
        self.visited: list[list[bool]] = self._build_visited()
        self.score: int = score
        self.lives: int = lives
        self.timer = 120

        self.score_pacgum = config.points_per_pacgum
        self.score_super = config.points_per_super_pacgum
        self.score_ghost = config.points_per_ghosts

    def _build_visited(self) -> list[list[bool]]:

        visited = []
        for y in range(len(self.maze.maze_grid)):
            visited.append([False if not self.maze.cell_sealed(x, y) else True for x in range(len(self.maze.maze_grid))])

        return visited

    def cell_visited(self, x: int, y: int) -> None:

        self.visited[y][x] = True

    def add_pacgum(self) -> None:

        self.score += self.score_pacgum

    def all_visited(self) -> bool:

        for row in self.visited:
            for cell in row:
                if not cell:
                    return False

        return True