"""Execute the documented diagnostic against a real broken TOML project."""
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'skills' / 'lean4-doctor' / 'examples' / 'toml-import'


class DoctorTomlTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='lean-toml-doctor-')
        self.addCleanup(temporary.cleanup)
        self.project = Path(temporary.name) / 'project'
        shutil.copytree(FIXTURE, self.project, ignore=shutil.ignore_patterns('.lake'))
        self.env = os.environ.copy()
        self.env.pop('ELAN_TOOLCHAIN', None)

    def run_command(self, command):
        return subprocess.run(command, cwd=self.project, env=self.env,
                              capture_output=True, text=True, timeout=120)

    def test_documented_checks_surface_toml_source_configuration(self):
        skill = (ROOT / 'skills' / 'lean4-doctor' / 'SKILL.md').read_text()
        checks = skill.split('## Checks', 1)[1]
        command = re.search(r'```bash\n(.*?)\n```', checks, re.S).group(1)
        result = self.run_command(['bash', '-c', command])
        self.assertIn('srcDir = "MissingSource"', result.stdout)
        self.assertIn('name = "DoctorFixture"', result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.project / 'lakefile.lean').exists())

    def test_toml_import_error_resolves_after_correcting_source_directory(self):
        failed = self.run_command(['lake', 'env', 'lean', 'Src/DoctorFixture.lean'])
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('DoctorFixture', failed.stdout + failed.stderr)
        configuration = self.project / 'lakefile.toml'
        configuration.write_text(configuration.read_text().replace('srcDir = "MissingSource"', 'srcDir = "Src"'))
        build = self.run_command(['lake', 'build'])
        self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
        checked = self.run_command(['lake', 'env', 'lean', 'Src/DoctorFixture.lean'])
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        print('Original import failure:', failed.stdout + failed.stderr)
        print('Corrected TOML build:', build.stdout + build.stderr)


if __name__ == '__main__':
    unittest.main()
