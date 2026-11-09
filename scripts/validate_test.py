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
SOMEONE = {"GIT_AUTHOR_NAME": "Someone Else", "GIT_AUTHOR_EMAIL": "someone@example.com",
           "GIT_COMMITTER_NAME": "Someone Else", "GIT_COMMITTER_EMAIL": "someone@example.com"}
CLAUDE, CODEX, CURSOR = ".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"
GEMINI, MCP = "gemini-extension.json", ".mcp.json"
CLAUDE_MARKET, CODEX_MARKET = ".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"
SKILL = "skills/publish-online/SKILL.md"


def edit(path, change):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    change(data)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def rewrite(path, old, new):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    assert old in text, (path, old)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(old, new))


def every_version(value):
    def plant(tree):
        for path in (CLAUDE, CODEX, CURSOR, GEMINI):
            edit(path, lambda data: data.update(version=value))
    return plant


def link_to_outside(tree):
    # The same bytes, moved outside the repo and linked back: only the mode
    # tells them apart.
    outside = os.path.join(os.path.dirname(tree), "outside.json")
    shutil.move(CLAUDE, outside)
    os.symlink(outside, CLAUDE)


def logo_names_a_directory(tree):
    # Every manifest agrees on a path that git tracks as a folder, not a file.
    edit(CLAUDE, lambda d: d.update(icon="./skills"))
    edit(CURSOR, lambda d: d.update(logo="./skills"))
    edit(CODEX, lambda d: d["interface"].update(logo="./skills", composerIcon="./skills"))


def new_file(name):
    def plant(tree):
        with open(name, "w", encoding="utf-8") as f:
            f.write("loaded by a host, named by no manifest\n")
    return plant


