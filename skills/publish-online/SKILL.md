---
name: publish-online
description: Publish a site, page, report, dashboard, slide deck, document, portfolio or small web app at a ShipStatic link anyone can open, with optional built-in password protection. Use when the user asks to publish something, deploy a static site or a build folder, put it online, or get a link others can open. Not for HTML the user only wants to see, download or keep as a file.
---

# Publish online

The user's own instructions come first. Where they say something different
from this workflow, follow them.

Publish what the user wants online: a site, a page, a report, a dashboard, a
slide deck, a document, a portfolio or a small web app. Publish when the user
has asked for it to be online. If they want to see a draft first, show it and
publish when they say so. Don't ask the user to sign in or connect anything
first.

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

Choose the way by what this session can do:

- **A shell with Node.js 20.19 or newer:** run
  `npx -y @shipstatic/ship@3 <folder> --json`. The command reads the files
  from disk, so nothing passes through the conversation.
- **Otherwise, when the `deployments_upload` tool is available:** call it with
  all the files of this version. Send text files (HTML, CSS, JavaScript, JSON,
  SVG) as plain text, and binary files such as images and fonts with
  `encoding: "base64"`. Never read a large build into the conversation to
  upload it.
- **Neither:** tell the user what is missing: Node.js for the command, or the
  ShipStatic MCP server for the upload.

Then:

- Publish straight away. Don't call `whoami` or any other ShipStatic tool
  first, and don't start a sign-in to publish.
- Publish all the files of a version at once.
- Don't set an expiry (`ttl`) unless the user asks for one. An expiry needs a
  connected account.
- If the user wants it private or behind a password, use ShipStatic's built-in
  password protection: `--password <password>` on the command, or `password`
  on the upload. It is checked before any file is served. Don't build a
  password page or script into the site. Make up a new password that is hard
  to guess, unless the user chose one. Never ask for a password the user
  already uses somewhere else.
- If the command fails, tell the user what its message says. Fix what you can,
  for example a file type that isn't allowed, or a project folder where its
  build folder was meant, and publish once more.
- If the command can't reach the network because the session limits it, ask
  to run it with network access. When the files are few and small, the upload
  is the other way.

## Tell the user

Both ways return the same fields. Use what came back:

- The link (`url`).
- A `claim` link and an `expires` time mean the site was published without an
  account, and it stays up for 3 days. Show the claim link: opening it and
  signing in keeps the site in the user's ShipStatic account.
- No claim link means the site went into an account. For the command, that is
  the account the ShipStatic CLI is set up with.
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

## Accounts

Bring up an account only when the user asks to see or manage what they have
published, or to use their own domain.

- With the ShipStatic MCP server connected to an account, uploads go to that
  account, with no claim link and no 3-day limit.
- The command has its own setup. If the user wants folders to go straight into
  their account, they run `npx -y @shipstatic/ship@3 config` once.
- If a ShipStatic account tool is refused and no sign-in starts, the user can
  see and manage their sites at https://my.shipstatic.com.
