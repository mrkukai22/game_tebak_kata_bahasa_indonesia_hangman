"""Immutable application configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Final, Mapping

from game import __version__

APP_NAME: Final = "Game Tebak Kata Bahasa Indonesia"
APP_VERSION: Final = __version__

PROJECT_ROOT: Final = Path(__file__).resolve().parent.parent
DATA_DIR: Final = PROJECT_ROOT / "data"
LOG_DIR: Final = PROJECT_ROOT / "logs"
BANK_KATA_PATH: Final = DATA_DIR / "bank_kata.json"
LEADERBOARD_PATH: Final = DATA_DIR / "leaderboard.json"

MAX_PLAYER_NAME_LENGTH: Final = 30
LEADERBOARD_STORAGE_LIMIT: Final = 100
LEADERBOARD_DISPLAY_LIMIT: Final = 10
EXPECTED_DIFFICULTY_LEVELS: Final = frozenset({"1", "2", "3"})


@dataclass(frozen=True, slots=True)
class DifficultySettings:
    """Rules applied to one difficulty level."""

    label: str
    max_wrong: int
    score_multiplier: int


DIFFICULTIES: Final[Mapping[int, DifficultySettings]] = MappingProxyType(
    {
        1: DifficultySettings("Mudah", max_wrong=8, score_multiplier=1),
        2: DifficultySettings("Sedang", max_wrong=7, score_multiplier=2),
        3: DifficultySettings("Sulit", max_wrong=6, score_multiplier=3),
    }
)

CATEGORY_LABELS: Final[Mapping[str, str]] = MappingProxyType(
    {
        "alam": "Alam",
        "alat_tulis": "Alat Tulis",
        "angka": "Angka",
        "bangunan": "Bangunan",
        "barang_pribadi": "Barang Pribadi",
        "benda": "Benda",
        "dapur": "Dapur",
        "hewan": "Hewan",
        "kamar_mandi": "Kamar Mandi",
        "kebun": "Kebun",
        "komputer": "Komputer",
        "makanan": "Makanan",
        "mata_pelajaran": "Mata Pelajaran",
        "musik": "Musik",
        "negara": "Negara",
        "olahraga": "Olahraga",
        "pakaian": "Pakaian",
        "pekerjaan": "Pekerjaan",
        "rumah": "Rumah",
        "rumah_sakit": "Rumah Sakit",
        "tempat": "Tempat",
        "transportasi": "Transportasi",
        "tubuh": "Tubuh",
        "warna": "Warna",
    }
)
