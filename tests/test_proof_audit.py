"""Build success must not hide incomplete or conditional Lean proofs."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[1] / 'skills' / 'lean4-checkpoint' / 'examples' / 'proof-audit'


class NativeProofAuditTests(unittest.TestCase):
    def test_successful_build_reports_direct_and_transitive_assumptions(self):
        with tempfile.TemporaryDirectory(prefix='lean-native-audit-') as temporary:
            project = Path(temporary) / 'project'
            shutil.copytree(FIXTURE, project, ignore=shutil.ignore_patterns('.lake'))
            env = os.environ.copy()
            env.pop('ELAN_TOOLCHAIN', None)  # Verify the fixture's own pinned toolchain.
            build = subprocess.run(['lake', 'build'], cwd=project, env=env,
                                   capture_output=True, text=True, timeout=120)
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            audit = subprocess.run(['lake', 'env', 'lean', 'Audit.lean'], cwd=project,
                                   env=env, capture_output=True, text=True, timeout=60)
            self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
            lines = audit.stdout.splitlines()
            expected = {
                'AuditFixture.proved': "does not depend on any axioms",
                'AuditFixture.unfinished': '[sorryAx]',
                'AuditFixture.dependsOnUnfinished': '[sorryAx]',
                'AuditFixture.localAssumption': '[AuditFixture.localAssumption]',
                'AuditFixture.assumesLocalAxiom': '[AuditFixture.localAssumption]',
            }
            for declaration, result in expected.items():
                with self.subTest(declaration=declaration):
                    reports = [line for line in lines if line.startswith("'" + declaration + "'")]
                    self.assertEqual(len(reports), 1, audit.stdout)
                    self.assertIn(result, reports[0])
            self.assertNotIn('sorry', (project / 'AuditFixture.lean').read_text().split('theorem dependsOnUnfinished')[1].split('axiom')[0])
            print(build.stdout, end='')
            print(audit.stdout, end='')


if __name__ == '__main__':
    unittest.main()
