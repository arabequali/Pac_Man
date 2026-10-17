import pygame
from src.objects import Asset
from src.maze import Maze


class Menu:
    def __init__(
        self,
        maze: Maze,
    ) -> None:
        self.maze = maze

        menu_assets_path = "assets/main_menu/"

        self.pacman_logo = Asset(menu_assets_path + "pacman_logo.svg")

        self.play_button = Asset(menu_assets_path + "play_button.png")
        self.play_button_cursor = Asset(menu_assets_path + "play_button_cursor.png")
        self.settings_button = Asset(menu_assets_path + "settings_button.png")
        self.settings_button_cursor = Asset(menu_assets_path + "settings_button_cursor.png")

        self.play_button.resize_asset(150, 50)
        self.play_button_cursor.resize_asset(150, 50)
        self.settings_button.resize_asset(150, 50)
        self.settings_button_cursor.resize_asset(150, 50)

    def menu_action(self) -> int:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            return (0)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            return (1)
        if keys[pygame.K_RETURN]:
            return (2)
        if keys[pygame.K_F11]:
            return (11)

    def display_menu(
        self,
        surface: pygame.Surface,
        cursor_pos: int,
        ticking: int
    ) -> None:

        if cursor_pos == 0 and ticking < 45:
            self.play_button_cursor.display_asset(surface, 2, 1.5)
            self.settings_button.display_asset(surface, 2, 1.3)
        elif cursor_pos == 0 and ticking >= 45:
            self.play_button.display_asset(surface, 2, 1.5)
            self.settings_button.display_asset(surface, 2, 1.3)
        elif cursor_pos == 1 and ticking < 45:
            self.play_button.display_asset(surface, 2, 1.5)
            self.settings_button_cursor.display_asset(surface, 2, 1.3)
        elif cursor_pos == 1 and ticking >= 45:
            self.play_button.display_asset(surface, 2, 1.5)
            self.settings_button.display_asset(surface, 2, 1.3)

        self.pacman_logo.display_asset(surface, 2, 3)
