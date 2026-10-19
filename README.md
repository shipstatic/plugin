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

## Use it

Ask in your own words, for example:

- "Build this project and publish it with ShipStatic."
- "Make a one-page site for my bakery and give me a link I can share."
- "Publish the dist folder with ShipStatic's built-in password protection."

The plugin has one skill, `publish-online`, and one MCP server, `https://mcp.shipstatic.com`.

- **A folder on disk** goes online through the ShipStatic CLI, with `npx -y @shipstatic/ship@3`. It needs Node.js 20.19 or newer, and nothing to install.
- **Files the agent writes** go online through the MCP server's `deployments_upload` tool.

## Accounts

You don't need an account to publish. A site published without one stays up for 3 days, and you get a claim link with it. Open the claim link and sign in to keep the site.

With a ShipStatic account you can keep every site, see them all and use your own domain:

- **The MCP server** asks you to sign in when you use an account tool, in hosts that support it. Cursor doesn't yet, so in Cursor you manage your sites at [my.shipstatic.com](https://my.shipstatic.com).
- **The CLI** publishes into your account once you run `npx -y @shipstatic/ship@3 config` and paste an API key from [my.shipstatic.com/api-key](https://my.shipstatic.com/api-key).

## Private sites

Ask for ShipStatic's built-in password protection. Visitors have to type the password before they see anything, on the site's link and on any custom domain pointing at it.

## Also available

| Surface | Reach it |
|---------|----------|
| **[MCP](https://mcp.shipstatic.com)** | Add `https://mcp.shipstatic.com` to any MCP client |
| **[CLI and SDK](https://github.com/shipstatic/ship)** | `npx @shipstatic/ship ./dist` |
| **[GitHub Action](https://github.com/shipstatic/action)** | `shipstatic/action@v3` |
| **[n8n](https://www.npmjs.com/package/n8n-nodes-shipstatic)** | Search "ShipStatic" in n8n's node panel |
| **[Agent Skill](https://www.shipstatic.com/SKILL.md)** | One file, for any skills-aware tool |

[Support](https://www.shipstatic.com/support) • [Privacy](https://www.shipstatic.com/privacy) • [Terms](https://www.shipstatic.com/terms)

## License

MIT
