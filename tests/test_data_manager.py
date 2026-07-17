"""Tests for word-bank validation, statistics, and selection."""

from __future__ import annotations

import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from game.config import APP_VERSION, BANK_KATA_PATH, CATEGORY_LABELS
from game.data_manager import (
    get_bank_statistics,
    load_bank,
    select_random_word,
    validate_bank_payload,
)
from game.exceptions import BankKataError


def minimal_payload() -> dict[str, object]:
    """Return a complete and structurally valid minimal payload."""
    categories = {
        category: {
            "1": [f"a{index}a"],
            "2": [f"b{index}b"],
            "3": [f"c{index}c"],
        }
        for index, category in enumerate(CATEGORY_LABELS)
    }
    # Answers cannot contain digits, so replace the generated markers.
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    categories = {
        category: {
            "1": [f"a{alphabet[index]}a"],
            "2": [f"b{alphabet[index]}b"],
            "3": [f"c{alphabet[index]}c"],
        }
        for index, category in enumerate(CATEGORY_LABELS)
    }
    counts = {category: 3 for category in categories}
    return {
        "metadata": {
            "versi": APP_VERSION,
            "jumlah_kategori": len(categories),
            "jumlah_entri": len(categories) * 3,
            "jumlah_frasa": 0,
            "jumlah_per_kategori": counts,
        },
        "kategori": categories,
    }


