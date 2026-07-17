#!/usr/bin/env python3
"""Validate the word bank and optionally print generic detailed statistics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from game.config import APP_VERSION, BANK_KATA_PATH, CATEGORY_LABELS  # noqa: E402
from game.data_manager import get_bank_statistics, load_bank  # noqa: E402
from game.exceptions import BankKataError  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    """Build arguments for the validation utility."""
    parser = argparse.ArgumentParser(description="Validasi bank kata")
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=BANK_KATA_PATH,
        help="Lokasi bank_kata.json.",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "--details",
        action="store_true",
        help="Tampilkan jumlah entri seluruh kategori.",
    )
    output_group.add_argument(
        "--json",
        action="store_true",
        help="Tampilkan hasil dalam JSON untuk otomasi.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Validate a bank and print consistent, category-neutral statistics."""
    args = build_parser().parse_args(argv)
    try:
        bank = load_bank(args.path)
    except (BankKataError, OSError, json.JSONDecodeError) as error:
        if args.json:
            print(
                json.dumps(
                    {"valid": False, "error": str(error)},
                    ensure_ascii=False,
                )
            )
        else:
            print(f"TIDAK VALID: {error}")
        return 1

    statistics = get_bank_statistics(bank)
    result = {
        "valid": True,
        "versi": APP_VERSION,
        "jumlah_kategori": statistics.category_count,
        "jumlah_entri": statistics.entry_count,
        "jumlah_frasa": statistics.phrase_count,
        "jumlah_per_kategori": dict(statistics.entries_per_category),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print("VALID: Struktur dan metadata bank kata konsisten.")
    print(f"Kategori : {statistics.category_count}")
    print(f"Entri    : {statistics.entry_count}")
    print(f"Frasa    : {statistics.phrase_count}")
    print(f"Versi    : {APP_VERSION}")

    if args.details:
        print("\nRincian kategori:")
        for category in sorted(
            statistics.entries_per_category,
            key=lambda key: CATEGORY_LABELS[key],
        ):
            label = CATEGORY_LABELS[category]
            count = statistics.entries_per_category[category]
            print(f"- {label:<22} {count:>4} entri")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
