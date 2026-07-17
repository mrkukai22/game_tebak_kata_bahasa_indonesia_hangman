"""Shared validation helpers for user-facing and persisted text."""

from __future__ import annotations

import re
from typing import Final

from game.config import MAX_PLAYER_NAME_LENGTH

ANSWER_PATTERN: Final = re.compile(r"[a-z]+(?: [a-z]+)*")


def normalize_player_name(raw_name: object) -> str:
    """Normalize a player name and reject unsafe terminal text.

    The game accepts Unicode names, but control characters (including ANSI
    escape sequences) are rejected so persisted leaderboard data cannot alter
    terminal output.
    """
    if not isinstance(raw_name, str):
        raise ValueError("Nama pemain harus berupa teks.")

    name = " ".join(raw_name.split())
    if not name:
        raise ValueError("Nama pemain tidak boleh kosong.")
    if len(name) > MAX_PLAYER_NAME_LENGTH:
        raise ValueError(
            f"Nama pemain maksimal {MAX_PLAYER_NAME_LENGTH} karakter."
        )
    if not all(character.isprintable() for character in name):
        raise ValueError("Nama pemain mengandung karakter kontrol.")
    if not any(character.isalnum() for character in name):
        raise ValueError("Nama pemain harus mengandung huruf atau angka.")
    return name


def normalize_answer(raw_answer: object) -> str:
    """Normalize and validate a word-bank answer or persisted answer."""
    if not isinstance(raw_answer, str):
        raise ValueError("Jawaban harus berupa teks.")
    answer = " ".join(raw_answer.strip().lower().split())
    if not ANSWER_PATTERN.fullmatch(answer):
        raise ValueError("Jawaban hanya boleh berisi huruf a-z dan satu spasi.")
    return answer
