# Ship Plugin

AI plugin for [ShipStatic](https://shipstatic.com) — deploy static websites, landing pages, and prototypes instantly from your AI assistant.

Distributed as a Gemini CLI extension. The underlying SKILL.md uses the open [Agent Skills](https://agentskills.io) standard, so the same instructional content powers any of the [35+ skills-aware tools](https://agentskills.io/clients) — Claude, Claude Code, Cursor, GitHub Copilot, VS Code, OpenAI Codex, Goose, and more.

## Setup

### Gemini CLI

```bash
gemini extensions install https://github.com/shipstatic/plugin
```

### Claude Code, Cursor, and other Agent Skills tools

Copy `skills/using-ship/SKILL.md` into the tool's skills directory. See [skills-aware tools](https://agentskills.io/clients) for per-tool instructions.

## Prerequisite

The plugin teaches your AI assistant the [Ship CLI](https://github.com/shipstatic/ship). Install it first:

```bash
npm install -g @shipstatic/ship
```

## Deploy — Free, No Account Needed

Ask your AI assistant to deploy a site. No API key, no sign-up, no configuration.

Your site is live instantly on `*.shipstatic.com`.

Deployments without an API key are public and expire in 3 days. The response includes a **claim URL** — always show it to the user so they can keep the site permanently.

Want a private site? Ask your AI assistant to set a password when deploying — visitors will be prompted to unlock before viewing, on the deployment URL and on any custom domains pointing at it.

## All Commands — Free API Key

For permanent deployments and full control over your sites and domains, get a free API key from [my.shipstatic.com/api-key](https://my.shipstatic.com/api-key).

```bash
ship config    # paste your API key when prompted
```

### Deployments

| Command | Description |
|---------|-------------|
| `ship ./dist` | Publish files and get a live URL instantly, optionally protected by a password |
| `ship deployments list` | List all deployments with their URLs, status, labels, and password protection state |
| `ship deployments get <deployment>` | Get deployment details including URL, status, file count, size, labels, and password protection state |
| `ship deployments set <deployment>` | Update the labels on a deployment for organization and filtering |
| `ship deployments remove <deployment>` | Permanently remove a deployment and all its files |

### Domains

| Command | Description |
|---------|-------------|
| `ship domains set <name> [deployment]` | Connect a custom domain to your site, switch deployments, or update labels |
| `ship domains list` | List all domains with their linked deployments and verification status |
| `ship domains get <name>` | Get domain details including linked deployment, verification status, and labels |
| `ship domains records <name>` | Get the DNS records you need to configure at your DNS provider |
| `ship domains dns <name>` | Look up which DNS provider hosts a domain (e.g. Cloudflare, Namecheap) |
| `ship domains share <name>` | Get a shareable link so someone else can see the required DNS records |
| `ship domains validate <name>` | Check if a domain name is valid and available before connecting it |
| `ship domains verify <name>` | Check if DNS is configured correctly after you set up the records |
| `ship domains remove <name>` | Permanently disconnect and remove a custom domain |

### Account

| Command | Description |
|---------|-------------|
| `ship whoami` | Get your account details including email, plan, and usage |
| `ship tokens create` | Create a deploy token (shown once) |
| `ship tokens list` | List all tokens |
| `ship tokens remove <token>` | Revoke a token |

## Also Available

| Integration | Install |
|-------------|---------|
| **[CLI & SDK](https://github.com/shipstatic/ship)** | `npm install -g @shipstatic/ship` |
| **[MCP Server](https://github.com/shipstatic/mcp)** | `npx @shipstatic/mcp` |
| **[VS Code Extension](https://marketplace.visualstudio.com/items?itemName=shipstatic.shipstatic)** | Search "ShipStatic" in the VS Code Marketplace |
| **[GitHub Action](https://github.com/shipstatic/action)** | `shipstatic/action@v1` |

## License

MIT
