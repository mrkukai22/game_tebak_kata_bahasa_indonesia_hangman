"""Tests for console input validation and rendering."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from game.data_manager import BankStatistics
from game.hangman import GuessStatus, HangmanGame
from game.ui import ConsoleUI


class ConsoleUITest(unittest.TestCase):
    def make_ui(self, inputs: list[str] | None = None) -> tuple[ConsoleUI, list[str]]:
        values = iter(inputs or [])
        output: list[str] = []
        ui = ConsoleUI(
            input_function=lambda _: next(values),
            output_function=output.append,
            clear_enabled=False,
        )
        return ui, output

    def test_prompt_player_name_retries_and_normalizes(self) -> None:
        ui, output = self.make_ui(["", "---", "  Ariq   Gym "])
        self.assertEqual(ui.prompt_player_name("Nama: "), "Ariq Gym")
        self.assertEqual(len(output), 2)

    def test_prompt_number_retries_invalid_values(self) -> None:
        ui, output = self.make_ui(["abc", "9", "2"])
        self.assertEqual(ui.prompt_number("Pilih: ", 1, 3), 2)
        self.assertEqual(len(output), 2)

    def test_category_and_difficulty_selection(self) -> None:
        bank = {
            "hewan": {"1": ["sapi"], "2": ["kelinci"], "3": ["trenggiling"]},
            "alam": {"1": ["air"], "2": ["hujan"], "3": ["matahari"]},
        }
        ui, output = self.make_ui(["1"])
        self.assertEqual(ui.choose_category(bank), "alam")
        self.assertTrue(any("Alam" in line for line in output))

        ui, _ = self.make_ui(["3"])
        self.assertIsNone(ui.choose_category(bank))

        ui, output = self.make_ui(["2"])
        self.assertEqual(ui.choose_difficulty(), 2)
        self.assertTrue(any("Pengali skor" in line for line in output))

    def test_round_leaderboard_and_general_pages_render(self) -> None:
        game = HangmanGame(
            word="arab saudi",
            category="negara",
            difficulty=3,
            max_wrong=6,
            score_multiplier=3,
        )
        game.guess("a")
        game.guess("z")
        ui, output = self.make_ui()
        ui.display_round(game, "Negara")
        self.assertTrue(any("Jumlah kata" in line for line in output))
        self.assertTrue(any("Huruf salah" in line for line in output))

        ui, output = self.make_ui()
        ui.display_leaderboard([])
        self.assertIn("Belum ada skor yang tersimpan.", output)

        score = {
            "nama": "Tester",
            "skor": 100,
            "kategori": "Hewan",
            "kesulitan": 1,
            "kata": "sapi",
            "waktu": "2026-06-16T10:00:00+00:00",
        }
        ui, output = self.make_ui()
        ui.display_leaderboard([score])
        self.assertTrue(any("Tester" in line for line in output))

        stats = BankStatistics(24, 2059, 397, {})
        ui, output = self.make_ui()
        ui.display_instructions(24)
        ui.display_about(stats)
        self.assertTrue(any("24 kategori" in line for line in output))
        self.assertFalse(any("195 negara" in line for line in output))

    def test_main_menu_guess_pause_header_and_outcome_messages(self) -> None:
        ui, output = self.make_ui(["5", "x", ""])
        self.assertEqual(ui.display_main_menu("Tester"), 5)
        self.assertEqual(ui.prompt_guess(), "x")
        ui.pause()
        ui.header("JUDUL")
        ui.write()
        for status in GuessStatus:
            ui.write_message_for_outcome(status, "a")
        self.assertTrue(any("Pemain: Tester" in line for line in output))
        self.assertTrue(any("JUDUL" in line for line in output))

    def test_clear_only_calls_os_when_enabled_and_tty(self) -> None:
        ui = ConsoleUI(clear_enabled=True)
        with patch("game.ui.sys.stdout.isatty", return_value=False), patch(
            "game.ui.os.system"
        ) as system:
            ui.clear()
            system.assert_not_called()

        with patch("game.ui.sys.stdout.isatty", return_value=True), patch(
            "game.ui.os.system"
        ) as system:
            ui.clear()
            system.assert_called_once()

    def test_join_or_dash(self) -> None:
        self.assertEqual(ConsoleUI._join_or_dash(set()), "-")
        self.assertEqual(ConsoleUI._join_or_dash({"b", "a"}), "a, b")


if __name__ == "__main__":
    unittest.main()
