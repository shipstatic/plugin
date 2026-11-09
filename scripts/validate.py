#!/usr/bin/env python3
"""The plugin's own checks, run by validate.yml on both branches and by
release.yml on the tagged commit.

    python3 scripts/validate.py              # the package and the history
    python3 scripts/validate.py --tag vX.Y.Z # also: the tag equals every version

Every manifest is a file a host reads with no import, so the facts they share
(the name, the version, the one server's URL) are restated, and this script is
what compares the copies. Comparisons against other repos (the skill's tool
names against the MCP catalogue, the logo against the website's) live in a
check outside this repo, so a release here never goes red because another
repo moved.
"""

import json
import os
import re
import subprocess
import sys

NAME = "shipstatic"
URL = "https://mcp.shipstatic.com"
IDENTITY = "ShipStatic <hello@shipstatic.com>"
# A commit made in GitHub's web interface: GitHub commits it, the account
# authors it.
WEB_AUTHOR = "shipstatic-com <hello@shipstatic.com>"
WEB_COMMITTER = "GitHub <noreply@github.com>"

MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    ".cursor-plugin/plugin.json",
    "gemini-extension.json",
    ".mcp.json",
]
VERSIONED = [
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    "gemini-extension.json",
]

# What a value may be. A host reads these files with its own parser, so a
# string where a list belongs is a broken listing that no JSON check sees.
TYPES = {
    "string": lambda v: isinstance(v, str),
    "strings": lambda v: isinstance(v, list) and all(isinstance(x, str) for x in v),
    "object": lambda v: isinstance(v, dict),
    "objects": lambda v: isinstance(v, list) and all(isinstance(x, dict) for x in v),
}
S, SS, O, OS = "string", "strings", "object", "objects"

