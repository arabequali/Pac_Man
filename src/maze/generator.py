from collections import deque
from typing import Any

from src.maze.maze import Cell, Direction, Maze

MIN_SIZE = 3
MAX_CELL_VALUE = 15  # four wall bits: north 1, east 2, south 4, west 8

# How one step in each direction changes (x, y); y grows downwards.
_STEPS: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}


class MazeGenerationError(Exception):
    """Raised when a maze cannot be generated or is not usable."""


class MazeGenerator:
    """Generate a maze with the assigned package and validate it.

    After construction, `maze` holds a grid of cells (grid[y][x]) that has
    passed every check. If anything is wrong, MazeGenerationError is raised
    and no maze is exposed.
    """

    def __init__(self, size: list[int], seed: int = 0) -> None:
        """Generate and validate a maze.

        Args:
            size: [width, height] in cells, each at least MIN_SIZE.
            seed: Same seed gives the same maze. The package treats 0 as
                "random", so 0 is NOT reproducible.

        Raises:
            MazeGenerationError: bad arguments, package failure, or a
                maze that fails validation.
        """
        self._check_arguments(size, seed)
        self._width: int = size[0]
        self._height: int = size[1]
        raw = self._generate_maze(size, seed)
        self._check_raw_maze(raw)
        self.maze: list[list[Cell]] = self._convert_maze(raw)
        self._check_maze(self.maze)

    # ---- step 1: arguments --------------------------------------------

    @staticmethod
    def _check_arguments(size: list[int], seed: int) -> None:
        """Reject arguments the package would mishandle silently."""
        if len(size) != 2 or not all(
            isinstance(v, int) and not isinstance(v, bool) for v in size
        ):
            raise MazeGenerationError(
                "Maze size must be two integers: [width, height]."
            )
        if size[0] < MIN_SIZE or size[1] < MIN_SIZE:
            raise MazeGenerationError(
                f"Maze size {size[0]}x{size[1]} is too small "
                f"(minimum {MIN_SIZE}x{MIN_SIZE})."
            )
        if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
            raise MazeGenerationError(
                "Maze seed must be an integer greater than or equal to 0."
            )

    # ---- step 2: call the package -------------------------------------

    def _generate_maze(self, size: list[int], seed: int) -> Any:
        """Call the package and turn every failure into our own error."""
        try:
            import mazegenerator
        except ImportError as e:
            raise MazeGenerationError(
                "The maze package 'mazegenerator' is not installed."
            ) from e
        try:
            return mazegenerator.MazeGenerator(
                (size[0], size[1]), perfect=False, seed=seed
            ).maze
        except Exception as e:  # third-party code: anything can go wrong
            raise MazeGenerationError(
                f"The maze package failed ({type(e).__name__}): {e}"
            ) from e

    # ---- step 3: check the raw output ---------------------------------

    def _check_raw_maze(self, raw: Any) -> None:
        """Check the package output: right shape, right values."""
        if not isinstance(raw, list) or len(raw) != self._height:
            rows = len(raw) if isinstance(raw, list) else "?"
            raise MazeGenerationError(
                f"Expected {self._height} rows, the package gave {rows}."
            )
        for y, row in enumerate(raw):
            if not isinstance(row, list) or len(row) != self._width:
                raise MazeGenerationError(
                    f"Row {y} should have {self._width} cells."
                )
            for x, value in enumerate(row):
                if (isinstance(value, bool) or not isinstance(value, int)
                        or not 0 <= value <= MAX_CELL_VALUE):
                    raise MazeGenerationError(
                        f"Cell ({x}, {y}) has an invalid value: {value!r}."
                    )

    # ---- step 4: convert ----------------------------------------------

    @staticmethod
    def _convert_maze(raw: list[list[int]]) -> list[list[Cell]]:
        """Turn the integer grid into a grid of Cell (bit set = wall)."""
        return [
            [
                Cell(
                    north_wall=bool(value & 1),
                    east_wall=bool(value & 2),
                    south_wall=bool(value & 4),
                    west_wall=bool(value & 8),
                )
                for value in row
            ]
            for row in raw
        ]

    # ---- step 5: check the maze itself --------------------------------

    def _check_maze(self, grid: list[list[Cell]]) -> None:
        """Run the three structural checks, in order."""
        self._check_borders(grid)
        self._check_walls_match(grid)
        self._check_connected(grid)

    @staticmethod
    def _check_borders(grid: list[list[Cell]]) -> None:
        """The outer edge must be closed, or entities could leave."""
        height, width = len(grid), len(grid[0])
        for x in range(width):
            if not grid[0][x].north_wall:
                raise MazeGenerationError(f"Cell ({x}, 0): top edge open.")
            if not grid[height - 1][x].south_wall:
                raise MazeGenerationError(
                    f"Cell ({x}, {height - 1}): bottom edge open."
                )
        for y in range(height):
            if not grid[y][0].west_wall:
                raise MazeGenerationError(f"Cell (0, {y}): left edge open.")
            if not grid[y][width - 1].east_wall:
                raise MazeGenerationError(
                    f"Cell ({width - 1}, {y}): right edge open."
                )

    @staticmethod
    def _check_walls_match(grid: list[list[Cell]]) -> None:
        """A wall between two cells must be seen the same from both sides.

        Otherwise one side could walk through while the other sees a wall.
        """
        height, width = len(grid), len(grid[0])
        for y in range(height):
            for x in range(width):
                if (x + 1 < width
                        and grid[y][x].east_wall != grid[y][x + 1].west_wall):
                    raise MazeGenerationError(
                        f"Wall mismatch between ({x}, {y}) and "
                        f"({x + 1}, {y})."
                    )
                if (y + 1 < height and
                        grid[y][x].south_wall != grid[y + 1][x].north_wall):
                    raise MazeGenerationError(
                        f"Wall mismatch between ({x}, {y}) and "
                        f"({x}, {y + 1})."
                    )

    @staticmethod
    def _check_connected(grid: list[list[Cell]]) -> None:
        """Every non-sealed cell must be reachable from every other.

        Sealed cells (four walls) are the package's '42' pattern: they are
        not part of the playable area, so they are skipped.
        """
        maze = Maze(grid)
        open_cells = [
            (x, y)
            for y in range(maze.height)
            for x in range(maze.width)
            if not maze.cell_sealed(x, y)
        ]
        if not open_cells:
            raise MazeGenerationError("The maze has no open cell.")

        start = open_cells[0]
        seen = {start}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            for direction, (dx, dy) in _STEPS.items():
                nxt = (x + dx, y + dy)
                if nxt not in seen and maze.can_move(x, y, direction):
                    seen.add(nxt)
                    queue.append(nxt)

        unreachable = [cell for cell in open_cells if cell not in seen]
        if unreachable:
            raise MazeGenerationError(
                f"{len(unreachable)} cell(s) cannot be reached, "
                f"for example {unreachable[0]}."
            )