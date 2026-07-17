"""Tests for CLI entry-point behavior."""

from __future__ import annotations

import argparse
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

import main
from game.exceptions import BankKataError


class MainTest(unittest.TestCase):
    def test_build_parser_supports_flags(self) -> None:
        parser = main.build_parser()
        args = parser.parse_args(["--no-clear", "--validate-bank"])
        self.assertTrue(args.no_clear)
        self.assertTrue(args.validate_bank)
        with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):
            parser.parse_args(["--version"])

    def test_validate_bank_mode_prints_generic_summary(self) -> None:
        bank = {"hewan": {"1": ["sapi"], "2": ["kelinci"], "3": ["trenggiling"]}}
        stream = io.StringIO()
        with (
            patch("main.configure_logging"),
            patch("main.load_bank", return_value=bank),
            redirect_stdout(stream),
        ):
            self.assertEqual(main.main(["--validate-bank"]), 0)
        output = stream.getvalue()
        self.assertIn("VALID", output)
        self.assertNotIn("Negara", output)

    def test_normal_application_mode_uses_clear_flag(self) -> None:
        application = MagicMock()
        application.run.return_value = 0
        with (
            patch("main.configure_logging"),
            patch("main.load_bank", return_value={}),
            patch("main.ConsoleUI") as ui_class,
            patch("main.GameApplication", return_value=application),
        ):
            self.assertEqual(main.main(["--no-clear"]), 0)
        ui_class.assert_called_once_with(clear_enabled=False)

    def test_expected_interruption_and_unexpected_errors_have_exit_codes(self) -> None:
        logger = MagicMock()
        with patch("main.logging.getLogger", return_value=logger):
            with patch("main.configure_logging"), patch(
                "main.load_bank", side_effect=BankKataError("rusak")
            ), redirect_stdout(io.StringIO()):
                self.assertEqual(main.main([]), 1)

            with patch("main.configure_logging"), patch(
                "main.load_bank", side_effect=KeyboardInterrupt
            ), redirect_stdout(io.StringIO()):
                self.assertEqual(main.main([]), 130)

            with patch("main.configure_logging"), patch(
                "main.load_bank", side_effect=RuntimeError("boom")
            ), redirect_stdout(io.StringIO()):
                self.assertEqual(main.main([]), 1)

        logger.error.assert_called_once()
        logger.exception.assert_called_once()

    def test_logging_falls_back_when_log_directory_cannot_be_created(self) -> None:
        with patch.object(type(main.LOG_DIR), "mkdir", side_effect=OSError), patch(
            "main.logging.basicConfig"
        ) as basic_config:
            main.configure_logging()
        basic_config.assert_called_once()


if __name__ == "__main__":
    unittest.main()
