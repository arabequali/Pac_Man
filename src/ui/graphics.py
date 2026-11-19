import pygame

from src.maze.maze import Cell


Image = pygame.Surface
Color = tuple[int, int, int] | tuple[int, int, int, int]


class Graphics:
    """The class that handles the graphics of the application (window, images, drawing pixels)."""
    def __init__(
            self,
        ) -> None:
        self._window_title: str = "Pac-Man"
        self._window = None

    @property
    def window_title(self) -> str:
        return self._window_title

    @property
    def window(self) -> pygame.Surface | None:
        return self._window

    def get_window_size(self) -> tuple[int, int]:
        if self._window is not None:
            return self._window.get_size()
        else:
            return (0, 0)

    def open_window(self) -> None:
        pygame.init()
        self._window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(self._window_title)

    def clear_window(self, color: tuple[int, int, int]) -> None:
        self._window.fill(color)

    def update_window(self) -> None:
        pygame.display.flip()

    def get_actions(self) -> list[str]:
        actions = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.append("QUIT")
            elif event.type == pygame.KEYDOWN:
                actions.append(f"KEYDOWN_{pygame.key.name(event.key).upper()}")
            elif event.type == pygame.KEYUP:
                actions.append(f"KEYUP_{pygame.key.name(event.key).upper()}")
        return actions

    def close_window(self) -> None:
        pygame.quit()

    def new_image(
            self,
            width: int,
            height: int,
            transparent: bool = False
        ) -> pygame.Surface:
        """Create an image: opaque black, or fully transparent."""
        if transparent:
            return pygame.Surface((width, height), pygame.SRCALPHA)
        return pygame.Surface((width, height))

    def put_pixel(self, image: pygame.Surface, x: int, y: int, color: tuple[int, int, int]) -> None:
        image.set_at((x, y), color)

    def draw_cell(
            self,
            image: pygame.Surface,
            cell: Cell,
            cell_size: int,
            x: int,
            y: int
        ) -> pygame.Surface:
        """Draw a cell (cell argument) with open/closed walls in a given surface (image argument)"""

        if cell.north_wall:
            for px_x in range(cell_size):
                self.put_pixel(image, px_x + x, 0 + y, (255, 255, 255))
        if cell.east_wall:
            for px_y in range(cell_size):
                self.put_pixel(image, cell_size - 1 + x, px_y + y, (255, 255, 255))
        if cell.south_wall:
            for px_x in range(cell_size):
                self.put_pixel(image, px_x + x, cell_size - 1 + y, (255, 255, 255))
        if cell.west_wall:
            for px_y in range(cell_size):
                self.put_pixel(image, 0 + x, px_y + y, (255, 255, 255))
        return image

    def put_image_in_image(
            self,
            image_dest: pygame.Surface,
            image_src: pygame.Surface,
            x: int,
            y: int
        ) -> None:
        image_dest.blit(image_src, (x, y))

    def put_image(
            self,
            image: pygame.Surface,
            x: int,
            y: int
    ) -> None:
        self.window.blit(image, (x, y))

    def get_string_size(self, text: str, font_size: int) -> tuple[int, int]:
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        return text_surface.get_size()

    def draw_string(self, x: int, y: int, text: str, font_size: int, color: tuple[int, int, int]) -> None:
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self._window.blit(text_surface, (x, y))