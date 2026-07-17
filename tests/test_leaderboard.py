"""Tests for validated atomic leaderboard persistence."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from game.exceptions import LeaderboardError
from game.leaderboard import load_leaderboard, save_score, top_scores


class LeaderboardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / "leaderboard.json"

    def tearDown(self) -> None:
        self.directory.cleanup()

    def test_missing_file_is_created_as_empty_array(self) -> None:
        self.assertEqual(load_leaderboard(self.path), [])
        self.assertEqual(json.loads(self.path.read_text()), [])

    def test_scores_are_normalized_sorted_and_limited(self) -> None:
        entry = save_score(self.path, "  Ariq   Gym ", 100, "Hewan", 1, "sapi")
        self.assertEqual(entry["nama"], "Ariq Gym")
        save_score(self.path, "B", 300, "Hewan", 3, "trenggiling")
        save_score(self.path, "C", 200, "Makanan", 2, "rendang")
        self.assertEqual(
            [item["skor"] for item in top_scores(self.path, 3)],
            [300, 200, 100],
        )

        for index in range(110):
            save_score(self.path, f"P{index}", index + 1, "Hewan", 1, "sapi")
        self.assertEqual(len(load_leaderboard(self.path)), 100)

    def test_read_errors_and_invalid_root_are_rejected(self) -> None:
        self.path.write_text("{invalid", encoding="utf-8")
        with self.assertRaisesRegex(LeaderboardError, "rusak"):
            load_leaderboard(self.path)

        self.path.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(LeaderboardError, "array"):
            load_leaderboard(self.path)

        with patch.object(Path, "read_text", side_effect=OSError("disk")):
            with self.assertRaisesRegex(LeaderboardError, "dibaca"):
                load_leaderboard(self.path)

    def test_invalid_entry_variants_are_rejected(self) -> None:
        valid = {
            "nama": "A",
            "skor": 10,
            "kategori": "Hewan",
            "kesulitan": 1,
            "kata": "sapi",
            "waktu": "2026-06-16T10:00:00+00:00",
        }
        variants = [
            "bukan object",
            {"nama": "A"},
            {**valid, "nama": ""},
            {**valid, "nama": " A "},
            {**valid, "nama": "A\x1b[31m"},
            {**valid, "skor": 0},
            {**valid, "skor": True},
            {**valid, "kategori": "Tidak Ada"},
            {**valid, "kesulitan": True},
            {**valid, "kesulitan": 9},
            {**valid, "kata": "café"},
            {**valid, "waktu": 1},
            {**valid, "waktu": "bukan waktu"},
            {**valid, "waktu": "2026-06-16T10:00:00"},
        ]
        for variant in variants:
            with self.subTest(variant=variant):
                self.path.write_text(
                    json.dumps([variant]),
                    encoding="utf-8",
                )
                with self.assertRaises(LeaderboardError):
                    load_leaderboard(self.path)

    def test_save_score_rejects_invalid_values(self) -> None:
        invalid_calls = (
            ("", 10, "Hewan", 1, "sapi"),
            ("---", 10, "Hewan", 1, "sapi"),
            ("A", 0, "Hewan", 1, "sapi"),
            ("A", True, "Hewan", 1, "sapi"),
            ("A", 10, "Tidak Ada", 1, "sapi"),
            ("A", 10, "Hewan", True, "sapi"),
            ("A", 10, "Hewan", 9, "sapi"),
            ("A", 10, "Hewan", 1, "sapi-ikan"),
        )
        for args in invalid_calls:
            with self.subTest(args=args), self.assertRaises(LeaderboardError):
                save_score(self.path, *args)

    def test_top_scores_rejects_nonpositive_and_boolean_limit(self) -> None:
        self.assertEqual(top_scores(self.path, 0), [])
        self.assertEqual(top_scores(self.path, -1), [])
        self.assertEqual(top_scores(self.path, True), [])

    def test_atomic_write_cleans_temporary_file_on_success_and_failure(self) -> None:
        save_score(self.path, "A", 100, "Hewan", 1, "sapi")
        self.assertEqual(list(self.path.parent.glob(".leaderboard.json.*.tmp")), [])

        with patch("game.leaderboard.os.replace", side_effect=OSError("gagal")):
            with self.assertRaisesRegex(LeaderboardError, "disimpan"):
                save_score(self.path, "B", 200, "Hewan", 1, "sapi")
        self.assertEqual(list(self.path.parent.glob(".leaderboard.json.*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
