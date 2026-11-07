#!/usr/bin/env python3
"""Point Formula/my-tui.rb at a my-tui release and push this tap.

Usage: python3 bump-formula.py 0.1.5
       python3 bump-formula.py v0.1.5
"""

from __future__ import annotations

import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FORMULA = ROOT / "Formula" / "my-tui.rb"
REPOSITORY = "rogerwcpt/weissdigital-my-tui"
ARCHIVES = ("osx-arm64",)
VERSION = re.compile(r"^v?(\d+\.\d+\.\d+)$")
SHA = re.compile(r"^[0-9a-f]{64}$")


def version_number(argument: str) -> str:
    match = VERSION.fullmatch(argument.strip())
    if match is None:
        raise SystemExit("Version must look like 0.1.5 or v0.1.5.")
    return match.group(1)


def release_checksums(version: str) -> dict[str, str]:
    url = f"https://github.com/{REPOSITORY}/releases/download/v{version}/SHA256SUMS"
    request = urllib.request.Request(url, headers={"User-Agent": "my-tui-homebrew-bump"})
    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode()
    except urllib.error.HTTPError as error:
        raise SystemExit(f"No SHA256SUMS for v{version} ({error.code}).") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"Could not download checksums for v{version}: {error.reason}") from error

    found: dict[str, str] = {}
    for line in body.splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        found[name] = digest

    needed: dict[str, str] = {}
    for archive in ARCHIVES:
        name = f"my-tui-{version}-{archive}.tar.gz"
        digest = found.get(name)
        if digest is None or SHA.fullmatch(digest) is None:
            raise SystemExit(f"SHA256SUMS has no checksum for {name}.")
        needed[archive] = digest
    return needed


def update_formula(text: str, version: str, checksums: dict[str, str]) -> str:
    updated = text
    for archive, digest in checksums.items():
        pattern = (
            rf'^(\s*)url "https://github.com/{re.escape(REPOSITORY)}/releases/download/'
            rf'v[^"]+/my-tui-[^"]+-{re.escape(archive)}\.tar\.gz"\n'
            rf'(\s*)sha256 "[^"]+"'
        )
        replacement = (
            rf'\1url "https://github.com/{REPOSITORY}/releases/download/v{version}/'
            rf'my-tui-{version}-{archive}.tar.gz"\n'
            rf'\2sha256 "{digest}"'
        )
        updated, count = re.subn(pattern, replacement, updated, count=1, flags=re.MULTILINE)
        if count != 1:
            raise SystemExit(f"The formula has no {archive} url and sha256.")
    return updated


def git(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise SystemExit(detail or f"git {' '.join(args)} failed.")
    return result


def commit_and_push(version: str) -> None:
    git(["add", "--", "Formula/my-tui.rb"])
    staged = git(["diff", "--cached", "--quiet"], check=False)
    if staged.returncode == 0:
        raise SystemExit(f"Formula/my-tui.rb is already at {version}.")
    git(["commit", "-m", f"Update my-tui to {version}."])
    upstream = git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"], check=False)
    if upstream.returncode == 0:
        git(["push"])
    else:
        git(["push", "-u", "origin", "HEAD"])


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 bump-formula.py 0.1.5")
    version = version_number(sys.argv[1])
    if not FORMULA.is_file():
        raise SystemExit(f"Missing {FORMULA}.")
    original = FORMULA.read_text()
    FORMULA.write_text(update_formula(original, version, release_checksums(version)))
    commit_and_push(version)
    print(f"Pushed my-tui {version}.")


if __name__ == "__main__":
    main()
