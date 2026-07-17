"""Entry point Game Tebak Kata Bahasa Indonesia."""

from __future__ import annotations

import argparse
import logging
from logging.handlers import RotatingFileHandler
from typing import Sequence

from game.application import GameApplication
from game.config import (
    APP_NAME,
    APP_VERSION,
    BANK_KATA_PATH,
    LEADERBOARD_PATH,
    LOG_DIR,
)
from game.data_manager import get_bank_statistics, load_bank
from game.exceptions import AppError
from game.ui import ConsoleUI


def configure_logging() -> None:
    """Configure rotating logging, with stderr fallback on file errors."""
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        handler: logging.Handler = RotatingFileHandler(
            LOG_DIR / "application.log",
            maxBytes=500_000,
            backupCount=2,
            encoding="utf-8",
        )
    except OSError:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)


def build_parser() -> argparse.ArgumentParser:
    """Build command-line arguments for the application."""
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="Jangan bersihkan terminal ketika berpindah halaman.",
    )
    parser.add_argument(
        "--validate-bank",
        action="store_true",
        help="Validasi bank kata lalu keluar.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {APP_VERSION}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the application and return an operating-system exit code."""
    args = build_parser().parse_args(argv)
    configure_logging()
    logger = logging.getLogger(__name__)

    try:
        bank = load_bank(BANK_KATA_PATH)
        if args.validate_bank:
            statistics = get_bank_statistics(bank)
            print("VALID: Bank kata konsisten.")
            print(f"Kategori : {statistics.category_count}")
            print(f"Entri    : {statistics.entry_count}")
            print(f"Frasa    : {statistics.phrase_count}")
            print(f"Versi    : {APP_VERSION}")
            return 0

        ui = ConsoleUI(clear_enabled=not args.no_clear)
        application = GameApplication(
            bank=bank,
            leaderboard_path=LEADERBOARD_PATH,
            ui=ui,
        )
        return application.run()
    except AppError as error:
        logger.error("Application error: %s", error)
        print(f"Gagal menjalankan aplikasi: {error}")
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan oleh pengguna.")
        return 130
    except Exception:
        logger.exception("Unexpected application failure")
        print(
            "Terjadi kesalahan yang tidak terduga. "
            "Detail disimpan di logs/application.log."
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
