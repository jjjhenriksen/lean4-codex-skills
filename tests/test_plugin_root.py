"""Exercise each skill's documented setup and references in isolated workspaces."""
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted((ROOT / 'skills').glob('lean4-*/SKILL.md'))


class PluginRootTests(unittest.TestCase):
    def resolve(self, skill, workspace, configured=None):
        text = skill.read_text()
        setup = re.search(r'```bash\n(.*?)\n```', text, re.S).group(1)
        paths = re.findall(r'`((?:\$LEAN4_PLUGIN_ROOT|vendor/lean4-plugin)/[^`]+)`', text)
        references = [path.split('/', 1)[1] if path.startswith('$') else path[len('vendor/lean4-plugin/'):] for path in paths]
        self.assertTrue(references, f'No configured-root references in {skill}')
        env = os.environ.copy()
        for name in ('LEAN4_PLUGIN_ROOT', 'LEAN4_SCRIPTS', 'LEAN4_PYTHON_BIN'):
            env.pop(name, None)
        if configured is not None:
            env['LEAN4_PLUGIN_ROOT'] = str(configured)
        expressions = [path if path.startswith('$') else '$PWD/' + path for path in paths]
        script = setup + '\n' + '\n'.join(f'if test -f "{expression}"; then printf "found:%s\\n" "{expression}"; else printf "missing:%s\\n" "{expression}"; fi' for expression in expressions)
        script += '\nprintf "scripts:%s\\n" "$LEAN4_SCRIPTS"\n'
        result = subprocess.run(['bash', '-c', script], cwd=workspace, env=env,
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        return references, result.stdout

    def test_every_skill_resolves_nondefault_root_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix='lean-root-') as temporary:
            workspace = (Path(temporary) / 'workspace').resolve()
            workspace.mkdir()
            root = Path(temporary) / 'external plugin with spaces'
            for skill in SKILLS:
                text = skill.read_text()
                for relative in re.findall(r'`(?:\$LEAN4_PLUGIN_ROOT|vendor/lean4-plugin)/([^`]+)`', text):
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text('Fixture optional guide\n')
                with self.subTest(skill=skill.parent.name):
                    references, output = self.resolve(skill, workspace, root)
                    for relative in references:
                        self.assertIn(f'found:{root / relative}\n', output)
                    self.assertIn(f'scripts:{root / "lib/scripts"}\n', output)
                    self.assertNotIn('missing:', output)

    def test_absent_default_optional_backend_keeps_setup_usable(self):
        with tempfile.TemporaryDirectory(prefix='lean-no-plugin-') as temporary:
            workspace = Path(temporary).resolve()
            for skill in SKILLS:
                with self.subTest(skill=skill.parent.name):
                    references, output = self.resolve(skill, workspace)
                    for relative in references:
                        self.assertIn(f'missing:{workspace / "vendor/lean4-plugin" / relative}\n', output)
                    self.assertIn(f'scripts:{workspace / "vendor/lean4-plugin/lib/scripts"}\n', output)

    def test_optional_env_file_configuration_is_respected(self):
        with tempfile.TemporaryDirectory(prefix='lean-env-root-') as temporary:
            workspace = Path(temporary).resolve()
            (workspace / 'lean4-codex.env').write_text('export LEAN4_PLUGIN_ROOT="$PWD/env-selected-root"\n')
            for skill in SKILLS:
                with self.subTest(skill=skill.parent.name):
                    _, output = self.resolve(skill, workspace)
                    self.assertIn(str(workspace / 'env-selected-root'), output)
                    self.assertNotIn('vendor/lean4-plugin', output)


if __name__ == '__main__':
    unittest.main()
