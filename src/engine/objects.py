import pygame
from src.maze.maze import Maze


class Asset():

    def __init__(
        self,
        asset_path: str,
        size_w: int = None,
        size_h: int = None
    ) -> None:
        self.asset_path : str = asset_path
        self.size_w: int = size_w
        self.size_h: int = size_h
        self.asset = self._load_asset()

    def _load_asset(self) -> None:
        image = pygame.image.load(self.asset_path)
        if (self.size_w) and (self.size_h):
            image = pygame.transform.scale(image, (self.size_w, self.size_h))
        return (image)

    def resize_asset(
        self,
        width: int,
        height: int
    ) -> None:
        self.asset = pygame.transform.scale(self.asset, (width, height))

    def display_asset(
        self,
        surface: pygame.Surface,
        display_x: int,
        display_y: int
    ) -> None:
        surface.blit(self.asset, (surface.get_width() / display_x - self.asset.get_width() / 2, surface.get_height() / display_y - self.asset.get_height() / 2))

class Objects():

    def __init__(self, x: int, y: int, asset: Asset) -> None:
        self.x : int = x
        self.y : int = y
        self.asset : str = asset


class Static(Objects):

    def __init__(self, x: int, y: int, asset: Asset, score: int) -> None:
        super().__init__(x, y, asset)
        self.active : bool = True
        self.score : int = score


class PacGum(Static):

    def __init__(self, x: int, y: int, asset: Asset) -> None:
        super().__init__(x, y, asset, 100)


class SuperPacGum(Static):

    def __init__(x: int, y: int, asset: Asset) -> None:
        super.__init__(x, y, asset, 500)


class Moving(Objects):

    def __init__(self, x: int, y: int, asset: Asset) -> None:
        super().__init__(x, y, asset)
        self.startx : int = x
        self.starty : int = y

    def move(self, direction: int) -> None:
        match direction:
                case 0:
                    self.x -= 1
                case 1:
                    self.y += 1
                case 2:
                    self.x += 1
                case 3:
                    self.y -= 1



class Ghost(Moving):

    def __init__(x: int, y: int, asset: Asset) -> None:
        super.__init__(x, y, asset)
        self.state : str = "Base"

    def routine(self, pac: Pacman, maze: Maze):
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

    def routineBase(self, pac:Pacman) -> list[int]:
        prio : list[int] = []
        if pac.x == self.x and pac.y == self.y:
            #kill pacman
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

    def routineScared() -> None:
        prio : list[int] = []
        if pac.x == self.x and pac.y == self.y:
            #kill ghost
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

    def __init__(self, x: int, y: int, asset: Asset) -> None:
        super().__init__(x, y, asset)
        self.direction : int = 0

    def pacmove(self, key_pressed: int, width_wall: int, height_wall: int, maze) -> None:
        if key_pressed == 0 and maze.can_go(self.x, self.y, 0):
            self.y -= height_wall
        if key_pressed == 1 and maze.can_go(self.x, self.y, 1):
            self.x += width_wall
        if key_pressed == 2 and maze.can_go(self.x, self.y, 2):
            self.y += height_wall
        if key_pressed == 3 and maze.can_go(self.x, self.y, 3):
            self.x -= width_wall

    #direction: up = 0, right = 1, down = 2, left = 3
    def set_direction(dir: int) -> None:
        if (dir < 0 or dir > 3):
            print("invalid direction value")
        else:
            self.direction = dir
        

    def routine(self, maze: Maze):
        if maze.can_go(x, y, self.direction):
            self.move(self.direction)
        else:
            self.set_direction((self.direction + 2) % 4)
            if maze.can_go(x, y, self.direction):
                self.move(self.direction)
            else:
                self.set_direction((self.direction + 2) % 4)



#dans le programme principal, tous les cycles, appeler toutes les routines
