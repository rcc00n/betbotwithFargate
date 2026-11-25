import ast
import os
from pathlib import Path
import re
import unittest
from unittest.mock import patch

from runtime_config import required_env, json_object


class ConfigurationTests(unittest.TestCase):
    def test_missing_and_blank_configuration_fails_without_echoing_values(self):
        for value in (None, " "):
            with patch.dict(os.environ, {} if value is None else {"EXAMPLE_KEY": value}, clear=True):
                with self.assertRaisesRegex(RuntimeError, "Set EXAMPLE_KEY"):
                    required_env("EXAMPLE_KEY")

    def test_explicit_environment_is_used(self):
        with patch.dict(os.environ, {"EXAMPLE_KEY": "  local-fixture  "}, clear=True):
            self.assertEqual(required_env("EXAMPLE_KEY"), "local-fixture")

    def test_json_configuration_is_bounded_to_an_object_and_errors_are_redacted(self):
        for raw in ("[]", "null", "broken-private-value"):
            with patch.dict(os.environ, {"EXAMPLE_JSON": raw}, clear=True):
                with self.assertRaisesRegex(RuntimeError, "EXAMPLE_JSON must contain a JSON object") as error:
                    json_object("EXAMPLE_JSON")
                self.assertNotIn(raw, str(error.exception))
        with patch.dict(os.environ, {"EXAMPLE_JSON": '{"fixture":"value"}'}, clear=True):
            self.assertEqual(json_object("EXAMPLE_JSON"), {"fixture":"value"})

    def test_entrypoints_have_no_literal_provider_credentials(self):
        root = Path(__file__).resolve().parents[1]
        telegram = re.compile(r"\b[0-9]{8,12}:[A-Za-z0-9_-]{30,}\b")
        discord = re.compile(r"\b[A-Za-z0-9_-]{24,}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{25,}\b")
        for path in root.glob("*.py"):
            text = path.read_text()
            self.assertFalse(telegram.search(text) or discord.search(text), path.name)
            tree = ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {"TeleBot", "run"}:
                    if node.args and isinstance(node.args[0], ast.Constant):
                        self.fail(f"Literal provider credential in {path.name}")
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "api_key" for t in node.targets):
                    self.assertNotIsInstance(node.value, ast.Constant, path.name)


if __name__ == "__main__":
    unittest.main()
