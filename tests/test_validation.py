"""Tests for shared text validation."""

from __future__ import annotations

import unittest

from game.validation import normalize_answer, normalize_player_name


class ValidationTest(unittest.TestCase):
    def test_player_name_is_normalized(self) -> None:
        self.assertEqual(normalize_player_name("  Ariq   Gym  "), "Ariq Gym")
        self.assertEqual(normalize_player_name("Budi-01"), "Budi-01")

    def test_player_name_rejects_invalid_values(self) -> None:
        for value in (None, "", "   ", "---", "A\x1b[31m"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_player_name(value)
        with self.assertRaisesRegex(ValueError, "maksimal"):
            normalize_player_name("a" * 31)

    def test_answer_is_normalized(self) -> None:
        self.assertEqual(normalize_answer("  Arab   Saudi "), "arab saudi")

    def test_answer_rejects_invalid_values(self) -> None:
        for value in (None, "", "café", "dua-kata", "abc  123"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_answer(value)


if __name__ == "__main__":
    unittest.main()
