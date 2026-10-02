#!/usr/bin/env python3
"""Inspect optional upstream guide/script layout; execute no plugin code."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / 'optional-upstream.json').read_text())


def requested_files() -> list[str]:
    requested = set(SPEC['script_files'])
    for skill in (ROOT / 'skills').glob('lean4-*/SKILL.md'):
        requested.update(re.findall(r'`\$LEAN4_PLUGIN_ROOT/([^`]+)`', skill.read_text()))
    return sorted(requested)


def inspect_plugin(root: Path) -> dict:
    root = root.expanduser().resolve()
    files = requested_files()
    absent = [relative for relative in files if not (root / relative).is_file()]
    revision = None
    clean = None
    if root.is_dir():
        result = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'],
                                capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            revision = result.stdout.strip()
            status = subprocess.run(['git', '-C', str(root), 'status', '--porcelain'],
                                    capture_output=True, text=True, timeout=10)
            clean = status.returncode == 0 and not status.stdout
    return {'root': str(root), 'status': 'absent_optional' if not root.exists() else 'incompatible_layout' if absent else 'layout_compatible',
            'requested_files': files, 'missing_files': absent,
            'tested_revision': SPEC['revision'], 'checkout_revision': revision,
            'revision_matches': None if revision is None else revision == SPEC['revision'],
            'checkout_clean': clean, 'plugin_code_executed': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(os.environ.get('LEAN4_PLUGIN_ROOT', str(Path.cwd() / 'vendor/lean4-plugin'))))
    parser.add_argument('--require-compatible', action='store_true', help='Fail when requested guides/scripts are absent')
    parser.add_argument('--require-pinned', action='store_true', help='Also require a clean checkout at the tested revision')
    parser.add_argument('--output', type=Path, help='Optional JSON evidence output')
    args = parser.parse_args()
    report = inspect_plugin(args.root)
    text = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end='')
    if args.require_pinned and (report['revision_matches'] is not True or report['checkout_clean'] is not True):
        return 1
    if report['status'] == 'layout_compatible':
        return 0
    if report['status'] == 'absent_optional' and not (args.require_compatible or args.require_pinned):
        return 0
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
