# CLAUDE.md

Claude Code instructions for **`shipstatic/plugin`, ShipStatic's plugin for
coding agents**.

## What this repo is, and what it is not

ShipStatic reaches AI hosts in two ways, and they never share a repo, a URL
or a release:

- **Connectors** are dedicated submissions to a chat app's directory, each a
  URL of its own: the ChatGPT listing (its own repo, `shipstatic/gpt`) and the
  Claude directory listing. **Nothing here is a connector**, and OpenAI
  calling its listing a "plugin" makes it no relative of this repo.
- **This repo is the plugin:** one package that Claude Code, Codex, Cursor
  and Gemini CLI install from this repo, and Grok Build and Grok Bot through
  the formats they read. A plugin is code we ship, so it never earns a channel
  door, and the URL it names is the plain `https://mcp.shipstatic.com`.

The shape is AgentMail's (`agentmail-to/agentmail-plugins`): one `.mcp.json`
with the hosted URL, shared skills, a thin native manifest per host.

## Layout

```
.mcp.json                          # the one server: the plain URL
.claude-plugin/plugin.json         # Claude Code (and Grok Build)
.claude-plugin/marketplace.json    # /plugin marketplace add shipstatic/plugin
.codex-plugin/plugin.json          # Codex
.agents/plugins/marketplace.json   # codex plugin marketplace add shipstatic/plugin
.cursor-plugin/plugin.json         # the Cursor Marketplace (and Grok Bot)
gemini-extension.json              # Gemini CLI: the same URL under its own key
skills/publish-online/SKILL.md     # the one skill: putting things online
scripts/validate.py                # the checks, for both workflows
scripts/validate_test.py           # each check, drilled against its defect
evals/                             # what the skill decides, run by hand
.claude/CLAUDE.md                  # this guide
```

The plugin folder is the repo root, so every tracked file ships to every
installer and is scanned as the plugin. That is the price of one repo serving
five hosts: Gemini CLI installs the root and finds `skills/` only there. So
this guide lives in `.claude/`, where a contributor's Claude Code still loads
it and no host reads it as the plugin's, and the evals and the validator's
test are text a host never runs.

The logo under assets is www's logo, byte for byte. This guide names it in
prose only: the Claude directory holds a plugin for review when a guide,
command or script writes an image's path in backticks or a code block, so
the manifests that need the logo are the only files that name its path.

## The skill does one job

`publish-online` deploys and does nothing else. It chooses the way by what the
session can do, never by the host's name: a shell with Node runs
`npx -y @shipstatic/ship@3 <folder> --json`, which reads files from disk;
otherwise the hosted `deployments_upload` takes the files inline. It reports
from what the deploy returned (a `claim` link and an `expires` time mean the
site has no account yet), never from whether the host is connected.

`@3` pins the CLI's major, as the GitHub Action's install line does, and the
plugin's own major is that number: the plugin is 3.x while its skill runs
`@shipstatic/ship@3`, and it moves to 4 only in the release whose skill runs
`@4`. Minor and patch are the plugin's own, so a ship release forces no plugin
release. `scripts/validate.py` holds the pin and the major equal.

The skill's text is owned here, and it is ShipStatic's one skill: the CLI
package ships none of its own. `npx skills add shipstatic/plugin` installs it
from this repo for any skills-aware tool. Two copies carry it byte for byte:
the one file served at www.shipstatic.com/SKILL.md, and the ChatGPT listing's
`skills/publish-online/SKILL.md` in `shipstatic/gpt`. A script outside this
repo writes both and a check holds them equal, so they are never edited by
hand. A change to the skill is released here first, then carried to the
copies.

ClawHub (OpenClaw, and Hermes's Skills Hub, which reads it) serves the skill as
`shipstatic`, a copy published by hand, because ClawHub has no trusted
publishing for skills. After a release that changes the skill, publish the
released bytes there, signed in to ShipStatic's ClawHub account, with the next
version:

```bash
npx -y clawhub@0.23.3 skill publish <folder holding the released SKILL.md> --slug shipstatic \
  --name ShipStatic --version <x.y.z> --source-repo shipstatic/plugin \
  --source-commit <released sha> --source-ref main --source-path skills/publish-online
```

A check outside this repo reads ClawHub's copy against this repo's `main`, so
a release that skipped this step shows red there.

## Which account a deploy lands in

Each way uses its own credential: the hosted upload uses the host's OAuth
grant, the CLI uses the key it is set up with (`ship config`), and neither
reaches the other. With neither, a deploy has no account and comes with a
claim link. Attribution follows the way: `via: mcp` for an upload, `via: cli`
for a folder.

**Cursor cannot sign in mid-session on this URL.** Its client starts a
sign-in after connect only for hosts it names, so in Cursor publishing works
with no account and account tools answer Unauthorized. The skill's section
on accounts sends the user to `my.shipstatic.com` for that case. It changes
when Cursor starts a sign-in after connect for this host.

## The checks

`scripts/validate.py`, run by `validate.yml` on both branches and by
`release.yml` on the tagged commit:

- every manifest is readable JSON;
- one name, `shipstatic`, everywhere, and one version across the four
  versioned manifests, written MAJOR.MINOR.PATCH (and, on a release, equal
  to the tag);
- exactly one server, the plain production URL, in `.mcp.json` and again
  under Gemini's `httpUrl`;
- both marketplace entries are this repo's root, and Codex's sign-in is
  `ON_USE`: sign-in at install would end publishing with no account;
- each manifest, and each marketplace entry, holds exactly the keys its fixed
  shape lists, each of its type: a string, a list of strings, an object (a
  key added or dropped is a design decision first, never a passing edit);
  both marketplaces are named `shipstatic`, and Codex's policy is exactly
  `AVAILABLE` and `ON_USE`;
- the Codex and Cursor manifests name exactly `./.mcp.json` and `./skills/`,
  and every manifest that names the logo names the same path, inside the
  repo;
- the Claude manifest's listing links (`supportUrl`, `privacyPolicyUrl`,
  `termsOfServiceUrl`) equal the Codex `interface` copies, which spell them
  `...URL`: the Claude directory reads its listing from that manifest;
