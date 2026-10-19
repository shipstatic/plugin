# ShipStatic plugin for coding agents

Deploy static websites, landing pages, and prototypes instantly from your coding agent. Free, no account needed.

Ask your agent to put what you made online. It publishes a build folder straight from disk, or a page it just wrote, and gives you a link you can share right away.

## Install

### Cursor

From the Cursor Marketplace:

```
/add-plugin shipstatic
```

### Claude Code

```
/plugin marketplace add shipstatic/plugin
/plugin install shipstatic@shipstatic
```

### Codex

```bash
codex plugin marketplace add shipstatic/plugin
codex plugin add shipstatic@shipstatic
```

### Gemini CLI

```bash
gemini extensions install https://github.com/shipstatic/plugin
```

Gemini CLI serves paid and API-key plans. Google moved free users to Antigravity CLI.

After installing, start a new chat (in Cursor, reload the window first) so your agent sees the plugin.

## Use it

Ask in your own words, for example:

- "Build this project and publish it with ShipStatic."
- "Make a one-page site for my bakery and give me a link I can share."
- "Publish the dist folder with ShipStatic's built-in password protection."

The plugin has one skill, `publish-online`, and one MCP server, `https://mcp.shipstatic.com`. Your agent picks how the files travel:

- **A folder on disk** goes through the ShipStatic CLI, with `npx -y @shipstatic/ship@3`. It needs Node.js 20.19 or newer, and nothing to install.
- **When the CLI can't run** (no Node.js, no network, or a host with no shell), a few small files go through the MCP server's `deployments_upload` tool instead.

## No account needed

Publishing needs no account, whichever way the files travel. A site published without one stays up for 3 days, and you get a claim link with it. Open the claim link and sign in to keep the site.

If you want sites to go straight into your account, each way has its own setup:

| | With no account (the default) | Straight into your account |
|---|---|---|
| **A folder, through the CLI** | Live for 3 days, with a claim link | Run `npx -y @shipstatic/ship@3 config` once, with an API key from [my.shipstatic.com/api-key](https://my.shipstatic.com/api-key) |
| **Files, through the MCP server** | Live for 3 days, with a claim link | Sign in when your agent first uses an account tool. Cursor doesn't offer this sign-in yet, so in Cursor use the claim link |

Signing in on one way doesn't set up the other. You can see and manage every site at [my.shipstatic.com](https://my.shipstatic.com).

## Private sites

Ask for ShipStatic's built-in password protection. Visitors have to type the password before they see anything, on the site's link and on any custom domain pointing at it.

## Also available

| Surface | Reach it |
|---------|----------|
| **[MCP](https://mcp.shipstatic.com)** | Add `https://mcp.shipstatic.com` to any MCP client |
| **[CLI and SDK](https://github.com/shipstatic/ship)** | `npx @shipstatic/ship ./dist` |
| **[GitHub Action](https://github.com/shipstatic/action)** | `shipstatic/action@v3` |
| **[n8n](https://www.npmjs.com/package/n8n-nodes-shipstatic)** | Search "ShipStatic" in n8n's node panel |

[Support](https://www.shipstatic.com/support) • [Privacy](https://www.shipstatic.com/privacy) • [Terms](https://www.shipstatic.com/terms)

## License

MIT
