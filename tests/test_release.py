"""Release-consistency checks."""

from __future__ import annotations

import json
import tomllib
import unittest
from pathlib import Path

from game import __version__
from game.config import APP_VERSION, BANK_KATA_PATH, LEADERBOARD_PATH, PROJECT_ROOT


class ReleaseConsistencyTest(unittest.TestCase):
    def test_versions_are_consistent(self) -> None:
        pyproject = tomllib.loads(
            (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        )
        bank = json.loads(BANK_KATA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(APP_VERSION, __version__)
        self.assertEqual(pyproject["project"]["version"], APP_VERSION)
        metadata = bank["metadata"]
        self.assertEqual(metadata["versi"], APP_VERSION)
        self.assertNotIn("jumlah_negara", metadata)
        self.assertNotIn("jumlah_kata", metadata)
        self.assertIn("jumlah_per_kategori", metadata)

    def test_distribution_leaderboard_is_empty(self) -> None:
        self.assertEqual(
            json.loads(LEADERBOARD_PATH.read_text(encoding="utf-8")),
            [],
        )


if __name__ == "__main__":
    unittest.main()