# The package's shape is fixed: each manifest holds exactly these keys, each
# of its type. A key added (a second server, hooks, an app, a context file)
# or dropped is a change to the plugin's shape: a design decision first,
# written here after.
SHAPE = {
    ".claude-plugin/plugin.json": {
        "$schema": S, "name": S, "displayName": S, "version": S, "description": S, "icon": S,
        "author": O, "homepage": S, "documentationUrl": S, "supportUrl": S, "privacyPolicyUrl": S,
        "termsOfServiceUrl": S, "repository": S, "license": S, "keywords": SS,
    },
    ".claude-plugin/marketplace.json": {"name": S, "owner": O, "description": S, "plugins": OS},
    ".codex-plugin/plugin.json": {
        "name": S, "version": S, "description": S, "author": O, "homepage": S, "repository": S,
        "license": S, "keywords": SS, "skills": S, "mcpServers": S, "interface": O,
    },
    ".agents/plugins/marketplace.json": {"name": S, "interface": O, "plugins": OS},
    ".cursor-plugin/plugin.json": {
        "name": S, "version": S, "description": S, "author": O, "homepage": S, "repository": S,
        "license": S, "keywords": SS, "logo": S, "skills": S, "mcpServers": S,
    },
    "gemini-extension.json": {"name": S, "version": S, "description": S, "mcpServers": O},
    ".mcp.json": {"mcpServers": O},
}
# Codex's listing, under its manifest's `interface`.
INTERFACE = {
    "displayName": S, "shortDescription": S, "longDescription": S, "developerName": S,
    "category": S, "capabilities": SS, "websiteURL": S, "privacyPolicyURL": S,
    "termsOfServiceURL": S, "supportURL": S, "defaultPrompt": SS, "composerIcon": S, "logo": S,
}
# A fact the host manifests restate is one fact. Each row names the places
# that hold it, as a file and a dotted path into it, and the places must
# agree. The Claude directory reads its listing's links from the Claude
# manifest and Codex's listing carries the same links under `interface`,
# spelled `...URL` where Anthropic spells `...Url`. Gemini's description is
# its own, for Gemini's gallery, so it is no row.
CLAUDE, CODEX, CURSOR = ".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"
CLAUDE_MARKET, CODEX_MARKET = ".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"
SHARED = {
    "description": [(CLAUDE, "description"), (CODEX, "description"), (CURSOR, "description"),
                    (CLAUDE_MARKET, "plugins.0.description")],
    "display name": [(CLAUDE, "displayName"), (CODEX, "interface.displayName"),
                     (CODEX_MARKET, "interface.displayName")],
    "homepage": [(CLAUDE, "homepage"), (CODEX, "homepage"), (CURSOR, "homepage"),
                 (CODEX, "interface.websiteURL")],
    "repository": [(CLAUDE, "repository"), (CODEX, "repository"), (CURSOR, "repository")],
    "license": [(CLAUDE, "license"), (CODEX, "license"), (CURSOR, "license")],
    "keywords": [(CLAUDE, "keywords"), (CODEX, "keywords"), (CURSOR, "keywords")],
    "author name": [(CLAUDE, "author.name"), (CODEX, "author.name"), (CURSOR, "author.name"),
                    (CLAUDE_MARKET, "owner.name"), (CODEX, "interface.developerName")],
    "author email": [(CLAUDE, "author.email"), (CODEX, "author.email"), (CURSOR, "author.email"),
                     (CLAUDE_MARKET, "owner.email")],
    "support link": [(CLAUDE, "supportUrl"), (CODEX, "interface.supportURL")],
    "privacy link": [(CLAUDE, "privacyPolicyUrl"), (CODEX, "interface.privacyPolicyURL")],
    "terms link": [(CLAUDE, "termsOfServiceUrl"), (CODEX, "interface.termsOfServiceURL")],
}
# The one entry each marketplace lists.
ENTRY = {
    ".claude-plugin/marketplace.json": {"name": S, "source": S, "description": S, "category": S},
    ".agents/plugins/marketplace.json": {"name": S, "source": O, "policy": O, "category": S},
}
# The text files of the package. Hosts load more than manifests name (Gemini
# a root GEMINI.md, Cursor and Codex a root plugin.json, Claude Code a
# commands/ folder), so the list of files is the one check that covers every
# way in at once. A new file is a decision recorded first.
#
# The logo is the package's one image, and it is not listed: the Claude
# directory holds a plugin for review when a script writes a bundled image's
# path. The manifests name it, and this script reads the path from them.
FILES = {
    ".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json",
    ".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json",
    ".claude/CLAUDE.md", ".github/workflows/release.yml", ".github/workflows/validate.yml",
    ".mcp.json", "AGENTS.md", "LICENSE", "README.md", "gemini-extension.json",
    "scripts/validate.py", "scripts/validate_test.py", "skills/publish-online/SKILL.md",
}
# The eval cases (claude plugin eval), run by hand before a release that
# changes the skill. Each case is a folder of text: its case, its mocks and
# the script that sets up its files.
EVALS, EVAL_SUFFIXES = "evals/", (".yaml", ".md", ".sh")
# Git's mode for a regular file. The directory refuses links and submodules,
# and a link would let a manifest's path reach outside the repo.
REGULAR = "100644"
# MAJOR.MINOR.PATCH, as Cursor documents `version`, with no leading zeros.
SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")

failures = []


def fail(message):
    failures.append(message)


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as error:
        fail(f"{path}: not readable JSON ({error})")
        return None


def shaped(owner, value, shape):
    """True when `value` holds exactly the keys of `shape`, each of its type."""
    before = len(failures)
    extra = sorted(set(value) - set(shape))
    missing = sorted(set(shape) - set(value))
    if extra:
        fail(f"{owner}: carries {extra}, outside the plugin's fixed shape")
    if missing:
        fail(f"{owner}: lacks {missing}, which the plugin's fixed shape holds")
    for key, kind in shape.items():
        if key in value and not TYPES[kind](value[key]):
            fail(f"{owner}: {key} is {value[key]!r}, not {kind}")
    return len(failures) == before


def pick(value, dotted):
    """The value at a dotted path, through objects and lists."""
    for part in dotted.split("."):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def inside(owner, value):
    """A path a manifest names, relative and inside the repo, as git lists it."""
    parts = value.split("/")
    if value.startswith("/") or ".." in parts:
        fail(f"{owner}: path {value!r} must be relative, inside the repo")
        return None
    return "/".join(part for part in parts if part not in ("", "."))


