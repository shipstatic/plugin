# ShipStatic plugin for coding agents

Deploy static websites, landing pages, and prototypes instantly from your coding agent. Free, no account needed.

## Try it in seconds, no account needed

Install the plugin in your coding agent:

### Cursor

From the Cursor Marketplace (the listing isn't live yet):

```
/add-plugin shipstatic
```

Until then, add `https://mcp.shipstatic.com` as an MCP server in Cursor's settings, or install just the skill with `npx skills add shipstatic/plugin`.

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

### Just the skill, in any skills-aware tool

```bash
npx skills add shipstatic/plugin
```

After installing, start a new chat (in Cursor, reload the window first) so your agent sees it.

### Then just ask

Ask in your own words, for example:

- "Build this project and publish it with ShipStatic."
- "Make a one-page site for my bakery and give me a link I can share."
- "Publish the dist folder with ShipStatic's built-in password protection."

You get back a link you can share right away, and a claim link. The site stays up for 3 days, and opening the claim link keeps it for good.

Want it private? Ask for ShipStatic's built-in password protection. Visitors have to type the password before they see anything, on the site's link and on any custom domain pointing at it.

The plugin has one skill, `publish-online`, and one MCP server, `https://mcp.shipstatic.com`. Your agent picks how the files travel:

- **A folder on disk** goes through the ShipStatic CLI, with `npx -y @shipstatic/ship@3`. It needs Node.js 20.19 or newer, and nothing to install.
- **When the CLI can't run** (no Node.js, no network, or a host with no shell), a few small files go through the MCP server's `deployments_upload` tool instead.

## Keep your sites with a free account

Everything above works with no account. A free account keeps your sites for good, lets you use your own domain, and shows you everything you've published in one place.

Each way your agent publishes has its own setup:

| | With no account (the default) | Straight into your account |
|---|---|---|
| **A folder, through the CLI** | Live for 3 days, with a claim link | Run `npx -y @shipstatic/ship@3 config` once, with an API key from [my.shipstatic.com/api-key](https://my.shipstatic.com/api-key) |
| **Files, through the MCP server** | Live for 3 days, with a claim link | Sign in when your agent first uses an account tool. Cursor doesn't offer this sign-in yet, so in Cursor use the claim link |

Signing in on one way doesn't set up the other. You can see and manage every site at [my.shipstatic.com](https://my.shipstatic.com).

## Also available

| Surface | Reach it |
|---------|----------|
| **[MCP](https://mcp.shipstatic.com)** | Drop `https://mcp.shipstatic.com` into any MCP client |
| **[CLI and SDK](https://github.com/shipstatic/ship)** | `npx @shipstatic/ship ./dist` |
| **[VS Code](https://marketplace.visualstudio.com/items?itemName=shipstatic.shipstatic)** | Search "ShipStatic" in the Marketplace |
| **[n8n](https://www.npmjs.com/package/n8n-nodes-shipstatic)** | Search "ShipStatic" in n8n's node panel |
| **[GitHub Action](https://github.com/shipstatic/action)** | `shipstatic/action@v3` |

[Support](https://www.shipstatic.com/support) • [Privacy](https://www.shipstatic.com/privacy) • [Terms](https://www.shipstatic.com/terms)

## License

MIT
