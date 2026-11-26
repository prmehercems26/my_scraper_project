# Books to Scrape — Publication Audit

**Reviewed:** 2026-11-26
**Scope:** This repository only. This is a publication-readiness review, not a guarantee that the project is safe.

## Checks performed

- Reviewed the tracked file list, working-tree status, `.gitignore`, `requirements.txt`, `README.md`, and project source.
- Scanned the five tracked files and all reachable Git history for common credential patterns. No credential-shaped values were found in the current files, and no non-redacted PostgreSQL URLs remain in the 25 rewritten commits; candidate values were not printed.
- Confirmed that `.env`, virtual environments, Python bytecode, and common test/linter caches are excluded.
- Confirmed that the GitHub repository is public. A separate logged-out browser check was not performed.
- Did not execute project code as part of this audit.

## Findings and actions

| Finding | Status and action |
| --- | --- |
| The project README did not cover all required topics or provide a short demonstration. | **Addressed here:** expanded the README with purpose, data collection and persistence, user interaction, setup, a demo walkthrough, learning reflection, limitations, and assistance disclosure. |
| No project audit record was present. | **Addressed here:** added this sanitized `AUDIT.md`. |
| The ignore rules did not cover common virtual-environment and test/linter cache paths. | **Addressed here:** added `venv/`, test/linter caches, coverage output, and Flask's local `instance/` directory to `.gitignore`. |
| A database connection URL containing a password was previously committed in the public Git history. | **History cleanup completed:** all reachable repository history was rewritten to remove credential-bearing PostgreSQL URLs, and the rewritten `main` branch was force-pushed. GitHub's `main` matches the rewritten commit; no other branches, tags, or pull requests were found. **Rotation:** the user reports changing the Supabase database password on 2026-11-26; this was not independently verified. Old clones, forks, caches, or backups may still retain the previous history. |

## Remaining limitations

- The app reads only the first catalog page; name search filters the current scrape, not the full catalog or saved database rows.
- Repeated runs append rows without deduplication, and the interface does not load previously saved rows.
- The demo insert policy grants the Supabase `anon` role insert access and is not suitable for production data.
- Table creation and permission repair depend on the configured database pooler.
- No screenshot is stored in this repository; the README includes a short reproducible walkthrough instead.
- No automated test suite is included. This review did not run tests or verify a live Supabase insert.

## Overall result

The Books project covers the identified submission topics, and the exposed URL has been removed from the repository's published history. The user reports that the Supabase database password has been rotated; the report was not independently verified. The project is ready for submission against the Books-only checklist reviewed here.
