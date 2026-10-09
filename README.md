# Termux Profitnoter Bridge

A privacy-first bridge for turning a Termux workspace inventory into a local Profitnoter note.

This public repository contains reusable code from Robert / Relentless73's Termux-to-GitHub integration. It is designed to help others organize local automation work without uploading scripts, credentials, cookies, tokens, MCP configuration, or private repository history.

## Included

- `tools/termux_manifest.py` — standard-library-only safe inventory scanner.
- `src/termuxManifest.ts` — browser-safe parser that turns a manifest into a Profitnoter note payload.
- `scripts/facebook_page_drafts.py` — standard-library-only Meta Graph API client for creating and listing unpublished Page posts.
- `docs/termux-github-integration.md` — verified relationship between the Termux workspace and the GitHub projects.
- `docs/facebook-page-drafts.md` — Meta endpoint, token, permission, and draft-only behavior documentation.

## Safety behavior

The scanner exports relative paths, file extensions, sizes, and modification times only. The browser parser accepts only the declared manifest format and creates a note from its safe metadata. The scanner excludes hidden files and directories, MCP configuration, environment files, credentials, tokens, cookies, archives, databases, and private-key files. It never reads file contents.

The Facebook client targets Pages only. It sends a Page access token through an HTTP authorization header, sets `published=false`, and has no publication command.

## License

MIT. See `LICENSE`.
