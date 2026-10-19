import mazegenerator
from src.display import Display
from src.maze import Maze
from src.game import Game


if __name__ == '__main__':

    test = mazegenerator.MazeGenerator((20, 20)).maze
    for t in test:
        print(t)
    Display(720, 720).pipeline()