def check_package():
    data = {path: load(path) for path in MANIFESTS}
    if any(value is None for value in data.values()):
        return None

    # Every check below reads the shape, so a manifest out of shape stops
    # here, with what is wrong.
    if not all([shaped(path, data[path], SHAPE[path]) for path in MANIFESTS]):
        return None
    inner = [(".codex-plugin/plugin.json: its interface",
              data[".codex-plugin/plugin.json"]["interface"], INTERFACE)]
    for market, shape in ENTRY.items():
        entries = data[market]["plugins"]
        if len(entries) != 1:
            fail(f"{market}: lists {len(entries)} plugins, not one")
            return None
        inner.append((f"{market}: its entry", entries[0], shape))
    if not all([shaped(*args) for args in inner]):
        return None

    claude, codex, cursor = (data[f".{host}-plugin/plugin.json"] for host in ("claude", "codex", "cursor"))
    claude_entry = data[".claude-plugin/marketplace.json"]["plugins"][0]
    codex_entry = data[".agents/plugins/marketplace.json"]["plugins"][0]

    # One name.
    names = {path: data[path]["name"] for path in VERSIONED}
    names[".claude-plugin/marketplace.json: its entry"] = claude_entry["name"]
    names[".agents/plugins/marketplace.json: its entry"] = codex_entry["name"]
    for market in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"):
        names[f"{market}: the marketplace"] = data[market]["name"]
    for path, name in names.items():
        if name != NAME:
            fail(f"{path}: name is {name!r}, not {NAME!r}")

    # Every marketplace entry is this repo's root.
    if claude_entry["source"] != "./":
        fail(".claude-plugin/marketplace.json: source is not the repo root './'")
    if codex_entry["source"] != {"source": "local", "path": "./"}:
        fail(".agents/plugins/marketplace.json: source is not the repo root")
    # Sign-in comes at first use: an account at install would end publishing
    # with no account.
    if codex_entry["policy"] != {"installation": "AVAILABLE", "authentication": "ON_USE"}:
        fail(".agents/plugins/marketplace.json: policy must be installation AVAILABLE, authentication ON_USE")

    # One version, and a semantic one.
    versions = {path: data[path]["version"] for path in VERSIONED}
    if len(set(versions.values())) != 1:
        fail(f"the manifests state more than one version: {versions}")
    for path, version in versions.items():
        if not SEMVER.fullmatch(version):
            fail(f"{path}: version {version!r} is not MAJOR.MINOR.PATCH")

    # Exactly one server, the plain production URL, stated twice: once in
    # .mcp.json and once under Gemini's own key.
    servers = data[".mcp.json"]["mcpServers"]
    if list(servers) != [NAME]:
        fail(f".mcp.json: servers are {list(servers)}, not exactly [{NAME!r}]")
    elif servers[NAME] != {"type": "http", "url": URL}:
        fail(f".mcp.json: the server is {servers[NAME]}, not the plain URL {URL}")
    gemini = data["gemini-extension.json"]["mcpServers"]
    if gemini != {NAME: {"httpUrl": URL}}:
        fail(f"gemini-extension.json: mcpServers is {gemini}, not one server at {URL}")
    # The shape is fixed, so the paths are checked as values, not as files
    # that happen to exist.
    for path, manifest in ((".codex-plugin/plugin.json", codex), (".cursor-plugin/plugin.json", cursor)):
        if manifest["mcpServers"] != "./.mcp.json":
            fail(f"{path}: mcpServers does not name ./.mcp.json")
        if manifest["skills"] != "./skills/":
            fail(f"{path}: skills does not name ./skills/")

    for fact, places in SHARED.items():
        values = {f"{path}: {dotted}": pick(data[path], dotted) for path, dotted in places}
        if len({json.dumps(v, sort_keys=True) for v in values.values()}) != 1:
            fail(f"the {fact} differs between manifests: {values}")

    # The logo, wherever a manifest names it. Its path is read here and never
    # opened: git's index below proves it is a tracked regular file.
    named = {
        ".claude-plugin/plugin.json: icon": claude["icon"],
        ".cursor-plugin/plugin.json: logo": cursor["logo"],
        ".codex-plugin/plugin.json: interface.logo": codex["interface"]["logo"],
        ".codex-plugin/plugin.json: interface.composerIcon": codex["interface"]["composerIcon"],
    }
    images = {owner: inside(owner, value) for owner, value in named.items()}
    if None in images.values():
        return None
    if len(set(images.values())) != 1:
        fail(f"the manifests name more than one logo: {named}")

    # The package is exactly its files, each a regular file, wherever a host
    # might look.
    modes = {}
    for line in git("ls-files", "-s").splitlines():
        meta, path = line.split("\t", 1)
        modes[path] = meta.split()[0]
    for path, mode in sorted(modes.items()):
        if mode != REGULAR:
            fail(f"{path}: git mode {mode}, not a regular file ({REGULAR})")
    for owner, image in images.items():
        if image not in modes:
            fail(f"{owner}: names {image!r}, which is not a tracked file")
    package = FILES | set(images.values())
    cases = {path for path in modes if path.startswith(EVALS) and path.endswith(EVAL_SUFFIXES)}
    if not cases:
        fail(f"{EVALS}: holds no eval cases")
    for path in sorted(set(modes) - package - cases):
        fail(f"{path}: not one of the plugin's files")
    for path in sorted(FILES - set(modes)):
        fail(f"{path}: one of the plugin's files is missing")

    # One skill, by decision. A next one, such as a custom domain, is a
    # design decision first, then a line here.
    folders = sorted(os.listdir("skills"))
    if folders != ["publish-online"]:
        fail(f"skills/ holds {folders}, not the one skill ['publish-online']")

    # Each skill is named for its folder, and runs the CLI at the plugin's
    # major: the skill runs `@shipstatic/ship@N`, and the plugin's major says
    # which N, as the GitHub Action's major does, so a move to the next CLI
    # major is the plugin's next major, never a silent one. Every mention of
    # the package must be exactly `@N`: no `@latest`, no exact version, no
    # bare name.
    majors = {v.split(".")[0] for v in versions.values()}
    want = f"@{majors.pop()}" if len(majors) == 1 else None
    for folder in folders:
        skill = os.path.join("skills", folder, "SKILL.md")
        if not os.path.isfile(skill):
            fail(f"skills/{folder}: has no SKILL.md")
            continue
        with open(skill, encoding="utf-8") as f:
            text = f.read()
        match = re.match(r"---\nname: (\S+)\ndescription: .+\n---\n", text)
        if not match:
            fail(f"{skill}: frontmatter is not 'name' then 'description'")
        elif match.group(1) != folder:
            fail(f"{skill}: is named {match.group(1)!r}, its folder {folder!r}")
        specs = re.findall(r"@shipstatic/ship(@[^\s`]*)?", text)
        if not specs:
            fail(f"{skill}: never names @shipstatic/ship")
        for spec in specs:
            if spec != want:
                fail(f"{skill}: runs @shipstatic/ship{spec}, not @shipstatic/ship{want}")

    return versions


