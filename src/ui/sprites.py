"""Sprites drawn pixel by pixel, once, then reused every frame.

SpriteBuilder knows the geometry (circles, wedges, ghost skirt) and writes
pixels through Graphics. SpriteSet is the finished collection that the
renderer looks images up in. Nothing here imports pygame.
"""

import math
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from src.maze.maze import Direction
from src.ui.graphics import Color, Graphics, Image

MIN_SPRITE_SIZE = 3
MAX_SPRITE_SIZE = 64          #  bigger cells are served by a centred sprite
MOUTH_HALF_ANGLE = 40.0       #  degrees on each side of the facing direction

#  Direction -> (x, y) step, y grows downwards like on the screen.
_VECTOR: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}

YELLOW: Color = (255, 255, 0, 255)
PELLET: Color = (255, 220, 180, 255)
WHITE: Color = (255, 255, 255, 255)
EYE_BLUE: Color = (33, 33, 222, 255)
SCARED_BLUE: Color = (33, 33, 222, 255)
SCARED_FACE: Color = (255, 200, 170, 255)
FLASH_FACE: Color = (222, 33, 33, 255)


class GhostColor(Enum):
    """Which ghost (a ghost keeps its colour when it is not edible)."""

    RED = (255, 0, 0, 255)
    PINK = (255, 184, 255, 255)
    CYAN = (0, 255, 255, 255)
    ORANGE = (255, 184, 82, 255)


class GhostLook(Enum):
    """How a ghost is drawn."""

    NORMAL = "normal"      # coloured body, eyes look where it goes
    EDIBLE = "edible"      # blue, scared face
    FLASHING = "flashing"  # white, power-up about to end
    EATEN = "eaten"        # only the eyes, going back to its corner


def _ghost_key(
        color: GhostColor,
        look: GhostLook,
        facing: Direction
) -> tuple[GhostColor, GhostLook, Direction]:
    """Collapse variants that look the same, so we store each image once."""
    if look in (GhostLook.EDIBLE, GhostLook.FLASHING):
        return (GhostColor.RED, look, Direction.NORTH)  # no colour, no gaze
    if look == GhostLook.EATEN:
        return (GhostColor.RED, look, facing)           # eyes only
    return (color, look, facing)


@dataclass
class SpriteSet:
    """All the images for one cell size. Plain storage with lookups."""

    size: int
    pacman: dict[tuple[Direction, bool], Image]
    ghosts: dict[tuple[GhostColor, GhostLook, Direction], Image]
    pacgum: Image
    super_pacgum: Image

    def get_pacman(self, facing: Direction, mouth_open: bool) -> Image:
        """Return Pac-Man looking toward `facing`."""
        return self.pacman[(facing, mouth_open)]

    def get_ghost(
            self,
            color: GhostColor,
            look: GhostLook,
            facing: Direction
    ) -> Image:
        """Return a ghost image for a colour, a look and a direction."""
        return self.ghosts[_ghost_key(color, look, facing)]


