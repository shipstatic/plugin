# ShipStatic for Gemini CLI

Deploy static websites, landing pages, and prototypes instantly from [ShipStatic](https://shipstatic.com), inside Gemini CLI. Free, no account needed.

## Gemini CLI

```bash
gemini extensions install https://github.com/shipstatic/plugin
```

The extension registers the ShipStatic MCP server ([`@shipstatic/mcp`](https://github.com/shipstatic/mcp)) inside Gemini CLI: all fifteen tools, running on your own machine, deploying folders straight from disk.

Ask Gemini to deploy a site. No API key, no sign-up, no configuration. Your site is live instantly on `*.shipstatic.com`.

Deployments without an API key are public and expire in 3 days. The response includes a **claim URL** so you can keep the site permanently.

Want a private site? Ask Gemini to set a password when deploying. Visitors will be prompted to unlock before viewing, on the deployment URL and on any custom domains pointing at it.

### API key (optional)

For permanent deployments, custom domains, and account tools, get a free API key from [my.shipstatic.com/api-key](https://my.shipstatic.com/api-key). Gemini asks for it when the extension installs and stores it in your system keychain. One credential, two names: the console mints it as an API key (`ship-...`), and the variable that carries it is the token (`SHIP_TOKEN`).

### Tools

| Tool | Description |
|------|-------------|
| `deployments_upload` | Deploy a folder and get a live URL instantly, optionally protected by a password |
| `deployments_list` | List all deployments with their URLs, status, labels, and password protection state |
| `deployments_get` | Get deployment details including URL, status, file count, size, and labels |
| `deployments_set` | Update the labels on a deployment for organization and filtering |
| `deployments_delete` | Permanently delete a deployment and all its files |
| `domains_set` | Connect a custom domain to your site, switch deployments, or update labels |
| `domains_list` | List all domains with their linked deployment and verification status |
| `domains_get` | Get domain details including linked deployment, verification status, and labels |
| `domains_records` | Get the DNS records you need to configure at your DNS provider |
| `domains_dns` | Look up which DNS provider hosts a domain (e.g. Cloudflare, Namecheap) |
| `domains_share` | Get a shareable link so someone else can see the required DNS records |
| `domains_validate` | Check if a domain name is valid and available before connecting it |
| `domains_verify` | Check if DNS is configured correctly after you set up the records |
| `domains_delete` | Permanently disconnect and delete a custom domain |
| `whoami` | Get your account details including email, plan, and usage |

## Agent Skills: Claude Code, Cursor, and 30+ tools

The repo also ships `skills/using-ship/SKILL.md`, which teaches the [ShipStatic CLI](https://github.com/shipstatic/ship) through the open [Agent Skills](https://agentskills.io) standard. Copy it into your tool's skills directory; see [skills-aware tools](https://agentskills.io/clients) for per-tool instructions. The skill needs the CLI available, and `npx -y @shipstatic/ship` needs no install at all.

## Also available

| Surface | Reach it |
|---------|----------|
| **[MCP](https://mcp.shipstatic.com)** | Drop `https://mcp.shipstatic.com` into any MCP client |
| **[CLI and SDK](https://github.com/shipstatic/ship)** | `npx @shipstatic/ship ./dist` |
| **[VS Code](https://marketplace.visualstudio.com/items?itemName=shipstatic.shipstatic)** | Search "ShipStatic" in the Marketplace |
| **[n8n](https://www.npmjs.com/package/n8n-nodes-shipstatic)** | Search "ShipStatic" in n8n's node panel |
| **[GitHub Action](https://github.com/shipstatic/action)** | `shipstatic/action@v2` |
| **[Agent Skill](https://www.shipstatic.com/SKILL.md)** | One file, for any skills-aware tool |

## License

MIT
