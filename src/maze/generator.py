from typing import Any

import mazegenerator
from src.maze.maze import Cell


class MazeGenerationError(Exception):
    pass


class MazeGenerator:
    def __init__(
            self,
            size: list[int],
            seed: int=0
        ) -> None:

        self.maze = self._convert_maze(self._generate_maze(size, seed=seed))

    def _generate_maze(
            self,
            size: list[int],
            seed: int
        ) -> Any:

        return mazegenerator.MazeGenerator(tuple(size), seed=seed, perfect=False).maze

    def _convert_maze(self, maze: list[list[int]]) -> list[list[Cell]]:

        converted_maze = []
        for row in maze:
            converted_row = []
            for cell in row:
                north_wall = bool(cell & 1)
                east_wall = bool(cell & 2)
                south_wall = bool(cell & 4)
                west_wall = bool(cell & 8)
                converted_row.append(Cell(north_wall, east_wall, south_wall, west_wall))
            converted_maze.append(converted_row)

        return converted_maze