- the repo tracks exactly the plugin's files, each a regular file (git mode
  `100644`: no link, no submodule): the text files listed in `validate.py`,
  and the logo at the path the manifests name. Hosts load more than
  manifests name (a root `GEMINI.md`, a root `plugin.json`, a `commands/`
  folder), and the file list is the one check that covers every way in. The
  script reads the logo's path from the manifests and never opens the image:
  git's index proves it is a tracked regular file;
- `skills/` holds exactly `publish-online`, named for its folder, and every
  mention of the CLI in it is exactly `@shipstatic/ship@N`, N the plugin's
  major;
- every commit on every remote branch and tag is ShipStatic's, with no
  attribution line: no `Co-Authored-By` or `Claude-Session` trailer and no
  link to an assistant's session. A commit made in GitHub's web interface passes
  with GitHub as its committer.

`scripts/validate_test.py`, which `validate.yml` runs next, drills those
checks: in a fresh copy of the package it plants one defect at a time (a
link, an executable file, a missing or an extra file, a directory at the
logo's path, a bad version, a wrong type, a key added or dropped) and
requires `validate.py` to fail naming it, after the untouched copy passes. A
new check comes with its case.

`validate.yml` also runs `claude plugin validate --strict --profile
directory` at an exact Claude Code version: it fails on anything the Claude
directory would refuse among the checks it runs, and on any warning. It
prints the directory's findings, so a hold shows in the log. The directory
runs more checks, so a green run is not its verdict.

`evals/` holds `claude plugin eval` cases, one per decision the skill makes,
each folder named for its decision. They run a model and cost money, so they
run by hand before any release that changes the skill, never in CI, and the
release's commit message records the scores. Every credential, password and
path in a case is made up. A decision the trace shows (which tool ran, in
what order, with what input) is graded by a tool or regex grader; a model
judges only wording. Run them from the repo root, with the results kept out
of the tree:

```bash
claude plugin eval . --trust-plugin --scaffold --ablation none --no-publish -j 4 \
  --allow-tools Write Bash \
  --output-dir "${TMPDIR:-/tmp}/plugin-evals" --report "${TMPDIR:-/tmp}/plugin-evals/report.html"
```

The run has a shell and Node and no internet: every command runs inside
Claude Code's sandbox, which confines writes to the run's workspace, hides
the home directory and grants no network, so `npx` cannot fetch the CLI
and no case can publish anything. That is the skill's own condition for
the upload (the shell cannot reach npm), and the agent then takes the
upload, which a mock under `evals/mocks/` answers. A narrower grant, one
command at a time, is refused: the sandbox denies a compound command when
any part of it is ungranted, which flips a run between the "built" and
"could not build" branches at random. The mocks hold results only. A saved
copy of the server's tool list is refused: it would be a second copy of the
MCP catalogue, and the cases test
the skill, not the tools.

The checks that compare this repo with another (the skill's tool names
against the MCP catalogue, the logo against the website's) live in a
check outside this repo, so a release here never goes red because another repo
moved.

**The `validate` job's name is the check `main`'s protection requires.**
Renaming it leaves `main` unprotected.

## Release

Tag-driven and branch-agnostic. **`main` moves only by a release**: the
Claude directory scans each commit on `main` as a version, and every host
installs `main`'s head, so a commit, a tag, a directory version and what
every host installs are one thing. A docs-only change waits on `development`
for the next version, or is itself a patch. Merge `development` into `main`,
let `validate` pass on that commit, then tag it:

```bash
git tag -a vX.Y.Z -m "X.Y.Z" && git push origin vX.Y.Z
```

`release.yml` refuses a tag that is not on `main` or whose commit has no
successful run of `validate.yml`, checks the tag against every manifest's
version, and creates the GitHub Release. Tag after `validate` has passed on
`main`; a release that ran too early is repaired with "Re-run failed jobs".
Released and listed are separate states: Cursor reviews every update by
hand, so a release reaches the Cursor Marketplace only once Cursor approves
that commit.

A release is done when the Claude directory has scanned it: check the
directory's scan of the release, since a scan can end with no result or hold
the version for a reviewer, and nothing else in this ritual would show it.

## Commit identity

Every commit is `ShipStatic <hello@shipstatic.com>`, unsigned, and the history
check in `validate.py` holds it.

## Gemini CLI facts worth keeping

- `--consent --skip-settings` is the non-interactive install.
- The manifest's `name` becomes the install directory and the handle for
  `gemini extensions config` and `uninstall`.
- Gemini finds `skills/` on its own, with no `contextFileName`.
- Individual Google login is retired for Gemini CLI, so the working auth is a
  Gemini API key, and the CLI caches its auth choice in
  `~/.gemini/settings.json` (`security.auth.selectedType`).
