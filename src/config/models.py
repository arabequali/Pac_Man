import os.path
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ConfigError(Exception):
    """Raised when the configuration file is unusable or invalid."""


SizeLimit = Annotated[int, Field(ge=11, le=99)]


class Config(BaseModel):
    """Game configuration. Every field is required and strictly typed."""

    model_config = ConfigDict(strict=True, extra="ignore")

    level_1_seed: int = Field(ge=0, le=2147483647)
    level_1_size: list[SizeLimit] = Field(min_length=2, max_length=2)
    level_size_increase: int = Field(ge=0, le=8)
    level_count: int = Field(ge=10)
    level_max_time: int = Field(ge=30)

    lives: int = Field(ge=1)

    points_per_pacgum: int = Field(ge=10)
    points_per_super_pacgum: int = Field(ge=10)
    points_per_ghosts: int = Field(ge=10)

    power_duration: float = Field(ge=0.0, allow_inf_nan=False)
    ghost_respawn_time: float = Field(ge=0.0, allow_inf_nan=False)

    cheat_mode: bool
    highscore_filename_path: str = Field(min_length=1)

    @model_validator(mode="after")
    def _check_last_level_size(self) -> "Config":
        """Reject configs whose last level would exceed the max size."""

        biggest = (max(self.level_1_size)
                   + self.level_size_increase * (self.level_count - 1))

        if biggest > 99:
            raise ValueError(
                f"last level would reach size {biggest} (maximum is 99)"
            )

        return self

    def change_level_1_seed(
            self,
            increment: bool | None = None,
            value: int | None = None
    ) -> None:
        """Changes the level_1_seed.
        If value is not None, it changes the level_1_seed to value.

        else:
        It adds 1 if increment is True, and remove 1 if decrement is True.
        If the value is already 0, it cannot decrement.
        If the value is already 2147483647, it cannot increment."""

        if value:
            self.level_1_seed = value
            return None

        if increment and self.level_1_seed < 2147483647:
            self.level_1_seed += 1
        elif not increment and self.level_1_seed > 0:
            self.level_1_seed -= 1

    def change_level_1_size(
            self,
            increment: bool | None = None,
            value: int | None = None
    ) -> None:
        """blabla"""

        if value and (11 <= value <= 99):
            self.level_1_size = [value, value]
            return None

        if increment and self.level_1_size[0] < 99:
            self.level_1_size[0] +=2
            self.level_1_size[1] += 2
        elif not increment and self.level_1_size[0] > 11:
            self.level_1_size[0] -= 2
            self.level_1_size[1] -= 2

    def change_level_size_increase(
            self,
            increment: bool | None = None,
            value: int | None = None
    ) -> None:

        if value and (0 <= value <= 10):
            self.level_size_increase = value
            return None

        if increment and (max(self.level_1_size) + (self.level_size_increase + 2) * (self.level_count - 1)) <= 99:
            self.level_size_increase += 2
        elif not increment and self.level_size_increase > 0:
            self.level_size_increase -= 2

    def change_level_count(
            self,
            increment: bool | None = None,
            value: int | None = None
    ) -> None:

        if value and (value >= 10):
            self.level_count = value
            return None

        if increment:
            self.level_count += 1
        elif not increment and self.level_count > 10:
            self.level_count -= 1

    def change_level_max_time(
            self,
            increment: bool | None = None,
            value: int | None = None
    ) -> None:

        if value and (value >= 30):
            self.level_max_time = value
            return None

        if increment:
            self.level_max_time += 5
        elif not increment and self.level_max_time > 30:
            self.level_max_time -= 5

    def change_lives(
            self,
            increment: bool | None = None,
            value: int | None = None
    ) -> None:

        if value and value >= 1:
            self.lives = value

        if increment:
            self.lives += 1
        elif not increment and self.lives > 1:
            self.lives -= 1

    def change_points_per_pacgum(
            self,
            increment: bool | None = None,
            value: int | None = None
    ) -> None:

        if value and value >= 10:
            self.points_per_pacgum = value

        if increment:
            self.points_per_pacgum += 10
        elif not increment and self.points_per_pacgum > 10:
            self.points_per_pacgum -= 10

    def change_points_per_super_pacgum(
            self,
            increment: bool = None,
            value: int | None = None
    ) -> None:

        if value and value >= 10:
            self.points_per_super_pacgum = value

        if increment:
            self.points_per_super_pacgum += 10
        elif not increment and self.points_per_super_pacgum > 10:
            self.points_per_super_pacgum -= 10

    def change_points_per_ghosts(
            self,
            increment: bool | None = None,
            value: int | None = None
    ) -> None:

        if value and value >= 10:
            self.points_per_ghosts = value
            return None

        if increment:
            self.points_per_ghosts += 10
        elif not increment and self.points_per_ghosts > 10:
            self.points_per_ghosts -= 10

    def change_power_duration(
            self,
            increment: bool | None = None,
            value: int | None = None
    ) -> None:

        if value and value >= 0:
            self.power_duration = value
            return None

        if increment:
            self.power_duration += 0.5
        elif not increment and self.power_duration > 0:
            self.power_duration -= 0.5

    def change_ghost_respawn_time(
            self,
            increment: bool | None = None,
            value: int | None = None
    ) -> None:

        if value and value >= 0:
            self.ghost_respawn_time = value

        if increment:
            self.ghost_respawn_time += 0.5
        elif not increment and self.ghost_respawn_time > 0:
            self.ghost_respawn_time -= 0.5

    def change_cheat_mode(self) -> None:

        self.cheat_mode = not self.cheat_mode

    def change_highscore_filename_path(
            self,
            value: str
    ) -> str | None:

        if len(value) >= 1 and os.path.isfile(value):
            self.highscore_filename_path = value
            return None
        return "Invalid file name."