"""Integration tests for the application service."""

from __future__ import annotations

import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from game.application import GameApplication
from game.exceptions import LeaderboardError
from game.ui import ConsoleUI


class ApplicationIntegrationTest(unittest.TestCase):
    def run_app(
        self,
        inputs: list[str],
        bank: dict[str, dict[str, list[str]]] | None = None,
        leaderboard_content: str | None = None,
    ) -> tuple[int, list[str], Path]:
        values = iter(inputs)
        output: list[str] = []
        ui = ConsoleUI(
            input_function=lambda _: next(values),
            output_function=output.append,
            clear_enabled=False,
        )
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        leaderboard_path = Path(self.directory.name) / "leaderboard.json"
        if leaderboard_content is not None:
            leaderboard_path.write_text(leaderboard_content, encoding="utf-8")
        app = GameApplication(
            bank=bank
            or {
                "hewan": {
                    "1": ["sapi"],
                    "2": ["kelinci"],
                    "3": ["trenggiling"],
                }
            },
            leaderboard_path=leaderboard_path,
            ui=ui,
            rng=random.Random(1),
        )
        return app.run(), output, leaderboard_path

    def test_player_can_exit_and_change_name(self) -> None:
        status, output, _ = self.run_app(["Tester", "5", "Nama Baru", "0"])
        self.assertEqual(status, 0)
        self.assertTrue(any("Pemain: Nama Baru" in line for line in output))
        self.assertIn("Terima kasih sudah bermain.", output)

    def test_complete_winning_round_persists_score(self) -> None:
        status, output, leaderboard_path = self.run_app(
            [
                "Tester",
                "1",
                "1",
                "1",
                "s",
                "a",
                "p",
                "i",
                "",
                "0",
            ]
        )
        self.assertEqual(status, 0)
        scores = json.loads(leaderboard_path.read_text(encoding="utf-8"))
        self.assertEqual(len(scores), 1)
        self.assertEqual(scores[0]["nama"], "Tester")
        self.assertGreater(scores[0]["skor"], 0)
        self.assertTrue(any("SELAMAT" in line for line in output))

    def test_forfeit_loss_and_category_back_paths(self) -> None:
        status, output, leaderboard_path = self.run_app(
            [
                "Tester",
                "1", "2",  # category back
                "1", "1", "1", "0", "",  # forfeit
                "1", "1", "1", "z", "x", "q", "w", "v", "b", "n", "m", "",  # loss
                "0",
            ],
            bank={"hewan": {"1": ["sapi"], "2": ["kelinci"], "3": ["trenggiling"]}},
        )
        self.assertEqual(status, 0)
        self.assertFalse(leaderboard_path.exists())
        self.assertTrue(any("menyerah" in line.lower() for line in output))
        self.assertTrue(any("Kesempatan habis" in line for line in output))

    def test_instructions_about_and_empty_leaderboard_paths(self) -> None:
        status, output, _ = self.run_app(
            ["Tester", "2", "", "3", "", "4", "", "0"]
        )
        self.assertEqual(status, 0)
        self.assertTrue(any("Belum ada skor" in line for line in output))
        self.assertTrue(any("CARA BERMAIN" in line for line in output))
        self.assertTrue(any("TENTANG PROYEK" in line for line in output))

    def test_corrupted_leaderboard_does_not_crash_menu(self) -> None:
        status, output, _ = self.run_app(
            ["Tester", "2", "", "0"],
            leaderboard_content="{invalid",
        )
        self.assertEqual(status, 0)
        self.assertTrue(any("tidak dapat dibuka" in line for line in output))

    def test_save_failure_is_reported_without_crashing(self) -> None:
        values = iter(["Tester", "1", "1", "1", "s", "a", "p", "i", "", "0"])
        output: list[str] = []
        ui = ConsoleUI(
            input_function=lambda _: next(values),
            output_function=output.append,
            clear_enabled=False,
        )
        with tempfile.TemporaryDirectory() as directory, patch(
            "game.application.save_score",
            side_effect=LeaderboardError("disk penuh"),
        ):
            app = GameApplication(
                bank={"hewan": {"1": ["sapi"], "2": ["kelinci"], "3": ["trenggiling"]}},
                leaderboard_path=Path(directory) / "leaderboard.json",
                ui=ui,
                rng=random.Random(1),
            )
            self.assertEqual(app.run(), 0)
        self.assertTrue(any("gagal disimpan" in line for line in output))

    def test_seen_answers_are_tracked_per_category_and_level_cycle(self) -> None:
        class ChoiceRng:
            def choice(self, sequence: list[str]) -> str:
                return sequence[0]

        output: list[str] = []
        # Three rounds in the same two-answer pool. The third round starts a new cycle.
        inputs = iter([
            "Tester",
            "1", "1", "1", "a", "",  # answer a
            "1", "1", "1", "b", "",  # answer b
            "1", "1", "1", "a", "",  # cycle resets to a
            "0",
        ])
        ui = ConsoleUI(
            input_function=lambda _: next(inputs),
            output_function=output.append,
            clear_enabled=False,
        )
        with tempfile.TemporaryDirectory() as directory:
            app = GameApplication(
                bank={"hewan": {"1": ["a", "b"], "2": ["c"], "3": ["d"]}},
                leaderboard_path=Path(directory) / "leaderboard.json",
                ui=ui,
                rng=ChoiceRng(),  # type: ignore[arg-type]
            )
            self.assertEqual(app.run(), 0)
        wins = [line for line in output if line.startswith("SELAMAT")]
        self.assertEqual(len(wins), 3)


if __name__ == "__main__":
    unittest.main()
