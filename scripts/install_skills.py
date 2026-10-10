#!/usr/bin/env python3
"""Preview or install the Lean skill bundles without replacing existing skills."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAMES = (
    'lean4-checkpoint', 'lean4-doctor', 'lean4-formalize', 'lean4-learn',
    'lean4-mentor', 'lean4-prove', 'lean4-review',
)


def install(destination: Path, *, source_root: Path = ROOT / 'skills',
            dry_run: bool = False) -> list[Path]:
    destination = destination.expanduser().resolve()
    source_root = source_root.resolve()
    if destination.is_relative_to(source_root):
        raise ValueError('Choose a destination outside the source bundles.')
    if destination.exists() and not destination.is_dir():
        raise ValueError('The destination must be a directory.')
    sources = [source_root / name for name in SKILL_NAMES]
    targets = [destination / name for name in SKILL_NAMES]
    for source in sources:
        if not (source / 'SKILL.md').is_file():
            raise ValueError(f'Missing source bundle: {source.name}')
    occupied = [target.name for target in targets if target.exists() or target.is_symlink()]
    if occupied:
        raise ValueError('Existing skills are preserved; move reviewed copies to a backup '
                         'outside skill roots before installing: ' + ', '.join(occupied))
    if dry_run:
        return targets

    destination.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    try:
        for source, target in zip(sources, targets):
            # Reserve each name exclusively, including after the initial preflight.
            target.mkdir()
            created.append(target)
            shutil.copytree(source, target, dirs_exist_ok=True)
    except BaseException:
        for target in reversed(created):
            shutil.rmtree(target)
        raise
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, required=True,
                        help='The intended Codex skill directory')
    parser.add_argument('--dry-run', action='store_true',
                        help='Validate and list the plan without creating files')
    args = parser.parse_args()
    try:
        targets = install(args.dest, dry_run=args.dry_run)
    except (OSError, ValueError) as error:
        print(f'Installation stopped: {error}', file=sys.stderr)
        return 1
    for target in targets:
        print(f'{"Would install" if args.dry_run else "Installed"}: {target}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
