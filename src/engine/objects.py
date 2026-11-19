import pygame

from src.maze.maze import Maze, Direction


Cell = tuple[int, int]  #  (x, y) in maze coordinates, y grows downwards


class ObjectSet:
    """Pac-Man, the four ghosts and every pellet of one maze."""

    def __init__(self, maze: Maze) -> None:
        """Place every object on the maze."""
        open_cells = self._open_cells(maze)
        if not open_cells:
            raise ValueError("The maze has no open cell.")

        spawn = self._nearest(open_cells, maze.width // 2, maze.height // 2)
        right, bottom = maze.width - 1, maze.height - 1
        corners = [
            self._nearest(open_cells, x, y)
            for x, y in ((0, 0), (right, 0), (0, bottom), (right, bottom))
        ]
        taken = {spawn, *corners}

        self.pacman: Pacman = Pacman(spawn[0], spawn[1])
        self.ghosts: list[Ghost] = [Ghost(x, y) for x, y in corners]
        self.super_pacgums: list[SuperPacGum] = [
            SuperPacGum(x, y) for x, y in corners
        ]
        self.pacgums: list[PacGum] = [
            PacGum(x, y) for x, y in open_cells if (x, y) not in taken
        ]

    @property
    def remaining_pacgums(self) -> int:
        """Number of pacgums not eaten yet"""

        return sum(1 for pacgum in self.pacgums if pacgum.active)

    @staticmethod
    def _open_cells(maze: Maze) -> list[Cell]:
        """Every cell that is not sealed"""

        return [
            (x, y)
            for y in range(maze.height)
            for x in range(maze.width)
            if not maze.cell_sealed(x, y)
        ]

    @staticmethod
    def _nearest(cells: list[Cell], target_x: int, target_y: int) -> Cell:
        """The cell closest to a target."""

        return min(
            cells,
            key=lambda c: (abs(c[0] - target_x) + abs(c[1] - target_y),
                           c[1], c[0]),
        )

    @staticmethod
    def _open_cells(maze: Maze) -> list[Cell]:
        """Every cell that is not sealed, row by row."""
        return [
            (x, y)
            for y in range(maze.height)
            for x in range(maze.width)
            if not maze.cell_sealed(x, y)
        ]


class Objects():

    def __init__(self, x: int, y: int) -> None:
        self.x : int = x
        self.y : int = y


class Static(Objects):

    def __init__(self, x: int, y: int, score: int) -> None:
        super().__init__(x, y)
        self.active : bool = True
        self.score : int = score


class PacGum(Static):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 100)


class SuperPacGum(Static):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 500)


class Moving(Objects):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.startx : int = x
        self.starty : int = y

    def move(
            self,
            direction: Direction,
            cell_size: int
        ) -> None:
        if direction == Direction.NORTH:
            self.y -= 1
        elif direction == Direction.EAST:
            self.x += 1
        elif direction == Direction.SOUTH:
            self.y += 1
        elif direction == Direction.WEST:
            self.x -= 1


class Ghost(Moving):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.state : str = "Base"

    def routine(self, pac, maze: Maze):
        prio : list[int] = []
        if self.state == "Base":
            self.routineBase(pac)
        else:
            self.routineScared(pac)
        match prio:
            case [0, 0, 0]:
                prio = [1, 2, 0, 3]
            case [0, 0, 1]:
                prio = [3, 2, 0, 1]
            case [0, 1, 0]:
                prio = [1, 0, 2, 3]
            case [0, 1, 1]:
                prio = [3, 0, 2, 1]
            case [1, 0, 0]:
                prio = [2, 1, 3, 0]
            case [1, 0, 1]:
                prio = [2, 3, 1, 0]
            case [1, 1, 0]:
                prio = [0, 1, 3, 2]
            case [1, 1, 1]:
                prio = [0, 3, 1, 2]
        for i in prio:
            if maze.can_go(self.x, self.y, i):
                self.move(i)
                break

    def routineBase(self, pac) -> list[int]:
        prio : list[int] = []
        if pac.x == self.x and pac.y == self.y:
            #  kill pacman
            pass
        if abs(self.x - pac.x) < abs(self.y - pac.y):
            prio.append(0)
        else:
            prio.append(1)
        if self.x < pac.x:
            prio.append(0)
        else:
            prio.append(1)
        if self.y < pac.y:
            prio.append(0)
        else:
            prio.append(1)
        return(prio)

    def routineScared(self, pac) -> list[int]:
        prio : list[int] = []
        if pac.x == self.x and pac.y == self.y:
            #kill ghost
            pass
        if abs(self.x - pac.x) < abs(self.y - pac.y):
            prio.append(0)
        else:
            prio.append(1)
        if self.x < pac.x:
            prio.append(1)
        else:
            prio.append(0)
        if self.y < pac.y:
            prio.append(1)
        else:
            prio.append(0)
        return(prio)

class Pacman(Moving):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.direction: Direction | None = Direction.EAST
        self.mouth_open: bool = True
        self.is_super = False

    #direction: up = 0, right = 1, down = 2, left = 3
    def set_direction(self, dir: Direction) -> None:
        self.direction = dir

    def routine(
            self,
            maze: Maze,
            cell_size: int,
            direction: Direction = None
        ):

        if direction:
            self.set_direction(direction)
        if maze.can_move(self.x, self.y, self.direction):
            self.move(self.direction, cell_size)

#dans le programme principal, tous les cycles, appeler toutes les routines
