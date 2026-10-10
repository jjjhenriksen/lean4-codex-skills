"""Installation is previewable and preserves all pre-existing skill content."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'install_skills.py'
spec = importlib.util.spec_from_file_location('installer', SCRIPT)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='lean-skill-install-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.destination = self.root / 'new folder with spaces' / 'skills'

    def test_dry_run_lists_every_bundle_without_creating_destination(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--dest', str(self.destination),
                                 '--dry-run'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('Would install:'), 7)
        self.assertFalse(self.destination.parent.exists())

    def test_install_copies_complete_bundles_and_preserves_unrelated_skills(self):
        self.destination.mkdir(parents=True)
        unrelated = self.destination / 'my-other-skill.txt'
        unrelated.write_text('Keep this')
        targets = installer.install(self.destination)
        for target in targets:
            source = ROOT / 'skills' / target.name
            for file in source.rglob('*'):
                if file.is_file():
                    self.assertEqual((target / file.relative_to(source)).read_bytes(), file.read_bytes())
        self.assertEqual(unrelated.read_text(), 'Keep this')
        self.assertEqual(len(targets), 7)

    def test_every_collision_is_checked_before_any_skill_is_copied(self):
        for kind in ('file', 'directory', 'broken-symlink'):
            with self.subTest(kind=kind):
                destination = self.root / kind
                destination.mkdir()
                target = destination / installer.SKILL_NAMES[-1]
                if kind == 'file':
                    target.write_text('Local edits')
                elif kind == 'directory':
                    target.mkdir()
                    (target / 'SKILL.md').write_text('Local edits')
                else:
                    target.symlink_to(self.root / 'absent')
                for preview in (False, True):
                    with self.assertRaisesRegex(ValueError, 'Existing skills are preserved'):
                        installer.install(destination, dry_run=preview)
                self.assertEqual(list(destination.iterdir()), [target])
                if kind == 'file':
                    self.assertEqual(target.read_text(), 'Local edits')
                elif kind == 'directory':
                    self.assertEqual((target / 'SKILL.md').read_text(), 'Local edits')
                else:
                    self.assertTrue(target.is_symlink())

    def test_failed_copy_removes_only_new_skill_directories(self):
        self.destination.mkdir(parents=True)
        existing = self.destination / 'keep.txt'
        existing.write_text('Existing')
        copytree = shutil.copytree

        def fail_second(source, target, *args, **kwargs):
            if Path(source).name == installer.SKILL_NAMES[1]:
                (target / 'partial').write_text('incomplete')
                raise OSError('copy interrupted')
            return copytree(source, target, *args, **kwargs)

        with patch.object(installer.shutil, 'copytree', side_effect=fail_second):
            with self.assertRaisesRegex(OSError, 'copy interrupted'):
                installer.install(self.destination)
        self.assertEqual(list(self.destination.iterdir()), [existing])
        self.assertEqual(existing.read_text(), 'Existing')

    def test_missing_source_and_recursive_destination_do_not_write(self):
        with self.assertRaisesRegex(ValueError, 'Missing source bundle'):
            installer.install(self.destination, source_root=self.root / 'missing')
        self.assertFalse(self.destination.exists())
        with self.assertRaisesRegex(ValueError, 'outside the source bundles'):
            installer.install(ROOT / 'skills' / 'nested')


if __name__ == '__main__':
    unittest.main()
