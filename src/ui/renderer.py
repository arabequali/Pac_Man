from src.ui.graphics import Graphics


class MazeLayout:
    """The class that contains the maze layout informations (maze size, cell size, etc.)"""

    def __init__(
            self,
            maze_size: int,
            cell_size: int,
            width_offset: int,
            height_offset: int,
            graphics: Graphics,
            game_engine
    ) -> None:
        """Initialize the class containing all the layout values"""

        self.maze_size = maze_size
        self.cell_size = cell_size
        self.width_offset, self.height_offset = self.get_offset(graphics)
        self.maze_image = self.create_maze_image(graphics, game_engine)

    def get_offset(self, graphics: Graphics) -> tuple[int]:

        window_width, window_height = graphics.get_window_size()
        return window_width - self.maze_size, window_height - self.maze_size

    def create_maze_image(
            self,
            graphics: Graphics,
            game_engine
    ) -> None:
        maze_size = self.maze_size
        cell_size = self.cell_size
        maze_image = graphics.new_image(maze_size, maze_size)
        maze = game_engine.current_level.maze.maze_grid

        for row in range(len(maze)):
            for cell in range(len(maze)):
                graphics.draw_cell(maze_image, maze[row][cell], cell_size, cell * self.cell_size, row * self.cell_size)

        return maze_image


class Renderer:
    """The class that handles the rendering of the application (calculate sizes)."""

    def __init__(self, graphics: Graphics) -> None:
        self._graphics = graphics

    @property
    def graphics(self) -> Graphics:
        return self._graphics

    def calculate_cell_size(
            self,
            maze_width: int,
            maze_height: int
        ) -> int:
        """Calculate the size of each cell in the maze based on the window size and maze dimensions.
        It takes the smallest size between the width and height of the calculated cell size to ensure that the cells remains squares."""

        window_width, window_height = self.graphics.get_window_size()
        cell_width = (window_width - window_width // 10) // maze_width
        cell_height = (window_height - window_height // 10) // maze_height
        cell_size = min(cell_width, cell_height)
        return cell_size

    def calculate_maze_size(
            self,
            cell_size: int,
            maze_width: int,
            maze_height: int
    ) -> int:
        """Calculate the size of the maze based on the window size and maze dimensions.
        It takes the minimum between width and height to ensure the maze remains a square."""

        maze_width_px = cell_size * maze_width
        maze_height_px = cell_size * maze_height
        maze_size_px = min(maze_width_px, maze_height_px)
        return maze_size_px

    def calculate_offsets_size(self) -> tuple[int]:
        window_width, window_height = self.graphics.get_window_size()
        return window_width // 10, window_height // 10

    def get_maze_layout(
            self,
            maze_size: tuple[int],
            game_engine
    ) -> MazeLayout:
        """Return the class MazeLayout by rendering the maze size, cell size and offset size"""

        maze_width, maze_height = maze_size
        cell_size = self.calculate_cell_size(maze_width, maze_height)
        maze_size = self.calculate_maze_size(cell_size, maze_width, maze_height)
        offsets = self.calculate_offsets_size()
        return MazeLayout(self.calculate_maze_size(cell_size, maze_width, maze_height), cell_size, offsets[0], offsets[1], self.graphics, game_engine)