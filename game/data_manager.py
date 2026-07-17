"""Word-bank loading, validation, statistics, and random selection."""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from game.config import (
    APP_VERSION,
    CATEGORY_LABELS,
    EXPECTED_DIFFICULTY_LEVELS,
)
from game.exceptions import BankKataError
from game.types import WordBank
from game.validation import ANSWER_PATTERN


@dataclass(frozen=True, slots=True)
class BankStatistics:
    """Generic structural statistics for a validated word bank."""

    category_count: int
    entry_count: int
    phrase_count: int
    entries_per_category: Mapping[str, int]


def _read_json(path: Path) -> object:
    """Read JSON and convert low-level errors into BankKataError."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise BankKataError(f"File bank kata tidak ditemukan: {path}") from error
    except PermissionError as error:
        raise BankKataError(f"Akses bank kata ditolak: {path}") from error
    except OSError as error:
        raise BankKataError(f"Bank kata tidak dapat dibaca: {error}") from error
    except json.JSONDecodeError as error:
        raise BankKataError(
            "JSON bank kata tidak valid pada "
            f"baris {error.lineno}, kolom {error.colno}."
        ) from error


def get_bank_statistics(bank: WordBank) -> BankStatistics:
    """Return generic statistics without privileging one category."""
    entries_per_category = {
        category: sum(len(words) for words in levels.values())
        for category, levels in bank.items()
    }
    phrase_count = sum(
        1
        for levels in bank.values()
        for words in levels.values()
        for answer in words
        if " " in answer
    )
    return BankStatistics(
        category_count=len(bank),
        entry_count=sum(entries_per_category.values()),
        phrase_count=phrase_count,
        entries_per_category=MappingProxyType(entries_per_category),
    )


def _validate_metadata(metadata: object, statistics: BankStatistics) -> None:
    """Validate generic metadata against calculated statistics."""
    if not isinstance(metadata, dict):
        raise BankKataError("Key 'metadata' tidak ada atau bukan object.")

    expected_values: dict[str, object] = {
        "versi": APP_VERSION,
        "jumlah_kategori": statistics.category_count,
        "jumlah_entri": statistics.entry_count,
        "jumlah_frasa": statistics.phrase_count,
        "jumlah_per_kategori": dict(statistics.entries_per_category),
    }
    for key, expected_value in expected_values.items():
        actual_value = metadata.get(key)
        if actual_value != expected_value:
            raise BankKataError(
                f"Metadata {key} tidak sesuai: "
                f"{actual_value!r} != {expected_value!r}."
            )


def validate_bank_payload(payload: object) -> WordBank:
    """Validate a decoded bank payload and return normalized categories."""
    if not isinstance(payload, dict):
        raise BankKataError("Root bank kata harus berupa object JSON.")

    categories = payload.get("kategori")
    if not isinstance(categories, dict) or not categories:
        raise BankKataError("Key 'kategori' tidak ada atau kosong.")

    expected_categories = set(CATEGORY_LABELS)
    actual_categories = set(categories)
    if actual_categories != expected_categories:
        missing = sorted(expected_categories - actual_categories)
        extra = sorted(actual_categories - expected_categories)
        details: list[str] = []
        if missing:
            details.append(f"kategori hilang: {missing}")
        if extra:
            details.append(f"kategori tidak dikenal: {extra}")
        raise BankKataError("; ".join(details))

    validated: WordBank = {}
    for category in CATEGORY_LABELS:
        raw_levels = categories[category]
        if not isinstance(raw_levels, dict):
            raise BankKataError(
                f"Kategori {category!r} harus memiliki object level."
            )
        if set(raw_levels) != EXPECTED_DIFFICULTY_LEVELS:
            raise BankKataError(
                f"Kategori '{category}' harus memiliki level 1, 2, dan 3."
            )

        levels: dict[str, list[str]] = {}
        seen_in_category: set[str] = set()
        for level in sorted(EXPECTED_DIFFICULTY_LEVELS):
            raw_answers = raw_levels[level]
            if not isinstance(raw_answers, list) or not raw_answers:
                raise BankKataError(
                    f"Kategori '{category}' level {level} harus berupa "
                    "list yang tidak kosong."
                )

            if raw_answers != sorted(raw_answers):
                raise BankKataError(
                    f"Kategori '{category}' level {level} harus diurutkan A-Z."
                )

            answers: list[str] = []
            for answer in raw_answers:
                if (
                    not isinstance(answer, str)
                    or not ANSWER_PATTERN.fullmatch(answer)
                ):
                    raise BankKataError(
                        f"Jawaban tidak valid: {answer!r} "
                        f"({category}, level {level})."
                    )
                if answer in seen_in_category:
                    raise BankKataError(
                        f"Jawaban duplikat dalam kategori "
                        f"'{category}': {answer!r}."
                    )
                seen_in_category.add(answer)
                answers.append(answer)
            levels[level] = answers

        category_label = CATEGORY_LABELS[category].lower()
        if category_label in seen_in_category:
            raise BankKataError(
                f"Kategori '{category}' tidak boleh memuat jawaban yang "
                "sama persis dengan nama kategorinya."
            )
        validated[category] = levels

    statistics = get_bank_statistics(validated)
    _validate_metadata(payload.get("metadata"), statistics)
    return validated


def load_bank(path: Path) -> WordBank:
    """Load and validate a word bank from disk."""
    return validate_bank_payload(_read_json(path))


def select_random_word(
    bank: WordBank,
    category: str,
    difficulty: int,
    excluded_words: set[str] | None = None,
    rng: random.Random | None = None,
) -> str:
    """Select a random answer while avoiding entries in the active cycle."""
    if category not in bank:
        raise BankKataError(f"Kategori tidak ditemukan: {category!r}.")

    level = str(difficulty)
    if level not in bank[category]:
        raise BankKataError(
            f"Kesulitan {difficulty} tidak tersedia pada '{category}'."
        )

    source = bank[category][level]
    excluded = excluded_words or set()
    candidates = [answer for answer in source if answer not in excluded]
    if not candidates:
        candidates = list(source)

    randomizer = rng or random.SystemRandom()
    return randomizer.choice(candidates)
