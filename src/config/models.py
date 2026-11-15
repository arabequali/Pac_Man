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
    level_size_increase: int = Field(ge=0, le=5)
    level_count: int = Field(ge=10)
    level_max_time: int = Field(ge=30)

    lives: int = Field(ge=1)

    points_per_pacgum: int = Field(ge=0)
    points_per_super_pacgum: int = Field(ge=0)
    points_per_ghosts: int = Field(ge=0)

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