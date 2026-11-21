import pygame

from src.maze.maze import Maze, Direction

from src.ui.sprites import GhostColor, GhostLook


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
        self.ghosts: list[Ghost] = [Ghost(corner[0], corner[1], list(GhostColor)[i]) for i, corner in enumerate(corners)]
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

    def __init__(self, x: int, y: int, state: GhostLook | str) -> None:
        super().__init__(x, y)
        self.startx : int = x
        self.starty : int = y
        self.state = state
        self.direction = Direction.EAST

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

    def set_state(self, state: str) -> None:
        self.state = state


class Ghost(Moving):

    def __init__(self, x: int, y: int, color: GhostColor) -> None:
        super().__init__(x, y, GhostLook.NORMAL)
        self.color = color
        self.eaten_timer = None

    def routine(self, pac, maze: Maze):
        prio : list[int] = []
        if self.state == GhostLook.NORMAL:
            prio = self.routineBase(pac)
        elif self.state == GhostLook.EDIBLE:
            prio = self.routineScared(pac)
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
            if i == 0:
                next_dir = Direction.NORTH
            elif i == 1:
                next_dir = Direction.EAST
            elif i == 2:
                next_dir = Direction.SOUTH
            elif i == 3:
                next_dir = Direction.WEST
            if maze.can_move(self.x, self.y, next_dir):
                self.move(next_dir, 1)
                break

    def routineBase(self, pac) -> list[int]:
        prio : list[int] = []
        if pac.x == self.x and pac.y == self.y:
            pac.set_state("dead")
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
            self.set_state(GhostLook.EATEN)
            self.eaten_timer = 0
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
        super().__init__(x, y, "alive")
        self.new_direction = None
        self.direction: Direction | None = Direction.EAST
        self.mouth_open: bool = True
        self.is_super : bool = False
        self.visited : list[list[int]] = []
        self.state = "normal"

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
            self.new_direction = direction
        if maze.can_move(self.x, self.y, self.new_direction):
            self.move(self.new_direction, cell_size)
            if [self.x, self.y] not in self.visited:
                self.visited.append([self.x, self.y]) #desactiver la pacgum a ces coords
            self.set_direction(self.new_direction)
            self.new_direction = None
        elif self.direction and maze.can_move(self.x, self.y, self.direction):
            self.move(self.direction, cell_size)
            if [self.x, self.y] not in self.visited:
                self.visited.append([self.x, self.y])

#dans le programme principal, tous les cycles, appeler toutes les routines