class SpriteBuilder:
    """Draw every sprite with pixel writes, for one cell size."""

    def __init__(self, graphics: Graphics, cell_size: int) -> None:
        """Prepare a builder.

        Args:
            graphics: the wrapper used for new_image and put_pixel.
            cell_size: size of a maze cell in pixels. Sprites are square
                images of min(cell_size, MAX_SPRITE_SIZE) pixels; the
                renderer centres them in the cell.
        """
        self._graphics = graphics
        self._size = max(MIN_SPRITE_SIZE, min(cell_size, MAX_SPRITE_SIZE))

    @property
    def size(self) -> int:
        """Side of every sprite, in pixels."""
        return self._size

    # ---- the whole collection ------------------------------------------

    def build(self) -> SpriteSet:
        """Build every image once and return them as a SpriteSet."""
        pacman = {
            (facing, mouth_open): self.pacman(facing, mouth_open)
            for facing in _VECTOR
            for mouth_open in (True, False)
        }
        ghosts: dict[tuple[GhostColor, GhostLook, Direction], Image] = {}
        for color in GhostColor:
            for look in GhostLook:
                for facing in _VECTOR:
                    key = _ghost_key(color, look, facing)
                    if key not in ghosts:
                        ghosts[key] = self.ghost(*key)
        return SpriteSet(
            self._size, pacman, ghosts, self.pacgum(), self.super_pacgum()
        )

    # ---- one method per kind of image ----------------------------------

    def pacman(self, facing: Direction, mouth_open: bool) -> Image:
        """A yellow disc, with a wedge removed when the mouth is open."""
        radius = 0.42 * self._size
        fx, fy = _VECTOR[facing]
        tan_half = math.tan(math.radians(MOUTH_HALF_ANGLE))

        def inside(dx: float, dy: float) -> bool:
            if dx * dx + dy * dy > radius * radius:
                return False
            if not mouth_open:
                return True
            forward = dx * fx + dy * fy      # distance along the facing
            side = abs(dy * fx - dx * fy)    # distance across it
            return not (forward > 0 and side <= forward * tan_half)

        image = self._new_image()
        self._paint(image, inside, YELLOW)
        return image

    def pacgum(self) -> Image:
        """A small pellet."""
        image = self._new_image()
        self._paint(image, self._disc(0, 0, max(0.12 * self._size, 0.8)),
                    PELLET)
        return image

    def super_pacgum(self) -> Image:
        """A large pellet (power-up)."""
        image = self._new_image()
        self._paint(image, self._disc(0, 0, max(0.28 * self._size, 1.5)),
                    PELLET)
        return image

    def ghost(
            self,
            color: GhostColor,
            look: GhostLook,
            facing: Direction
    ) -> Image:
        """A ghost: round head, wavy skirt, and eyes or a scared face."""
        size = self._size
        radius = 0.38 * size
        head_y = -0.05 * size        # centre of the head, relative to centre
        bottom = 0.40 * size
        tooth = max(1.0, 0.07 * size)

        def body(dx: float, dy: float) -> bool:
            if abs(dx) > radius:
                return False
            if dy <= head_y:
                return dx * dx + (dy - head_y) ** 2 <= radius * radius
            edge = bottom
            if int((dx + radius) / (2 * radius) * 6) % 2 == 1:
                edge -= tooth        # every other segment is shorter
            return dy <= edge

        image = self._new_image()
        eye_x = 0.17 * size
        eye_y = head_y - 0.03 * size
        if look == GhostLook.EDIBLE or look == GhostLook.FLASHING:
            body_color = SCARED_BLUE if look == GhostLook.EDIBLE else WHITE
            face = SCARED_FACE if look == GhostLook.EDIBLE else FLASH_FACE
            self._paint(image, body, body_color)
            dot = max(0.06 * size, 0.7)
            self._paint(image, self._disc(-eye_x, eye_y, dot), face)
            self._paint(image, self._disc(eye_x, eye_y, dot), face)
            self._paint(image, self._zigzag(0.12 * size, size), face)
        else:
            if look == GhostLook.NORMAL:
                self._paint(image, body, color.value)
            fx, fy = _VECTOR[facing]
            white = max(0.11 * size, 1.0)
            pupil = max(0.06 * size, 0.7)
            look_x, look_y = fx * 0.05 * size, fy * 0.05 * size
            for side in (-eye_x, eye_x):
                self._paint(image, self._disc(side, eye_y, white), WHITE)
                self._paint(
                    image,
                    self._disc(side + look_x, eye_y + look_y, pupil),
                    EYE_BLUE,
                )
        return image

    # ---- small drawing helpers ------------------------------------------

    def _new_image(self) -> Image:
        """A fully transparent square image."""
        return self._graphics.new_image(self._size, self._size,
                                        transparent=True)

    def _paint(
            self,
            image: Image,
            inside: Callable[[float, float], bool],
            color: Color
    ) -> None:
        """Write `color` on every pixel whose centre satisfies `inside`.

        `inside` receives the pixel centre relative to the middle of the
        image: dx grows to the right, dy grows downwards.
        """
        middle = self._size / 2
        for y in range(self._size):
            for x in range(self._size):
                if inside(x + 0.5 - middle, y + 0.5 - middle):
                    self._graphics.put_pixel(image, x, y, color)

    @staticmethod
    def _disc(
            center_x: float,
            center_y: float,
            radius: float
    ) -> Callable[[float, float], bool]:
        """Shape test: inside a circle."""
        def inside(dx: float, dy: float) -> bool:
            return (dx - center_x) ** 2 + (dy - center_y) ** 2 <= radius ** 2
        return inside

    @staticmethod
    def _zigzag(mouth_y: float, size: int) -> Callable[[float, float], bool]:
        """Shape test: the scared ghost's zigzag mouth."""
        half_width = 0.26 * size
        step = 2 * half_width / 5
        wave = 0.04 * size
        thick = max(0.5, 0.025 * size)

        def inside(dx: float, dy: float) -> bool:
            if abs(dx) > half_width:
                return False
            segment = int((dx + half_width) / step)
            offset = wave if segment % 2 else -wave
            return abs(dy - (mouth_y + offset)) <= thick

        return inside