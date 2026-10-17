import pygame


class Maze:
    def __init__(
        self,
        maze: list[list[int]],
        maze_size_w: int,
        maze_size_h: int
    ):
        self.maze = maze
        self.maze_size_w = maze_size_w
        self.maze_size_h = maze_size_h

    def display_maze(
        self,
        surface: pygame.Surface,
    ) -> None:
        border_size_width = surface.get_width() / 20
        border_size_height = surface.get_height() / 20
        width_wall = (surface.get_width() - border_size_width * 2) / self.maze_size_w
        height_wall = (surface.get_height() - border_size_height * 2) / self.maze_size_h

        for line_index, line in enumerate(self.maze):
            for number_index, number in enumerate(line):
                x0 = border_size_width + number_index * width_wall
                y0 = border_size_height + line_index * height_wall
                x1 = x0 + width_wall
                y1 = y0 + height_wall

                if number >= 8:
                    pygame.draw.line(
                        surface,
                        "white",
                        (x0, y0),
                        (x0, y1)
                    )
                    number -= 8
                if number >= 4:
                    pygame.draw.line(
                        surface,
                        "white",
                        (x0, y1),
                        (x1, y1)
                    )
                    number -= 4
                if number >= 2:
                    pygame.draw.line(
                        surface,
                        "white",
                        (x1, y0),
                        (x1, y1)
                    )
                    number -= 2
                if number >= 1:
                    pygame.draw.line(
                        surface,
                        "white",
                        (x0, y0),
                        (x1, y0)
                    )
                    number -= 1
