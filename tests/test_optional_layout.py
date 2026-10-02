"""Compatibility evidence must distinguish absent files and unverified revisions."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / 'scripts' / 'check_optional_plugin.py'
spec = importlib.util.spec_from_file_location('optional_layout', CHECKER)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class OptionalLayoutTests(unittest.TestCase):
    def invoke(self, root, *options):
        result = subprocess.run([sys.executable, str(CHECKER), '--root', str(root), *options],
                                capture_output=True, text=True, timeout=10)
        return result.returncode, json.loads(result.stdout)

    def fixture(self, root):
        for relative in checker.requested_files():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('raise AssertionError("Never execute fixture plugin code")\n')

    def test_absent_optional_plugin_is_nonfatal_unless_required(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'absent'
            code, report = self.invoke(root)
            self.assertEqual(code, 0)
            self.assertEqual(report['status'], 'absent_optional')
            self.assertFalse(report['plugin_code_executed'])
            self.assertEqual(self.invoke(root, '--require-compatible')[0], 1)

    def test_complete_layout_with_spaces_is_not_a_verified_revision(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'optional plugin with spaces'
            self.fixture(root)
            code, report = self.invoke(root, '--require-compatible')
            self.assertEqual(code, 0)
            self.assertEqual(report['status'], 'layout_compatible')
            self.assertIsNone(report['checkout_revision'])
            self.assertIsNone(report['revision_matches'])
            self.assertFalse(report['plugin_code_executed'])
            self.assertEqual(self.invoke(root, '--require-pinned')[0], 1)

    def test_missing_requested_reference_fails_compatibility(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root)
            (root / 'commands/diagnose.md').unlink()
            code, report = self.invoke(root, '--require-compatible')
            self.assertEqual(code, 1)
            self.assertEqual(report['missing_files'], ['commands/diagnose.md'])
            self.assertEqual(report['status'], 'incompatible_layout')

    def test_different_git_revision_is_reported_and_not_accepted_as_pinned(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root)
            for command in [
                ['git', 'init', '-q'], ['git', 'add', '.'],
                ['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Layout fixture']]:
                subprocess.run(command, cwd=root, check=True, capture_output=True)
            code, report = self.invoke(root, '--require-compatible', '--require-pinned')
            self.assertEqual(code, 1)
            self.assertFalse(report['revision_matches'])
            self.assertTrue(report['checkout_clean'])
            self.assertNotEqual(report['checkout_revision'], report['tested_revision'])


if __name__ == '__main__':
    unittest.main()