def check_tag(tag, versions):
    want = tag.removeprefix("v")
    for path, version in versions.items():
        if version != want:
            fail(f"{path}: version {version}, but the tag is {tag}")


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def check_history():
    """Every commit on every remote branch and tag names only ShipStatic."""
    # The commit under check too, so a pull request's own commits are read
    # before they merge. On a pull request that is the PR's head
    # (HISTORY_HEAD, from validate.yml), never the checked-out HEAD: that is
    # GitHub's merge commit, which GitHub authors.
    head = os.environ.get("HISTORY_HEAD") or "HEAD"
    refs = [head] + [line for line in git("for-each-ref", "--format=%(refname)",
                                            "refs/remotes/origin", "refs/tags").splitlines()
                       if not line.endswith("/HEAD")]
    if not refs:
        fail("history: no remote branches or tags were fetched to check")
        return
    log = git("log", "--format=%H%x1f%an <%ae>%x1f%cn <%ce>%x1f%B%x1e", *refs)
    count = 0
    for record in filter(str.strip, log.split("\x1e")):
        sha, author, committer, body = record.strip("\n").split("\x1f", 3)
        count += 1
        ours = author == IDENTITY and committer == IDENTITY
        web = author == WEB_AUTHOR and committer == WEB_COMMITTER
        if not (ours or web):
            fail(f"history: {sha[:7]} is by {author}, committed by {committer}")
        if re.search(r"^(co-authored-by|claude-session):|claude\.ai/code/session", body, re.I | re.M):
            fail(f"history: {sha[:7]} carries an attribution line")
    print(f"history: {count} commits across {len(refs)} refs")


def main():
    args = sys.argv[1:]
    tag = args[args.index("--tag") + 1] if "--tag" in args else None
    versions = check_package()
    if tag and versions:
        check_tag(tag, versions)
    check_history()
    for message in failures:
        print(f"::error::{message}")
    if failures:
        sys.exit(1)
    print("the plugin is consistent")


main()
