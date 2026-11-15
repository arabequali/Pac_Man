from enum import Enum


class Direction(Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


class Cell:

    def __init__(
            self,
            north_wall: bool,
            east_wall: bool,
            south_wall: bool,
            west_wall: bool
        ) -> None:
        self.north_wall: bool = north_wall
        self.east_wall: bool = east_wall
        self.south_wall: bool = south_wall
        self.west_wall: bool = west_wall


class Maze:

    def __init__(
            self,
            maze: list[list[Cell]],
            seed: int = 0
    ) -> None:
        self._width, self._height = len(maze[0]), len(maze)
        self._maze_grid = maze

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def maze_grid(self) -> list[list[Cell]]:
        return self._maze_grid

    def get_cell(self, x: int, y: int) -> Cell:
        """Get cell at coordinates (x, y)"""

        if not self.is_within_bounds(x, y):
                raise IndexError("Cell coordinates out of bounds")

        return self._maze_grid[y][x]

    def is_within_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates (x, y) are within maze bounds"""

        return 0 <= x < self._width and 0 <= y < self._height

    def cell_sealed(self, x: int, y: int) -> bool:
        """Verify if cell is sealed (has walls on all sides)"""

        if not self.is_within_bounds(x, y):
                raise IndexError("Cell coordinates out of bounds")
    
        cell = self.get_cell(x, y)
        return cell.north_wall and cell.east_wall and cell.south_wall and cell.west_wall

    def can_move(self, x: int, y: int, direction: Direction) -> bool:
        """Check if movement is possible in the given direction from the cell at (x, y)"""

        if not self.is_within_bounds(x, y):
            raise IndexError("Cell coordinates out of bounds")

        cell = self.get_cell(x, y)
        if direction == Direction.NORTH:
            return not cell.north_wall
        elif direction == Direction.EAST:
            return not cell.east_wall
        elif direction == Direction.SOUTH:
            return not cell.south_wall
        elif direction == Direction.WEST:
            return not cell.west_wall