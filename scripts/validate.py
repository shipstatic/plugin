#!/usr/bin/env python3
"""The plugin's own checks, run by validate.yml on both branches and by
release.yml on the tagged commit.

    python3 scripts/validate.py              # the package and the history
    python3 scripts/validate.py --tag v4.0.0 # also: the tag equals every version

Every manifest is a file a host reads with no import, so the facts they share
(the name, the version, the one server's URL) are restated, and this script is
what compares the copies. Comparisons against other repos (the skill's tool
names against the MCP catalogue, the logo against the website's) live in the
monorepo's scripts/check-canon.sh, so a release here never goes red because
another repo moved.
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


def relative_path_exists(owner, value):
    if not isinstance(value, str) or value.startswith(("http://", "https://")):
        return
    if value.startswith("/") or ".." in value.split("/"):
        fail(f"{owner}: path {value!r} must be relative, inside the repo")
    elif not os.path.exists(value):
        fail(f"{owner}: names {value!r}, which does not exist")


def check_package():
    data = {path: load(path) for path in MANIFESTS}
    if any(value is None for value in data.values()):
        return

    # One name.
    names = {
        ".claude-plugin/plugin.json": data[".claude-plugin/plugin.json"]["name"],
        ".codex-plugin/plugin.json": data[".codex-plugin/plugin.json"]["name"],
        ".cursor-plugin/plugin.json": data[".cursor-plugin/plugin.json"]["name"],
        "gemini-extension.json": data["gemini-extension.json"]["name"],
    }
    for market in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"):
        entries = data[market].get("plugins", [])
        if len(entries) != 1:
            fail(f"{market}: lists {len(entries)} plugins, not one")
            continue
        names[market] = entries[0].get("name")
    for path, name in names.items():
        if name != NAME:
            fail(f"{path}: name is {name!r}, not {NAME!r}")

    # Every marketplace entry is this repo's root.
    if data[".claude-plugin/marketplace.json"]["plugins"][0].get("source") != "./":
        fail(".claude-plugin/marketplace.json: source is not the repo root './'")
    codex_entry = data[".agents/plugins/marketplace.json"]["plugins"][0]
    if codex_entry.get("source") != {"source": "local", "path": "./"}:
        fail(".agents/plugins/marketplace.json: source is not the repo root")
    # Sign-in comes at first use: an account at install would end publishing
    # with no account (plan-plugin.md §2).
    if codex_entry.get("policy", {}).get("authentication") != "ON_USE":
        fail(".agents/plugins/marketplace.json: authentication must be ON_USE")

    # One version.
    versions = {path: data[path].get("version") for path in VERSIONED}
    if len(set(versions.values())) != 1:
        fail(f"the manifests state more than one version: {versions}")

    # Exactly one server, the plain production URL, stated twice: once in
    # .mcp.json and once under Gemini's own key.
    servers = data[".mcp.json"].get("mcpServers", {})
    if list(servers) != [NAME]:
        fail(f".mcp.json: servers are {list(servers)}, not exactly [{NAME!r}]")
    elif servers[NAME] != {"type": "http", "url": URL}:
        fail(f".mcp.json: the server is {servers[NAME]}, not the plain URL {URL}")
    gemini = data["gemini-extension.json"].get("mcpServers", {})
    if gemini != {NAME: {"httpUrl": URL}}:
        fail(f"gemini-extension.json: mcpServers is {gemini}, not one server at {URL}")
    for path in (".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"):
        if data[path].get("mcpServers") != "./.mcp.json":
            fail(f"{path}: mcpServers does not name ./.mcp.json")

    # The one server is .mcp.json's alone: no manifest declares a server,
    # hooks, commands, agents or rules of its own beside it.
    for path in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"):
        extra = sorted({"hooks", "commands", "agents", "rules"} & set(data[path]))
        if path == ".claude-plugin/plugin.json" and "mcpServers" in data[path]:
            extra.append("mcpServers")
        if extra:
            fail(f"{path}: declares {extra}; the plugin is .mcp.json and one skill")

    # Every path a manifest names exists.
    for path in (".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"):
        manifest = data[path]
        for key in ("skills", "mcpServers", "logo"):
            relative_path_exists(path, manifest.get(key))
        for key in ("logo", "composerIcon"):
            relative_path_exists(path, manifest.get("interface", {}).get(key))

    # The major is the CLI's: the skill runs `@shipstatic/ship@N`, and the
    # plugin's major says which N, as the GitHub Action's major does. A move
    # to the next CLI major is the plugin's next major, never a silent one.
    with open("skills/publish-online/SKILL.md", encoding="utf-8") as f:
        pins = set(re.findall(r"@shipstatic/ship@(\d+)\b", f.read()))
    majors = {str(v).split(".")[0] for v in versions.values()}
    if len(pins) != 1:
        fail(f"skills/publish-online/SKILL.md: pins the CLI at {sorted(pins) or 'no'} majors, not one")
    elif pins != majors:
        fail(f"the plugin's major {sorted(majors)} is not the CLI major its skill runs ({pins.pop()})")

    # One skill to start with, by decision (plan-plugin.md D3). A next one,
    # such as a custom domain, is a decision recorded there first, then a
    # line here.
    folders = sorted(os.listdir("skills"))
    if folders != ["publish-online"]:
        fail(f"skills/ holds {folders}, not the one skill ['publish-online']")

    # Each skill is named for its folder.
    for folder in folders:
        skill = os.path.join("skills", folder, "SKILL.md")
        if not os.path.isfile(skill):
            fail(f"skills/{folder}: has no SKILL.md")
            continue
        with open(skill, encoding="utf-8") as f:
            match = re.match(r"---\nname: (\S+)\ndescription: .+\n---\n", f.read())
        if not match:
            fail(f"{skill}: frontmatter is not 'name' then 'description'")
        elif match.group(1) != folder:
            fail(f"{skill}: is named {match.group(1)!r}, its folder {folder!r}")

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
    # HEAD too, so a pull request's own commits are read before they merge.
    refs = ["HEAD"] + [line for line in git("for-each-ref", "--format=%(refname)",
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
        if re.search(r"^co-authored-by:", body, re.I | re.M):
            fail(f"history: {sha[:7]} carries a Co-Authored-By trailer")
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
