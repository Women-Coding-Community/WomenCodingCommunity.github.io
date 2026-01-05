import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from publish_registry import load_registry, merge_registries, save_registry


class TestPublishRegistry(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_registry_existing_file(self):
        registry_file = self.temp_path / "registry.json"
        test_data = {"certificates": [{"id": "ABC123", "name": "Test User"}]}

        with open(registry_file, 'w') as f:
            json.dump(test_data, f)

        result = load_registry(registry_file)
        self.assertEqual(result, test_data)

    def test_load_registry_nonexistent_file(self):
        result = load_registry(self.temp_path / "nonexistent.json")
        self.assertEqual(result, {"certificates": []})

    def test_load_registry_invalid_json(self):
        registry_file = self.temp_path / "invalid.json"

        with open(registry_file, 'w') as f:
            f.write("invalid json{")

        result = load_registry(registry_file)
        self.assertEqual(result, {"certificates": []})

    def test_save_registry(self):
        registry_file = self.temp_path / "output" / "registry.json"
        test_data = {"certificates": [{"id": "XYZ789", "name": "Saved User"}]}

        save_registry(test_data, registry_file)

        self.assertTrue(registry_file.exists())

        with open(registry_file, 'r') as f:
            loaded = json.load(f)

        self.assertEqual(loaded, test_data)

    def test_merge_registries_no_duplicates(self):
        existing = {
            "certificates": [
                {"id": "AAA111", "name": "Alice", "type": "mentee"},
                {"id": "BBB222", "name": "Bob", "type": "mentor"}
            ]
        }

        new = {
            "certificates": [
                {"id": "CCC333", "name": "Charlie", "type": "volunteer"}
            ]
        }

        merged, added, skipped = merge_registries(existing, new)

        self.assertEqual(len(merged['certificates']), 3)
        self.assertEqual(added, 1)
        self.assertEqual(skipped, 0)

    def test_merge_registries_with_duplicates(self):
        existing = {
            "certificates": [
                {"id": "AAA111", "name": "Alice", "type": "mentee"},
                {"id": "BBB222", "name": "Bob", "type": "mentor"}
            ]
        }

        new = {
            "certificates": [
                {"id": "AAA111", "name": "Alice Updated", "type": "mentee"},
                {"id": "CCC333", "name": "Charlie", "type": "volunteer"}
            ]
        }

        merged, added, skipped = merge_registries(existing, new)

        self.assertEqual(len(merged['certificates']), 3)
        self.assertEqual(added, 1)
        self.assertEqual(skipped, 1)

        alice = next(c for c in merged['certificates'] if c['id'] == 'AAA111')
        self.assertEqual(alice['name'], 'Alice')

    def test_merge_registries_empty_existing(self):
        existing = {"certificates": []}

        new = {
            "certificates": [
                {"id": "AAA111", "name": "Alice", "type": "mentee"}
            ]
        }

        merged, added, skipped = merge_registries(existing, new)

        self.assertEqual(len(merged['certificates']), 1)
        self.assertEqual(added, 1)
        self.assertEqual(skipped, 0)

    def test_merge_registries_empty_new(self):
        existing = {
            "certificates": [
                {"id": "AAA111", "name": "Alice", "type": "mentee"}
            ]
        }

        new = {"certificates": []}

        merged, added, skipped = merge_registries(existing, new)

        self.assertEqual(len(merged['certificates']), 1)
        self.assertEqual(added, 0)
        self.assertEqual(skipped, 0)

    def test_merge_registries_sorts_by_name(self):
        existing = {
            "certificates": [
                {"id": "ZZZ999", "name": "Zoe", "type": "mentee"}
            ]
        }

        new = {
            "certificates": [
                {"id": "AAA111", "name": "Alice", "type": "mentor"},
                {"id": "MMM555", "name": "Mike", "type": "volunteer"}
            ]
        }

        merged, _, _ = merge_registries(existing, new)

        names = [c['name'] for c in merged['certificates']]
        self.assertEqual(names, ['Alice', 'Mike', 'Zoe'])


if __name__ == '__main__':
    unittest.main()
