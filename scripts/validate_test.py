#!/usr/bin/env python3
"""validate.py's checks, each drilled against the input it refuses.

    python3 scripts/validate_test.py

Each case copies the package into a new repository, plants one defect, and
asserts that validate.py fails with the message naming that defect. The
untouched copy must pass first, so a case that fails proves its check and
not a broken copy.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIT = ["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
       "-c", "init.defaultBranch=main"]
IDENTITY = {"GIT_AUTHOR_NAME": "ShipStatic", "GIT_AUTHOR_EMAIL": "hello@shipstatic.com",
            "GIT_COMMITTER_NAME": "ShipStatic", "GIT_COMMITTER_EMAIL": "hello@shipstatic.com"}


def edit(path, change):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    change(data)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def every_version(value):
    def plant(tree):
        for path in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json",
                     ".cursor-plugin/plugin.json", "gemini-extension.json"):
            edit(path, lambda data: data.update(version=value))
    return plant


def link_to_outside(tree):
    # The same bytes, moved outside the repo and linked back: only the mode
    # tells them apart.
    outside = os.path.join(os.path.dirname(tree), "outside.json")
    shutil.move(".claude-plugin/plugin.json", outside)
    os.symlink(outside, ".claude-plugin/plugin.json")


def directory_at_logo(tree):
    with open(".cursor-plugin/plugin.json", encoding="utf-8") as f:
        logo = json.load(f)["logo"]
    os.remove(logo)
    os.mkdir(logo)
    with open(os.path.join(logo, "inside.txt"), "w", encoding="utf-8") as f:
        f.write("not an image\n")


def new_file(name):
    def plant(tree):
        with open(name, "w", encoding="utf-8") as f:
            f.write("loaded by a host, named by no manifest\n")
    return plant


CASES = [
    ("a link in place of a manifest", link_to_outside, "git mode 120000"),
    ("an executable file", lambda tree: os.chmod("scripts/validate.py", 0o755), "git mode 100755"),
    ("a missing file", lambda tree: os.remove("README.md"),
     "README.md: one of the plugin's files is missing"),
    ("a file no host should load", new_file("GEMINI.md"), "GEMINI.md: not one of the plugin's files"),
    ("a directory at the logo's path", directory_at_logo, "which is not a tracked file"),
    ("a logo outside the repo",
     lambda tree: edit(".cursor-plugin/plugin.json", lambda d: d.update(logo="../logo")),
     "must be relative, inside the repo"),
    ("a version that is not semantic", every_version("3"), "is not MAJOR.MINOR.PATCH"),
    ("two versions", lambda tree: edit("gemini-extension.json", lambda d: d.update(version="3.0.0")),
     "more than one version"),
    ("a description that is not a string",
     lambda tree: edit(".codex-plugin/plugin.json", lambda d: d.update(description=False)),
     "description is False, not string"),
    ("prompts that are not a list of strings",
     lambda tree: edit(".codex-plugin/plugin.json", lambda d: d["interface"].update(defaultPrompt=42)),
     "defaultPrompt is 42, not strings"),
    ("a listing link that differs from Codex's",
     lambda tree: edit(".claude-plugin/plugin.json", lambda d: d.update(supportUrl="https://example.com")),
     "but Codex's interface.supportURL"),
    ("a key outside the shape",
     lambda tree: edit(".claude-plugin/plugin.json", lambda d: d.update(hooks="./hooks.json")),
     "outside the plugin's fixed shape"),
    ("a key the shape holds, dropped",
     lambda tree: edit(".cursor-plugin/plugin.json", lambda d: d.pop("keywords")),
     "lacks ['keywords']"),
]


def run(plant):
    """Copy the package, plant a defect, commit it, and run validate.py."""
    with tempfile.TemporaryDirectory() as base:
        tree = os.path.join(base, "plugin")
        files = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True, capture_output=True,
                               text=True).stdout.splitlines()
        for path in files:
            os.makedirs(os.path.join(tree, os.path.dirname(path)), exist_ok=True)
            shutil.copy2(os.path.join(ROOT, path), os.path.join(tree, path))
        env = {key: value for key, value in os.environ.items() if key != "HISTORY_HEAD"}
        env.update(IDENTITY)
        here = os.getcwd()
        os.chdir(tree)
        try:
            if plant:
                plant(tree)
            for args in (["init", "--quiet"], ["add", "--all"], ["commit", "--quiet", "-m", "The package"]):
                subprocess.run(GIT + args, check=True, env=env, capture_output=True)
            result = subprocess.run([sys.executable, "scripts/validate.py"], env=env,
                                    capture_output=True, text=True)
        finally:
            os.chdir(here)
        return result.returncode, result.stdout + result.stderr


def main():
    failed = False
    code, output = run(None)
    if code != 0:
        print(f"✗ the package as it is fails validate.py, so no case below can prove anything:\n{output}")
        sys.exit(1)
    print("✓ the package as it is passes")
    for name, plant, message in CASES:
        code, output = run(plant)
        if code != 0 and message in output:
            print(f"✓ {name}: refused")
        else:
            failed = True
            print(f"✗ {name}: validate.py exited {code} without {message!r}:\n{output}")
    sys.exit(1 if failed else 0)


main()