# (what is planted, how, the words validate.py must answer with). A plant of
# None leaves the package as it is; `args`, `identity` and `message` reach the
# temporary repository's commit and the validate.py call.
CASES = [
    # The package's files.
    ("a link in place of a manifest", link_to_outside, "git mode 120000"),
    ("an executable file", lambda tree: os.chmod("scripts/validate.py", 0o755), "git mode 100755"),
    ("a missing file", lambda tree: os.remove("README.md"), "README.md: one of the plugin's files is missing"),
    ("a file no host should load", new_file("GEMINI.md"), "GEMINI.md: not one of the plugin's files"),
    ("an eval file that is not text of a known kind", new_file("evals/notes.txt"),
     "evals/notes.txt: not one of the plugin's files"),
    ("no eval cases", lambda tree: shutil.rmtree("evals"), "holds no eval cases"),
    # The shape.
    ("a key outside the shape", lambda tree: edit(CLAUDE, lambda d: d.update(hooks="./hooks.json")),
     "outside the plugin's fixed shape"),
    ("a key the shape holds, dropped", lambda tree: edit(CURSOR, lambda d: d.pop("keywords")), "lacks ['keywords']"),
    ("a description that is not a string", lambda tree: edit(CODEX, lambda d: d.update(description=False)),
     "description is False, not string"),
    ("prompts that are not a list of strings",
     lambda tree: edit(CODEX, lambda d: d["interface"].update(defaultPrompt=42)), "defaultPrompt is 42, not strings"),
    # One name, one version, one server.
    ("a manifest with another name", lambda tree: edit(CURSOR, lambda d: d.update(name="shipstatic-cursor")),
     "name is 'shipstatic-cursor', not 'shipstatic'"),
    ("a version that is not semantic", every_version("3"), "is not MAJOR.MINOR.PATCH"),
    ("two versions", lambda tree: edit(GEMINI, lambda d: d.update(version="3.0.0")), "more than one version"),
    ("a server at another URL",
     lambda tree: edit(MCP, lambda d: d["mcpServers"]["shipstatic"].update(url="https://mcp.example.com")),
     "not the plain URL"),
    ("Gemini's server at another URL",
     lambda tree: edit(GEMINI, lambda d: d["mcpServers"]["shipstatic"].update(httpUrl="https://mcp.example.com")),
     "not one server at"),
    # The marketplaces.
    ("a Claude marketplace entry outside the root",
     lambda tree: edit(CLAUDE_MARKET, lambda d: d["plugins"][0].update(source="./plugins/shipstatic")),
     "source is not the repo root './'"),
    ("a Codex marketplace entry outside the root",
     lambda tree: edit(CODEX_MARKET, lambda d: d["plugins"][0]["source"].update(path="./plugins/shipstatic")),
     "source is not the repo root"),
    ("sign-in at install",
     lambda tree: edit(CODEX_MARKET, lambda d: d["plugins"][0]["policy"].update(authentication="ON_INSTALL")),
     "authentication ON_USE"),
    # The paths the manifests name.
    ("a Codex manifest naming another MCP file", lambda tree: edit(CODEX, lambda d: d.update(mcpServers="./mcp.json")),
     "mcpServers does not name ./.mcp.json"),
    ("a Cursor manifest naming another skills folder", lambda tree: edit(CURSOR, lambda d: d.update(skills="./skill/")),
     "skills does not name ./skills/"),
    ("a logo outside the repo", lambda tree: edit(CURSOR, lambda d: d.update(logo="../logo")),
     "must be relative, inside the repo"),
    ("two logos", lambda tree: edit(CURSOR, lambda d: d.update(logo="./assets/other.png")), "more than one logo"),
    ("a logo path that is a folder", logo_names_a_directory, "which is not a tracked file"),
    # One fact, restated.
    ("a listing link that differs from Codex's",
     lambda tree: edit(CLAUDE, lambda d: d.update(supportUrl="https://example.com")),
     "the support link differs between manifests"),
    ("a license that differs between manifests", lambda tree: edit(CURSOR, lambda d: d.update(license="ISC")),
     "the license differs between manifests"),
    ("a marketplace entry with its own description",
     lambda tree: edit(CLAUDE_MARKET, lambda d: d["plugins"][0].update(description="Something else.")),
     "the description differs between manifests"),
    # The skill.
    ("a skill running another CLI major", lambda tree: rewrite(SKILL, "@shipstatic/ship@3", "@shipstatic/ship@2"),
     "runs @shipstatic/ship@2, not @shipstatic/ship@3"),
    ("a skill folder with another name", lambda tree: shutil.move("skills/publish-online", "skills/publish"),
     "skills/ holds ['publish'], not the one skill"),
    ("a skill whose frontmatter opens with something else",
     lambda tree: rewrite(SKILL, "---\nname: publish-online\n", "---\nversion: 1\nname: publish-online\n"),
     "frontmatter is not 'name' then 'description'"),
    # The tag and the history.
    ("a tag that is not the version", None, "but the tag is v9.9.9", {"args": ["--tag", "v9.9.9"]}),
    ("a commit by someone else", None, "is by Someone Else <someone@example.com>", {"identity": SOMEONE}),
    ("a commit with an attribution line", None, "carries an attribution line",
     {"message": "The package\n\nCo-Authored-By: An Assistant <assistant@example.com>"}),
]


def run(plant, args=(), identity=IDENTITY, message="The package"):
    """Copy the package, plant a defect, commit it, and run validate.py."""
    with tempfile.TemporaryDirectory() as base:
        tree = os.path.join(base, "plugin")
        files = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True, capture_output=True,
                               text=True).stdout.splitlines()
        for path in files:
            os.makedirs(os.path.join(tree, os.path.dirname(path)), exist_ok=True)
            shutil.copy2(os.path.join(ROOT, path), os.path.join(tree, path))
        env = {key: value for key, value in os.environ.items() if key != "HISTORY_HEAD"}
        env.update(identity)
        here = os.getcwd()
        os.chdir(tree)
        try:
            if plant:
                plant(tree)
            for git_args in (["init", "--quiet"], ["add", "--all"], ["commit", "--quiet", "-m", message]):
                subprocess.run(GIT + git_args, check=True, env=env, capture_output=True)
            result = subprocess.run([sys.executable, "scripts/validate.py", *args], env=env,
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
    for name, plant, message, *rest in CASES:
        code, output = run(plant, **(rest[0] if rest else {}))
        if code != 0 and message in output:
            print(f"✓ {name}: refused")
        else:
            failed = True
            print(f"✗ {name}: validate.py exited {code} without {message!r}:\n{output}")
    sys.exit(1 if failed else 0)


main()
