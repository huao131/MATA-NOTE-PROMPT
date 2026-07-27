from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ._support import SRC  # noqa: F401
from mata_p0.errors import StopAndReport
from mata_p0.schema_validation import (
    load_json,
    require_boolean,
    require_enum,
    require_fields,
    require_nonnegative_integer,
)


class SchemaValidationTests(unittest.TestCase):
    def test_load_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TEST.json"
            path.write_text('{"ok": true}', encoding="utf-8")
            self.assertEqual(load_json(path), {"ok": True})

    def test_invalid_json_stops(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TEST.json"
            path.write_text("{", encoding="utf-8")
            with self.assertRaises(StopAndReport):
                load_json(path)

    def test_missing_field_stops(self) -> None:
        with self.assertRaises(StopAndReport):
            require_fields({}, ("required",))

    def test_invalid_enum_stops(self) -> None:
        with self.assertRaises(StopAndReport):
            require_enum("BAD", {"GOOD"}, "$.status")

    def test_boolean_rejects_integer(self) -> None:
        with self.assertRaises(StopAndReport):
            require_boolean(1, "$.flag")

    def test_nonnegative_integer_rejects_boolean(self) -> None:
        with self.assertRaises(StopAndReport):
            require_nonnegative_integer(True, "$.size")

    def test_schema_files_are_valid_json(self) -> None:
        root = Path(__file__).resolve().parents[2] / "schemas" / "p0"
        for path in root.glob("*.json"):
            with self.subTest(path=path.name):
                json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
