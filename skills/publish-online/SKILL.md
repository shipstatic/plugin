---
name: publish-online
description: Publish a site, page, report, dashboard, slide deck, document, portfolio or small web app at a ShipStatic link anyone can open, with no account needed and optional built-in password protection. Use when the user asks to publish something, deploy or host a static site or a build folder, put it online, or get a link others can open. Not for HTML the user only wants to see, download or keep as a file.
---

# Publish online

The user's own instructions come first. Where they say something different
from this workflow, follow them.

Publish what the user wants online: a site, a page, a report, a dashboard, a
slide deck, a document, a portfolio or a small web app. Publish when the user
has asked for it to be online. If they want to see a draft first, show it and
publish when they say so.

**Publishing needs no account.** Don't ask the user to sign in, connect
anything, create an account or give a key before publishing. Most sites are
published with no account, and that is the normal way, not a fallback.

## Two separate questions

1. **How the files travel.** You choose: the ShipStatic command for a folder
   on disk, or the `deployments_upload` tool for files you send in the call
   ("Publish" below). Both ways work with no account, and both return the
   same fields.
2. **Where the site lands.** You don't choose this and you don't check it
   first. With nothing set up, the site has no account. If the user has set
   up an account for the way you used, it goes into that account. The result
   tells you which ("Tell the user" below).

The two ways have separate setups: connecting the ShipStatic MCP server to an
account does not set up the command, and a key saved for the command does not
connect the MCP server.

## Find what to publish

- **A built site:** a folder with `index.html` at its root, such as `dist/`,
  `build/` or `out/`. Publish that folder.
- **A project with a build step:** run its build, then publish the folder it
  writes.
- **Nothing yet:** make the files, with the start page at `index.html`.

## Make the files

- Make it as HTML, with CSS, JavaScript, images and fonts as needed. It runs in
  the browser. There is no server, so no backend code, database or server-side
  form handling.
- Put the start page at `index.html`, at the root of what you publish. Link
  pages and files to each other with relative paths.
- A report or a single page can be one `index.html` with its CSS and
  JavaScript inside it, unless the user wants separate files. Charts and
  tables can be drawn with inline SVG, HTML and CSS.
- Use only content the user gave you or that you can make yourself. Don't link
  to images or files at addresses you guessed.
- Don't publish passwords, keys, government ID numbers, health records or
  payment card numbers, even behind a password. Offer a version with those
  left out or replaced by made-up examples.

## Publish

Choose how the files travel:

- **A shell with Node.js 20.19 or newer:** run
  `npx -y @shipstatic/ship@3 <folder> --json`. The command reads the files
  from disk, so nothing passes through the conversation.
- **When the command can't run** (no shell, no Node.js, or the session can't
  reach the network) **and the `deployments_upload` tool is available:** call
  it with all the files of this version, if they are few and small enough to
  send. Send text files (HTML, CSS, JavaScript, JSON, SVG) as plain text, and
  binary files such as images and fonts with `encoding: "base64"`.
- **A large build the command can't send:** never read it into the
  conversation. Ask the user to let the command reach the network, or tell
  them what is missing: Node.js for the command, or the ShipStatic MCP server
  for the upload.

Then:

- Publish straight away. Before publishing, don't call `whoami` or any other
  ShipStatic tool, don't run `ship whoami` or `ship config`, don't add
  `--token`, and don't start a sign-in.
- Publish all the files of a version at once.
- Don't set an expiry (`ttl`) or a domain unless the user asks for one. Both
  need an account.
- If the user wants it private or behind a password, use ShipStatic's built-in
  password protection: `--password <password>` on the command, or `password`
  on the upload. It works with no account, and it is checked before any file
  is served. Don't build a password page or script into the site. Make up a
  new password that is hard to guess, unless the user chose one. Never ask for
  a password the user already uses somewhere else.
- If the command fails with `authentication_failed`, the key saved for the
  command is old or wrong. Publish with no account instead: run the same
  command with `--config /dev/null` added, and tell the user their saved key
  was refused and this site has a claim link.
- If the command fails otherwise, tell the user what its message says. Fix
  what you can, for example a file type that isn't allowed, or a project
  folder where its build folder was meant, and publish once more.

## Tell the user

Read the result. Both ways return the same fields. Never decide from whether
you are connected, or from which way you used.

- **The result has a `claim` link** (the usual case): the site has no account.
  Give the link (`url`), say it stays up for 3 days, and give the claim link:
  opening it and signing in keeps the site for good. For example:

  > Your site is live: https://example-site-abc1234.shipstatic.com
  > It stays up for 3 days. To keep it, open
  > https://my.shipstatic.com/claim/… and sign in.

- **The result has no `claim` link:** the site is already in the user's
  ShipStatic account and stays until they delete it. Tell them just that,
  with the link. It is the account the MCP server is connected to (for the
  upload), or the account the command is set up with (for the command); the
  result doesn't name it, so don't guess which.
- The password, if you set one. A password the user never sees locks them out.

Keep the reply short. The links matter more than a summary of the files.

## When the user wants changes

Something published doesn't change. To change it, publish again: the user gets
a new link, and the earlier one keeps working until it expires. Say which link
is the new one, and that the claim link of the version they want to keep is
the one to open.

## When to stop or decline

- If the request needs a server (an API, a database, sign-in for the people
  who open the link), say that ShipStatic publishes static files such as HTML,
  and offer a static version if one would do the job.
- If publishing is refused, tell the user what the message says. Fix what you
  can, for example a file type that isn't allowed or files that are too large,
  and publish once more.

## Accounts, only when the user asks

Bring up an account only when the user asks to see or manage what they have
published, to use their own domain, or to publish into their account.

- A site published with no account moves into the user's account through its
  claim link, whichever way it was sent.
- For the MCP server's account tools, the host asks the user to sign in when
  one is first used. If a ShipStatic account tool is refused and no sign-in
  starts, the user can see and manage their sites at https://my.shipstatic.com.
- For the command to publish straight into their account, the user runs
  `npx -y @shipstatic/ship@3 config` once, with an API key from
  https://my.shipstatic.com/api-key.
