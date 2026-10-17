import mazegenerator
from src.display import Display
from src.maze import Maze
from src.game import Game


if __name__ == '__main__':
    maze_size_w = 25
    maze_size_h = 25

    maze_generator = mazegenerator.MazeGenerator((maze_size_w, maze_size_h))

    maze = Maze(maze_generator.maze, maze_size_w, maze_size_h)

    Display(maze, 720, 720).pipeline()
