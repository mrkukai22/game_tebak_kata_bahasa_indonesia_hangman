"""Tests for the standalone bank validator."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools import validate_bank


class ValidateBankToolTest(unittest.TestCase):
    def test_default_output_is_generic(self) -> None:
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(validate_bank.main([]), 0)
        output = stream.getvalue()
        self.assertIn("VALID", output)
        self.assertIn("Kategori", output)
        self.assertNotIn("Negara", output)

    def test_details_and_json_outputs(self) -> None:
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(validate_bank.main(["--details"]), 0)
        self.assertIn("Rincian kategori", stream.getvalue())

        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(validate_bank.main(["--json"]), 0)
        payload = json.loads(stream.getvalue())
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["jumlah_kategori"], 24)

    def test_invalid_file_returns_nonzero_in_text_and_json_modes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text("{invalid", encoding="utf-8")
            for extra in ([], ["--json"]):
                stream = io.StringIO()
                with self.subTest(extra=extra), redirect_stdout(stream):
                    self.assertEqual(
                        validate_bank.main([str(path), *extra]),
                        1,
                    )
                self.assertTrue(stream.getvalue())


if __name__ == "__main__":
    unittest.main()
