# Termux ↔ GitHub integration

## What was verified

The GitHub connector is authenticated as `Relentless73` and can read and write the selected repositories. The accessible repositories are:

- `Relentless73/profitnoter` — private, local-first notes workspace.
- `Relentless73/profitfinder-site` — public FlipProfit vehicle/equipment deal-screening site.
- `Relentless73/ollama` was not accessible under `Relentless73` during this check.

The Termux screenshot shows a local workspace containing `Local_mcp`, `OpenManus`, `mcp_config.json`, `storage`, `index.html`, `downloads`, `test_mcp.py`, and several Facebook-posting scripts. The actual Termux file contents were not available in the sandbox, so no script-content match was claimed.

## Three concrete correlations

1. **`index.html` → both GitHub web projects.** The screenshot contains `index.html`. Both repositories contain an HTML entry point and React/Vite source. This is the same kind of web-app project structure, not proof that the files are identical.
2. **`storage` → FlipProfit storage code and Profitnoter browser storage.** FlipProfit contains `server/storage.ts` and a storage proxy; Profitnoter contains browser persistence in `src/lib/noteStorage.ts`. Your Termux `storage` directory is therefore conceptually related to data persistence, but it was not copied because its contents were unavailable.
3. **`downloads` / `find_and_post.py` → existing export and delivery workflows.** FlipProfit has CSV export verification and a prepared downloadable product bundle. Your Termux names suggest a local download/post workflow, while GitHub contains a documented export/delivery workflow. No Facebook posting code was imported or connected because credentials and platform actions should remain outside a public repository.

## What was implemented

- `tools/termux_manifest.py` scans a Termux directory and writes a safe JSON inventory.
- It records only relative filenames, extensions, byte sizes, and modification times.
- It excludes hidden folders, MCP configuration, environment files, credentials, tokens, cookies, archives, and database/key files.
- Profitnoter now has an **Import Termux** button. It turns a generated manifest into a searchable local note.
- The imported note clearly states that only safe metadata was imported.

This is intentionally a metadata bridge, not a secret sync or Facebook auto-poster. It lets the GitHub project recognize and organize the Termux workspace without uploading private automation or account credentials.