class DataManagerTest(unittest.TestCase):
    def test_production_bank_statistics(self) -> None:
        bank = load_bank(BANK_KATA_PATH)
        statistics = get_bank_statistics(bank)
        self.assertEqual(statistics.category_count, 24)
        self.assertEqual(statistics.entry_count, 2059)
        self.assertEqual(statistics.phrase_count, 397)
        self.assertEqual(
            sum(statistics.entries_per_category.values()),
            statistics.entry_count,
        )


    def test_dataset_normalization_regressions(self) -> None:
        bank = load_bank(BANK_KATA_PATH)
        self.assertIn("surel", bank["komputer"]["1"])
        self.assertIn("peramban", bank["komputer"]["2"])
        self.assertIn("bulu tangkis", bank["olahraga"]["2"])
        self.assertIn("bahasa indonesia", bank["mata_pelajaran"]["3"])

        forbidden = {"email", "browser", "badminton", "pingpong", "staples"}
        all_answers = {
            answer
            for levels in bank.values()
            for answers in levels.values()
            for answer in answers
        }
        self.assertTrue(forbidden.isdisjoint(all_answers))

    def test_load_bank_handles_missing_invalid_and_os_errors(self) -> None:
        with self.assertRaisesRegex(BankKataError, "tidak ditemukan"):
            load_bank(Path("file-yang-tidak-ada.json"))

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bank.json"
            path.write_text("{invalid", encoding="utf-8")
            with self.assertRaisesRegex(BankKataError, "baris"):
                load_bank(path)

        with patch.object(Path, "read_text", side_effect=PermissionError):
            with self.assertRaisesRegex(BankKataError, "ditolak"):
                load_bank(Path("bank.json"))

        with patch.object(Path, "read_text", side_effect=OSError("disk")):
            with self.assertRaisesRegex(BankKataError, "tidak dapat dibaca"):
                load_bank(Path("bank.json"))

    def test_root_metadata_and_category_structure_are_validated(self) -> None:
        with self.assertRaisesRegex(BankKataError, "Root bank"):
            validate_bank_payload([])
        with self.assertRaisesRegex(BankKataError, "kategori"):
            validate_bank_payload({"metadata": {}})

        payload = minimal_payload()
        payload.pop("metadata")
        with self.assertRaisesRegex(BankKataError, "metadata"):
            validate_bank_payload(payload)

        payload = minimal_payload()
        categories = payload["kategori"]
        assert isinstance(categories, dict)
        categories.pop("alam")
        with self.assertRaisesRegex(BankKataError, "kategori hilang"):
            validate_bank_payload(payload)

        payload = minimal_payload()
        categories = payload["kategori"]
        assert isinstance(categories, dict)
        categories["lain"] = {"1": ["aaa"], "2": ["bbb"], "3": ["ccc"]}
        with self.assertRaisesRegex(BankKataError, "tidak dikenal"):
            validate_bank_payload(payload)

    def test_level_list_order_format_duplicates_and_tautology_are_validated(
        self,
    ) -> None:
        payload = minimal_payload()
        categories = payload["kategori"]
        assert isinstance(categories, dict)
        categories["alam"] = []
        with self.assertRaisesRegex(BankKataError, "object level"):
            validate_bank_payload(payload)

        payload = minimal_payload()
        categories = payload["kategori"]
        assert isinstance(categories, dict)
        categories["alam"] = {"1": ["aaa"], "2": ["bbb"]}
        with self.assertRaisesRegex(BankKataError, "level 1, 2, dan 3"):
            validate_bank_payload(payload)

        payload = minimal_payload()
        categories = payload["kategori"]
        assert isinstance(categories, dict)
        categories["alam"]["1"] = []
        with self.assertRaisesRegex(BankKataError, "tidak kosong"):
            validate_bank_payload(payload)

        payload = minimal_payload()
        categories = payload["kategori"]
        assert isinstance(categories, dict)
        categories["alam"]["1"] = ["zeta", "alfa"]
        with self.assertRaisesRegex(BankKataError, "A-Z"):
            validate_bank_payload(payload)

        payload = minimal_payload()
        categories = payload["kategori"]
        assert isinstance(categories, dict)
        categories["alam"]["1"] = ["café"]
        with self.assertRaisesRegex(BankKataError, "tidak valid"):
            validate_bank_payload(payload)

        payload = minimal_payload()
        categories = payload["kategori"]
        assert isinstance(categories, dict)
        duplicate = categories["alam"]["1"][0]
        categories["alam"]["2"] = [duplicate]
        with self.assertRaisesRegex(BankKataError, "duplikat"):
            validate_bank_payload(payload)

        payload = minimal_payload()
        categories = payload["kategori"]
        assert isinstance(categories, dict)
        categories["alam"]["1"] = ["alam"]
        with self.assertRaisesRegex(BankKataError, "nama kategorinya"):
            validate_bank_payload(payload)

    def test_all_generic_metadata_fields_are_validated(self) -> None:
        fields = (
            "versi",
            "jumlah_kategori",
            "jumlah_entri",
            "jumlah_frasa",
            "jumlah_per_kategori",
        )
        for field in fields:
            with self.subTest(field=field):
                payload = minimal_payload()
                metadata = payload["metadata"]
                assert isinstance(metadata, dict)
                metadata[field] = "salah"
                with self.assertRaisesRegex(BankKataError, field):
                    validate_bank_payload(payload)

    def test_phrase_count_and_immutable_statistics_mapping(self) -> None:
        payload = minimal_payload()
        categories = payload["kategori"]
        metadata = payload["metadata"]
        assert isinstance(categories, dict)
        assert isinstance(metadata, dict)
        categories["alam"]["1"] = ["air laut"]
        metadata["jumlah_frasa"] = 1
        bank = validate_bank_payload(payload)
        statistics = get_bank_statistics(bank)
        self.assertEqual(statistics.phrase_count, 1)
        with self.assertRaises(TypeError):
            statistics.entries_per_category["alam"] = 99  # type: ignore[index]

    def test_selection_validates_pool_and_respects_exclusions(self) -> None:
        bank = {"hewan": {"1": ["ayam", "sapi"], "2": [], "3": []}}
        with self.assertRaisesRegex(BankKataError, "Kategori"):
            select_random_word(bank, "alam", 1)
        with self.assertRaisesRegex(BankKataError, "Kesulitan"):
            select_random_word(bank, "hewan", 9)

        selected = select_random_word(
            bank,
            "hewan",
            1,
            excluded_words={"ayam"},
            rng=random.Random(7),
        )
        self.assertEqual(selected, "sapi")

        selected = select_random_word(
            bank,
            "hewan",
            1,
            excluded_words={"ayam", "sapi"},
            rng=random.Random(7),
        )
        self.assertIn(selected, {"ayam", "sapi"})

    def test_load_bank_reads_valid_file(self) -> None:
        payload = minimal_payload()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bank.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            bank = load_bank(path)
        self.assertEqual(len(bank), len(CATEGORY_LABELS))


if __name__ == "__main__":
    unittest.main()
