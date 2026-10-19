import pygame
from src.maze import Maze
from src.objects import Asset, PacGum, Pacman


class Game:

    def __init__(
        self,
        maze: Maze,
        surface: pygame.Surface
    ) -> None:
        self.maze = maze
        self.surface = surface

        self.game_assets_path = "assets/in_game/"

        self.border_size_width = self.surface.get_width() / 20
        self.border_size_height = self.surface.get_height() / 20

        self.width_wall = (self.surface.get_width() - self.border_size_width * 2) / self.maze.maze_size_w
        self.height_wall = (self.surface.get_height() - self.border_size_height * 2) / self.maze.maze_size_h

        self.pacgums: list[PacGum] = self._fill_pacgums()

        pacman_asset = Asset(self.game_assets_path + "pacman.svg")
        pacman_asset.resize_asset(self.width_wall / 1.5, self.height_wall / 1.5)

        x = self.border_size_width + (len(self.maze.maze[0]) // 2) * self.width_wall + self.width_wall / 2 - pacman_asset.asset.get_width() / 2
        y = self.border_size_height + (len(self.maze.maze) // 2) * self.height_wall + self.height_wall / 2 - pacman_asset.asset.get_height() / 2

        self.pacman = Pacman(x, y, pacman_asset)

    def _fill_pacgums(self) -> list[int]:

        border_size_width = self.surface.get_width() / 20
        border_size_height = self.surface.get_height() / 20
        width_wall = (self.surface.get_width() - border_size_width * 2) / self.maze.maze_size_w
        height_wall = (self.surface.get_height() - border_size_height * 2) / self.maze.maze_size_h


        pacgums = []
        for line_number, line in enumerate(self.maze.maze):
            for cell_number, cell in enumerate(self.maze.maze[line_number]):
                pacgum_asset = Asset(self.game_assets_path + "pacgum.png")
                pacgum_asset.resize_asset(width_wall / 4, height_wall / 4)

                x = border_size_width + cell_number * width_wall + width_wall / 2 - pacgum_asset.asset.get_width() / 2
                y = border_size_height + line_number * height_wall + height_wall / 2 - pacgum_asset.asset.get_height() / 2

                if self.maze.maze[line_number][cell_number] != 15:
                    pacgums.append(PacGum(x, y, pacgum_asset))

        return (pacgums)

    def game_action(self) -> int:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            return (0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            return (1)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            return (2)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            return (3)
        if keys[pygame.K_F11]:
            return (11)
        return (-1)

    def display_game(self) -> None:

        for pacgum in self.pacgums:
            self.surface.blit(pacgum.asset.asset, (pacgum.x, pacgum.y))
        self.surface.blit(self.pacman.asset.asset, (self.pacman.x, self.pacman.y))
