"""Validated and atomic leaderboard persistence."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import cast

from game.config import (
    CATEGORY_LABELS,
    DIFFICULTIES,
    LEADERBOARD_STORAGE_LIMIT,
)
from game.exceptions import LeaderboardError
from game.types import ScoreEntry
from game.validation import ANSWER_PATTERN, normalize_player_name

_ALLOWED_CATEGORY_LABELS = frozenset(CATEGORY_LABELS.values())


def _empty_leaderboard(path: Path) -> list[ScoreEntry]:
    """Create an empty leaderboard when storage does not yet exist."""
    _write_atomic(path, [])
    return []


def _validate_entry(raw: object, index: int) -> ScoreEntry:
    """Validate one decoded score entry and return a normalized copy."""
    if not isinstance(raw, dict):
        raise LeaderboardError(f"Entri leaderboard ke-{index} bukan object.")

    expected_keys = {
        "nama",
        "skor",
        "kategori",
        "kesulitan",
        "kata",
        "waktu",
    }
    if set(raw) != expected_keys:
        raise LeaderboardError(
            f"Struktur entri leaderboard ke-{index} tidak lengkap."
        )

    try:
        name = normalize_player_name(raw["nama"])
    except ValueError as error:
        raise LeaderboardError(
            f"Nama pada entri ke-{index} tidak valid: {error}"
        ) from error
    if name != raw["nama"]:
        raise LeaderboardError(
            f"Nama pada entri ke-{index} belum dinormalisasi."
        )

    score = raw["skor"]
    category = raw["kategori"]
    difficulty = raw["kesulitan"]
    word = raw["kata"]
    timestamp = raw["waktu"]

    if not isinstance(score, int) or isinstance(score, bool) or score <= 0:
        raise LeaderboardError(f"Skor pada entri ke-{index} tidak valid.")
    if category not in _ALLOWED_CATEGORY_LABELS:
        raise LeaderboardError(f"Kategori pada entri ke-{index} tidak valid.")
    if (
        not isinstance(difficulty, int)
        or isinstance(difficulty, bool)
        or difficulty not in DIFFICULTIES
    ):
        raise LeaderboardError(
            f"Kesulitan pada entri ke-{index} tidak valid."
        )
    if not isinstance(word, str) or not ANSWER_PATTERN.fullmatch(word):
        raise LeaderboardError(f"Jawaban pada entri ke-{index} tidak valid.")
    if not isinstance(timestamp, str):
        raise LeaderboardError(f"Waktu pada entri ke-{index} tidak valid.")

    try:
        parsed_timestamp = datetime.fromisoformat(timestamp)
    except ValueError as error:
        raise LeaderboardError(
            f"Format waktu pada entri ke-{index} tidak valid."
        ) from error
    if parsed_timestamp.tzinfo is None or parsed_timestamp.utcoffset() is None:
        raise LeaderboardError(
            f"Waktu pada entri ke-{index} harus memiliki zona waktu."
        )

    return cast(
        ScoreEntry,
        {
            "nama": name,
            "skor": score,
            "kategori": category,
            "kesulitan": difficulty,
            "kata": word,
            "waktu": timestamp,
        },
    )


def _write_atomic(path: Path, entries: list[ScoreEntry]) -> None:
    """Persist JSON atomically so a failed write cannot corrupt data."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(entries, temporary_file, ensure_ascii=False, indent=2)
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    except (OSError, TypeError) as error:
        raise LeaderboardError(
            f"Leaderboard tidak dapat disimpan: {error}"
        ) from error
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def load_leaderboard(path: Path) -> list[ScoreEntry]:
    """Load, validate, and sort all persisted leaderboard entries."""
    if not path.exists():
        return _empty_leaderboard(path)

    try:
        raw_data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise LeaderboardError(
            "JSON leaderboard rusak pada "
            f"baris {error.lineno}, kolom {error.colno}."
        ) from error
    except OSError as error:
        raise LeaderboardError(
            f"Leaderboard tidak dapat dibaca: {error}"
        ) from error

    if not isinstance(raw_data, list):
        raise LeaderboardError("Leaderboard harus berupa array JSON.")

    entries = [
        _validate_entry(raw, index)
        for index, raw in enumerate(raw_data, start=1)
    ]
    entries.sort(key=lambda entry: (-entry["skor"], entry["waktu"]))
    return entries


def save_score(
    path: Path,
    player_name: object,
    score: int,
    category: str,
    difficulty: int,
    word: str,
) -> ScoreEntry:
    """Validate, append, sort, and atomically persist one winning score."""
    try:
        name = normalize_player_name(player_name)
    except ValueError as error:
        raise LeaderboardError(str(error)) from error

    if not isinstance(score, int) or isinstance(score, bool) or score <= 0:
        raise LeaderboardError("Skor harus berupa bilangan bulat positif.")
    if category not in _ALLOWED_CATEGORY_LABELS:
        raise LeaderboardError("Kategori tidak valid.")
    if (
        not isinstance(difficulty, int)
        or isinstance(difficulty, bool)
        or difficulty not in DIFFICULTIES
    ):
        raise LeaderboardError("Tingkat kesulitan tidak valid.")
    if not isinstance(word, str) or not ANSWER_PATTERN.fullmatch(word):
        raise LeaderboardError("Jawaban tidak valid.")

    entry: ScoreEntry = {
        "nama": name,
        "skor": score,
        "kategori": category,
        "kesulitan": difficulty,
        "kata": word,
        "waktu": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    entries = load_leaderboard(path)
    entries.append(entry)
    entries.sort(key=lambda item: (-item["skor"], item["waktu"]))
    _write_atomic(path, entries[:LEADERBOARD_STORAGE_LIMIT])
    return entry


def top_scores(path: Path, limit: int) -> list[ScoreEntry]:
    """Return up to limit highest scores."""
    if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
        return []
    return load_leaderboard(path)[:limit]
