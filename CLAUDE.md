# CLAUDE.md

Claude Code instructions for the **ShipStatic Gemini CLI extension**.

**`shipstatic/plugin`**, installed with `gemini extensions install`. Since
2.0.0 it is an **MCP host**: the manifest registers the local stdio server, so
Gemini gets all fifteen ShipStatic tools running on the user's own machine.
Before 2.0.0 it was a context file teaching the `ship` CLI.

There is no code here (three manifests, a README, and a vendored skill), which
is why the repo carries no `package.json`, no biome and no coverage. It follows
the estate's tooling standard in the two ways a manifest-only repo can: the
`validate.yml` fences below, and this file.

## Layout

```
gemini-extension.json          # THE manifest: Gemini reads this one
.claude-plugin/plugin.json     # the same product, for Claude Code's plugin dir
.cursor-plugin/plugin.json     # and for Cursor's
skills/using-ship/SKILL.md     # VENDORED from npm/ship, never edited here
.github/workflows/validate.yml # the fences
.github/workflows/release.yml  # tag == manifest version, then a GitHub Release
```

## Why stdio rather than the hosted URL

Gemini CLI is a terminal agent working on a folder that already exists on the
user's disk. The stdio server takes a filesystem PATH; the hosted door takes
file bytes inlined in the tool arguments, because a Worker has no filesystem.
For an agent standing in a build output, the path is the whole point. Node is
guaranteed present (Gemini CLI runs on it), so `npx` costs nothing, and the
extension depends on no OAuth behaviour we have not measured in this host.

## The three fences in `validate.yml`

1. **The SKILL drift check.** `skills/using-ship/SKILL.md` must be
   byte-identical to `npm/ship/SKILL.md` on ship's **`main`**. This has an
   ORDER consequence that is easy to get wrong and is the reason this section
   exists: **a SKILL edit lands in `npm/ship` and reaches ship's `main`
   BEFORE the copy here is synced.** Sync first and this repo's CI is red
   until ship releases, through no fault of its own.
2. **The MCP major pin.** `args` must carry `@shipstatic/mcp@1`. Majors pin
   majors, the GitHub Action's law: this manifest resolves the package at
   RUNTIME, so `@latest` would put whatever the registry serves that minute
   inside every installed copy.
3. **The `via` restatement.** `env.SHIP_VIA` must be `gmn`. A manifest can
   import nothing, so the copy is a pinned literal; a respelling would
   silently attribute every Gemini deploy to the generic `mcp` fallback,
   because both readers drop a label the vocabulary does not know.

Plus: the three manifests state one version, and `gemini-extension.json` is
well-formed JSON.

## The `SHIP_TOKEN` setting is the whole credential story

Gemini prompts for it at install, stores it in the system keychain
(`sensitive: true`), and injects it into the MCP server's process. **It
reaches nothing without an `mcpServers` block**, which is what the manifest
declared for its whole life before 2.0.0, so the setting was inert: Gemini
sanitizes the environment and passes only declared variables to declared
processes, and there was no process. Optional by design: without it, deploys
are public and expire in 3 days.

## `contextFileName` is deliberately absent

Gemini CLI appends an MCP server's own `instructions` to the system prompt, so
the server already teaches the agent what it needs. A context file beside it
would be a second voice, and the two would drift the moment one changed.
`skills/using-ship/SKILL.md` stays in the repo for the Agent Skills story
(Claude Code, Cursor, and 30+ skills-aware tools copy it), not for Gemini.

## Release

Tag-driven and branch-agnostic: `validate.yml` runs on both branches,
`release.yml` fires on `v*`, asserts the tag equals the manifest version, and
creates the GitHub Release. The version lives in all three manifests at once.

```bash
git tag -a v2.0.1 -m "…" && git push origin v2.0.1
```

## The sitting is DONE (2026-09-02), and what it proved

The chat-level walk ran against a live Gemini session (0.59.0-preview.0,
Gemini API key auth): the agent loop invoked `deployments_upload` from this
extension's MCP server, the deploy landed on production with **`via: "gmn"`**,
the reply surfaced both the live URL and the claim URL as the instructions
teach, and the site served. Run headlessly (`gemini --yolo -p …`), which
leaves two small residues unwalked, recorded rather than implied: the
interactive tool-approval UX (`--yolo` skips it) and the authed leg INSIDE
Gemini (`gemini extensions config shipstatic "API Key"` is an interactive
keychain prompt; the same stdio server's authed path is proven elsewhere).

Two host facts from the same day, worth more than they look: **Google retired
individual Google-login for Gemini CLI** (every build answers "migrate to the
Antigravity suite"), so the working auth is a Gemini API key, and the CLI
CACHES its auth choice in `~/.gemini/settings.json`
(`security.auth.selectedType`) — a dead cached `oauth-personal` makes even
`GEMINI_API_KEY` runs fail with the Code Assist error, which reads as a key
problem and is not.

## The identifier is `shipstatic` (decided 2026-09-02, at the walk)

`name` was `ship` until 3.0.0, deferred because it is the install identity in
a host nobody had sat with. The walk happened: a real
`gemini extensions install` of the repo, an uninstall, and a reinstall under
the renamed manifest, all clean — the manifest `name` wins over the repo
directory name, and it becomes the on-disk directory
(`~/.gemini/extensions/shipstatic`), the config handle
(`gemini extensions config shipstatic`) and the uninstall handle. So the
canon's identifier rule applies with nothing against it, and 3.0.0 renames all
three manifests in one move. A major, honestly: anyone who installed a 2.x
would re-install under the new name. Two walk facts worth keeping:
`--consent --skip-settings` is the non-interactive install (without them the
command waits on prompts), and Gemini auto-discovers `skills/` even with no
`contextFileName`, so the vendored skill surfaces beside the MCP server as an
Agent Skill, matched by its own trigger description.
