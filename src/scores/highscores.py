"""Persistent top-10 highscores, stored in a JSON file.

HighscoreEntry is one validated (name, score) pair. HighscoreManager loads
and saves the table, and decides who enters it. Nothing here raises on file
problems: a missing, empty or damaged file gives an empty or partial table,
and the reason is logged as a warning.
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

MAX_ENTRIES = 10
MAX_NAME_LENGTH = 10


def is_valid_name(name: object) -> bool:
    """Tell whether `name` is an acceptable player name.

    Rules: 1 to MAX_NAME_LENGTH characters, only ASCII letters, digits and
    spaces, and no space at the start or the end.
    """
    return (
        isinstance(name, str)
        and 0 < len(name) <= MAX_NAME_LENGTH
        and name == name.strip()
        and all(c.isascii() and (c.isalnum() or c == " ") for c in name)
    )


def is_valid_score(score: object) -> bool:
    """Tell whether `score` is a non-negative integer (booleans refused)."""
    return (isinstance(score, int) and not isinstance(score, bool)
            and score >= 0)


@dataclass(frozen=True)
class HighscoreEntry:
    """One line of the highscore table."""

    name: str
    score: int

    def __post_init__(self) -> None:
        """Refuse an invalid name or score.

        Raises:
            ValueError: the name or the score breaks the rules above.
        """
        if not is_valid_name(self.name):
            raise ValueError(f"Invalid player name: {self.name!r}.")
        if not is_valid_score(self.score):
            raise ValueError(f"Invalid score: {self.score!r}.")


class HighscoreManager:
    """The top-10 table and its file."""

    def __init__(self, path: str | Path) -> None:
        """Prepare a manager. The file is only read by load().

        Args:
            path: the JSON file holding the table.
        """
        self._path = Path(path)
        self._entries: list[HighscoreEntry] = []

    @property
    def entries(self) -> list[HighscoreEntry]:
        """The table, best score first (a copy: changing it does nothing)."""
        return list(self._entries)

    # ---- reading ------------------------------------------------------

    def load(self) -> None:
        """Read the table from the file, replacing the current one.

        A missing file is normal (first launch). Any other problem is
        logged and gives an empty table, or only the valid lines.
        """
        self._entries = []
        try:
            with self._path.open(encoding="utf-8") as file:
                text = file.read()
        except FileNotFoundError:
            return
        except (OSError, UnicodeDecodeError) as e:
            logger.warning("Cannot read highscores %s: %s", self._path, e)
            return
        if not text.strip():
            return  # empty file: same as no scores yet

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            logger.warning("Highscores %s are not valid JSON (line %d): %s",
                           self._path, e.lineno, e.msg)
            return
        if not isinstance(data, list):
            logger.warning("Highscores %s must contain a list.", self._path)
            return

        entries: list[HighscoreEntry] = []
        for position, item in enumerate(data, start=1):
            entry = self._parse_entry(item)
            if entry is None:
                logger.warning("Highscores %s: entry %d ignored (invalid).",
                               self._path, position)
            else:
                entries.append(entry)
        entries.sort(key=lambda e: e.score, reverse=True)  # stable sort
        self._entries = entries[:MAX_ENTRIES]

    @staticmethod
    def _parse_entry(item: Any) -> HighscoreEntry | None:
        """Turn one JSON item into an entry, or None if it is invalid."""
        if not isinstance(item, dict):
            return None
        name: Any = item.get("name")
        score: Any = item.get("score")
        if isinstance(name, str):
            name = name.strip()
        try:
            return HighscoreEntry(name, score)
        except ValueError:
            return None

    # ---- writing ------------------------------------------------------

    def save(self) -> bool:
        """Write the table to the file.

        The data goes to a temporary file first, then replaces the real one,
        so a crash while saving cannot leave a half-written file.

        Returns:
            True if the file was written, False (and a warning) otherwise.
        """
        data = [{"name": e.name, "score": e.score} for e in self._entries]
        temporary = self._path.with_name(self._path.name + ".tmp")
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with temporary.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)
            temporary.replace(self._path)
        except OSError as e:
            logger.warning("Cannot save highscores %s: %s", self._path, e)
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
            return False
        return True

    # ---- the table ----------------------------------------------------

    def qualifies(self, score: int) -> bool:
        """Tell whether `score` would enter the table.

        There is room while the table has fewer than MAX_ENTRIES lines;
        once full, the score must beat the lowest one (a tie does not).
        """
        if not is_valid_score(score):
            return False
        return (len(self._entries) < MAX_ENTRIES
                or score > self._entries[-1].score)

    def add(self, name: str, score: int) -> int | None:
        """Insert a score if it qualifies, then save the table.

        Among equal scores, the older entry keeps the better rank.

        Args:
            name: the player name, outer spaces are removed.
            score: the final score.

        Returns:
            The rank (1 is the best), or None if the score does not qualify.

        Raises:
            ValueError: the name or the score is invalid. Check with
                is_valid_name / is_valid_score before calling.
        """
        entry = HighscoreEntry(name.strip(), score)
        if not self.qualifies(score):
            return None
        index = len(self._entries)
        for i, existing in enumerate(self._entries):
            if existing.score < score:
                index = i
                break
        self._entries.insert(index, entry)
        del self._entries[MAX_ENTRIES:]
        self.save()
        return index + 1