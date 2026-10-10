#!/usr/bin/env python3
"""Publish the tiny installable skill to skill-only in the same GitHub repo.

This uses a temporary Git index and does not switch or rewrite the main checkout.
The new commit is a normal fast-forward child of the current skill-only branch.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skill" / "source-to-motion"
BRANCH = "skill-only"


def git(*args: str, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=True, timeout=120)
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Build and compare the skill tree without publishing")
    args = parser.parse_args()
    subprocess.run([sys.executable, str(ROOT / "scripts/sync_skill_package.py"), "--check"],
                   cwd=ROOT, check=True, timeout=30)
    files = sorted(p for p in PACKAGE.rglob("*") if p.is_file()
                   and "__pycache__" not in p.parts and p.suffix != ".pyc")
    if not files or not (PACKAGE / "SKILL.md").is_file():
        raise SystemExit("Installable skill package is empty")
    with tempfile.TemporaryDirectory(prefix="stm-skill-index-") as tmp:
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = str(Path(tmp) / "index")
        git("read-tree", "--empty", env=env)
        for file in files:
            rel = file.relative_to(PACKAGE).as_posix()
            oid = git("hash-object", "-w", str(file))
            git("update-index", "--add", "--cacheinfo", f"100644,{oid},{rel}", env=env)
        tree = git("write-tree", env=env)
    remote = git("ls-remote", "--heads", "origin", BRANCH)
    parent = None
    if remote:
        git("fetch", "--depth=1", "origin", f"refs/heads/{BRANCH}")
        parent = git("rev-parse", "FETCH_HEAD")
        if tree == git("rev-parse", f"{parent}^{{tree}}"):
            print(f"{BRANCH} is already current")
            return
    if args.dry_run:
        print(f"Would publish {len(files)} files ({tree[:12]}) to {BRANCH}")
        return
    env = os.environ.copy()
    env.update({
        "GIT_AUTHOR_NAME": "Source to Motion",
        "GIT_AUTHOR_EMAIL": "source-to-motion@users.noreply.github.com",
        "GIT_COMMITTER_NAME": "Source to Motion",
        "GIT_COMMITTER_EMAIL": "source-to-motion@users.noreply.github.com",
    })
    message = f"Sync lightweight skill from main {git('rev-parse', '--short', 'HEAD')}"
    args = ["commit-tree", tree, "-m", message]
    if parent:
        args += ["-p", parent]
    commit = git(*args, env=env)
    git("push", "origin", f"{commit}:refs/heads/{BRANCH}")
    print(f"Published {len(files)} files ({commit[:12]}) to {BRANCH}")


if __name__ == "__main__":
    main()
