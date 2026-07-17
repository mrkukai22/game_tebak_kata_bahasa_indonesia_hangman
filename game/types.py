"""Shared type definitions."""

from __future__ import annotations

from typing import TypeAlias, TypedDict

DifficultyLevels: TypeAlias = dict[str, list[str]]
WordBank: TypeAlias = dict[str, DifficultyLevels]


class ScoreEntry(TypedDict):
    """One persisted leaderboard entry."""

    nama: str
    skor: int
    kategori: str
    kesulitan: int
    kata: str
    waktu: str
