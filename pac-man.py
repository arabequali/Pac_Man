import sys
from pathlib import Path

from src.config.loader import ConfigLoader
from src.config.models import ConfigError
from src.maze.generator import MazeGenerator
from src.maze.maze import Maze
from src.ui.graphics import Graphics
from src.ui.renderer import Renderer
from src.application import Application


def main(argv: list[str]) -> None:
    if (len(argv) != 2):
        print("Usage: uv run python3 pac-man.py <config file name>")
        return

    try:
        config_path = Path(argv[1])
        config_loader = ConfigLoader(config_path)
    except ConfigError as e:
        return print(e)

    maze = Maze(MazeGenerator(config_loader.config.level_1_size, seed=config_loader.config.level_1_seed).maze)
    graphics = Graphics()
    renderer = Renderer(graphics)
    application = Application(config_loader, graphics, renderer)
    application.run()


if __name__ == '__main__':
    main(sys.argv)