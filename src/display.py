import pygame
import mazegenerator

from src.maze import Maze
from src.menu import Menu
from src.game import Game

class Display:
    def __init__(
        self,
        window_width: int,
        window_height: int,
    ) -> None:
        self.menu: Menu
        self.maze: Maze
        self.game: Game

        self.window_size_w = window_width
        self.window_size_h = window_height

    def pipeline(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((self.window_size_w, self.window_size_h))
        self.menu = Menu(screen)
        self.maze = Maze(mazegenerator.MazeGenerator((20, 20)).maze, screen)
        self.game = Game(self.maze, screen)

        clock = pygame.time.Clock()

        running = True
        in_menu = True
        in_settings = False
        in_game = False

        cursor_pos = 0
        ticking = 0
        pacmove = -1

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill("black")

            if in_menu:
                key_pressed = self.menu.menu_action()
                if key_pressed == 0 and cursor_pos == 1:
                    cursor_pos -= 1
                elif key_pressed == 1 and cursor_pos == 0:
                    cursor_pos += 1
                elif key_pressed == 2 and cursor_pos == 0:
                    in_game = True
                    in_menu = False
                elif key_pressed == 2 and cursor_pos == 1:
                    in_settings = True
                    in_menu = False
                elif key_pressed == 11 and pygame.Surface.get_flags(screen) == 2164260866:
                    screen = pygame.display.set_mode((self.window_size_w, self.window_size_h))
                elif key_pressed == 11 and pygame.Surface.get_flags(screen) == 16777218:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.menu.display_menu(screen, cursor_pos, ticking)

            elif in_game:
                key_pressed = self.game.game_action()
                if key_pressed >= 0 and key_pressed <= 3:
                    pacmove = key_pressed
                elif key_pressed == 11 and pygame.Surface.get_flags(screen) == 2164260866:
                    screen = pygame.display.set_mode((self.window_size_w, self.window_size_h))
                elif key_pressed == 11 and pygame.Surface.get_flags(screen) == 16777218:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.maze.display_maze()
                if ticking % 10 == 0:
                    self.game.pacman.pacmove(pacmove, self.game.width_wall, self.game.height_wall, self.maze, screen)
                    pacmove = -1
                    key_pressed = -1
                self.game.display_game()

            pygame.display.flip()

            clock.tick(60)
            if ticking < 60:
                ticking += 1
            else:
                ticking = 0

        pygame.quit()
