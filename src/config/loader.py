import json

from pathlib import Path
from typing import Any
from pydantic import ValidationError

from src.config.models import Config, ConfigError


class ConfigLoader:
    """Loads the config file and strictly validates it."""

    def __init__(self, path: Path) -> None:
        """Load and validate the file, raising ConfigError on any problem."""

        self.config: Config = self._validate(self._load_file(path))

    @staticmethod
    def _strip_comments(text: str) -> str:
        """Blank out full-line comments (# or //), keeping line numbers."""

        lines = []
        for line in text.splitlines():
            if line.lstrip().startswith(("#", "//")):
                lines.append("")
            else:
                lines.append(line)

        return "\n".join(lines)

    def _load_file(self, path: Path) -> dict[str, Any]:
        """Read the file and return its content as a dict."""

        if path.suffix != ".json":
            raise ConfigError(f"{path} is not a json file.")

        try:
            with path.open(encoding="utf-8") as file:
                text = file.read()
        except (OSError, UnicodeDecodeError) as e:
            raise ConfigError(f"Cannot read {path}: {e}") from e

        try:
            data = json.loads(self._strip_comments(text))
        except json.JSONDecodeError as e:
            raise ConfigError(
                f"Invalid JSON in {path} "
                f"(line {e.lineno}, column {e.colno}): {e.msg}."
            ) from e

        if not isinstance(data, dict):
            raise ConfigError(f"{path} must contain a JSON object.")

        return data

    @staticmethod
    def _validate(data: dict[str, Any]) -> Config:
        """Validate the data, listing every error found."""

        try:
            return Config.model_validate(data)
        except ValidationError as e:
            lines = []
            for error in e.errors():
                where = ".".join(str(p) for p in error["loc"]) or "config"
                lines.append(f"  - {where}: {error['msg']}")

            raise ConfigError(
                "Invalid configuration:\n" + "\n".join(lines)
            ) from None