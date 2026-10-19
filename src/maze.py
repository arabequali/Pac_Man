import pygame


class Maze:
    def __init__(
        self,
        maze: list[list[int]],
        surface: pygame.Surface
    ):
        self.maze = maze

        self.maze_size_w = len(maze)
        self.maze_size_h = len(maze[0])

        self.surface = surface

        self.border_size_width = self.surface.get_width() / 20
        self.border_size_height = self.surface.get_height() / 20

        self.width_wall = (self.surface.get_width() - self.border_size_width * 2) / self.maze_size_w
        self.height_wall = (self.surface.get_height() - self.border_size_height * 2) / self.maze_size_h

    #  direction: up=0, right=1, down=2, left=3
    def can_go(self, x: int, y: int, direction: int) -> int:

        number_index = int((x - self.border_size_width) / self.width_wall)
        line_index = int((y - self.border_size_height) / self.height_wall)

        if direction == 0:
            if self.maze[line_index][number_index] >= 8:
                return (0)
            return (1)

        verif_value = self.maze[line_index][number_index]
        if direction == 1:
            if self.maze[line_index][number_index] >= 8:
                verif_value -= 8
            if self.maze[line_index][number_index] >= 4:
                return (0)
            return (1)

        verif_value = self.maze[line_index][number_index]
        if direction == 2:
            if verif_value >= 8:
                verif_value -= 8
            if verif_value >= 4:
                verif_value -= 4
            if verif_value >= 2:
                return (0)
            return (1)

        if direction == 3:
            if verif_value >= 8:
                verif_value -= 8
            if verif_value >= 4:
                verif_value -= 4
            if verif_value >= 2:
                verif_value -= 2
            if verif_value >= 1:
                return (0)
            return (1)

    def display_maze(self) -> None:

        for line_index, line in enumerate(self.maze):
            for number_index, number in enumerate(line):
                x0 = self.border_size_width + number_index * self.width_wall
                y0 = self.border_size_height + line_index * self.height_wall
                x1 = x0 + self.width_wall
                y1 = y0 + self.height_wall

                if number >= 8:
                    pygame.draw.line(
                        self.surface,
                        "white",
                        (x0, y0),
                        (x0, y1)
                    )
                    number -= 8
                if number >= 4:
                    pygame.draw.line(
                        self.surface,
                        "white",
                        (x0, y1),
                        (x1, y1)
                    )
                    number -= 4
                if number >= 2:
                    pygame.draw.line(
                        self.surface,
                        "white",
                        (x1, y0),
                        (x1, y1)
                    )
                    number -= 2
                if number >= 1:
                    pygame.draw.line(
                        self.surface,
                        "white",
                        (x0, y0),
                        (x1, y0)
                    )
                    number -= 1
