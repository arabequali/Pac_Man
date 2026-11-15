import sys
from pathlib import Path

from src.config.loader import ConfigLoader
from src.config.models import ConfigError
from src.maze.generator import MazeGenerator, MazeGenerationError
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

    graphics = Graphics()
    renderer = Renderer(graphics)

    try:
        application = Application(config_loader.config, graphics, renderer)
    except MazeGenerationError as e:
        return print(f"Maze generation error occurred: {e}")
    application.run()


if __name__ == '__main__':
    main(sys.argv)