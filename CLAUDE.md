# CLAUDE.md

Claude Code instructions for **`shipstatic/plugin`, ShipStatic's plugin for
coding agents**.

## What this repo is, and what it is not

ShipStatic reaches AI hosts in two ways (the monorepo's
`integrations/CLAUDE.md`, "Connectors and the plugin"):

- **Connectors** are dedicated submissions to a chat app's directory, each a
  URL of its own: the ChatGPT listing (its own repo, `shipstatic/gpt`) and the
  Claude directory listing. **Nothing here is a connector**, and OpenAI
  calling its listing a "plugin" makes it no relative of this repo.
- **This repo is the plugin:** one package that Claude Code, Codex, Cursor
  and Gemini CLI install from this repo, and Grok Build and Grok Bot through
  the formats they read. A plugin is code we ship, so it never earns a channel
  door, and the URL it names is the plain `https://mcp.shipstatic.com`.

The shape is AgentMail's (`agentmail-to/agentmail-plugins`): one `.mcp.json`
with the hosted URL, shared skills, a thin native manifest per host. The
design, its decisions and what was refused are the monorepo's
`plan-plugin.md`.

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
assets/logo.png                    # the mark, the same bytes as www's logo.png
scripts/validate.py                # the checks, for both workflows
```

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
from this repo for any skills-aware tool. Two places carry it byte for byte,
both written by the monorepo's `node scripts/skill.mjs` and held equal by the
super-repo's pre-commit hook whenever this pointer, www's or gpt's is staged:
`web/www/SKILL.md`, served as one file at www.shipstatic.com/SKILL.md, and the
ChatGPT listing's `integrations/gpt/skills/publish-online/SKILL.md`. A change
to the skill is released here first, then carried to the copies.

## Which account a deploy lands in

Each way uses its own credential: the hosted upload uses the host's OAuth
grant, the CLI uses the key it is set up with (`ship config`), and neither
reaches the other. With neither, a deploy has no account and comes with a
claim link. Attribution follows the way: `via: mcp` for an upload, `via: cli`
for a folder.

**Cursor cannot sign in mid-session on this URL.** Its client starts a
sign-in after connect only for hosts it names, so in Cursor publishing works
with no account and account tools answer Unauthorized. The skill's last
sentence sends the user to `my.shipstatic.com` for that case. The monorepo's
`plan-plugin.md` §6 has the measurement and what would change it.

## The checks

`scripts/validate.py`, run by `validate.yml` on both branches and by
`release.yml` on the tagged commit:

- every manifest is readable JSON, and every path it names exists inside
  the repo;
- one name, `shipstatic`, everywhere, and one version across the four
  versioned manifests (and, on a release, equal to the tag);
- exactly one server, the plain production URL, in `.mcp.json` and again
  under Gemini's `httpUrl`;
- both marketplace entries are this repo's root, and Codex's sign-in is
  `ON_USE`: sign-in at install would end publishing with no account;
- each manifest, and each marketplace entry, holds only the keys it holds
  today (the package's shape is fixed, so a new key is a decision recorded
  in `plan-plugin.md` first); both marketplaces are named `shipstatic`, and
  Codex's policy is exactly `AVAILABLE` and `ON_USE`;
- the Codex and Cursor manifests name exactly `./.mcp.json` and `./skills/`,
  every path is a string inside the repo, and a logo is a file;
- the repo tracks exactly the plugin's files, listed in `validate.py`: hosts
  load more than manifests name (a root `GEMINI.md`, a root `plugin.json`, a
  `commands/` folder), and the file list is the one check that covers every
  way in;
- `skills/` holds exactly `publish-online`, named for its folder, and every
  mention of the CLI in it is exactly `@shipstatic/ship@N`, N the plugin's
  major;
- every commit on every remote branch and tag is ShipStatic's, with no
  attribution line: no `Co-Authored-By` or `Claude-Session` trailer and no
  link to an assistant's session. A commit made in GitHub's web interface passes
  with GitHub as its committer.

`validate.yml` also runs `claude plugin validate` at an exact Claude Code
version. It allows one warning: Claude Code does not load a plugin's root
`CLAUDE.md`, and this file is the repo's guidance, not the plugin's.

The checks that compare this repo with another (the skill's tool names
against the MCP catalogue, the logo against the website's) live in the
monorepo's `scripts/check-canon.sh`, so a release here never goes red because
another repo moved.

**The `validate` job's name is the check `main`'s protection requires.**
Renaming it leaves `main` unprotected.

## Release

Tag-driven and branch-agnostic. Merge `development` into `main`, let
`validate` pass on that commit, then tag it:

```bash
git tag -a v3.1.0 -m "3.1.0" && git push origin v3.1.0
```

`release.yml` refuses a tag that is not on `main` or whose commit has no
successful run of `validate.yml`, checks the tag against every manifest's version,
and creates the GitHub Release. Tag after `validate` has passed on `main`;
a release that ran too early is repaired with "Re-run failed jobs". Released and listed are
separate states: Cursor reviews every update by hand, so a release reaches the
Cursor Marketplace only once Cursor approves that commit.

## History

The repo's history began again on 2026-10-19 as one commit authored by
ShipStatic: the earlier history named the wrong people. Every commit since is
`ShipStatic <hello@shipstatic.com>`, unsigned, and the history check holds it.

## Gemini CLI facts worth keeping

- `--consent --skip-settings` is the non-interactive install.
- The manifest's `name` becomes the install directory and the handle for
  `gemini extensions config` and `uninstall`.
- Gemini finds `skills/` on its own, with no `contextFileName`.
- Individual Google login is retired for Gemini CLI, so the working auth is a
  Gemini API key, and the CLI caches its auth choice in
  `~/.gemini/settings.json` (`security.auth.selectedType`).
