# App Twin Sync Journal

This journal keeps the HTML twin (`app_twin/`) current with the real app on `main`.
Each entry records which `main` commits were reviewed, what changed visually, and
what was updated in the twin. **The newest entry's "synced to" SHA is the sync state.**

## How a sync run works (procedure for the agent)

Trigger: Clara says **"update the twin"**. Never run automatically.

1. `git fetch origin` (read-only; never checkout/commit/push `main`).
2. Read the last synced SHA from the newest entry below.
3. `git log <last-sha>..origin/main --oneline -- lib/screens lib/components lib/widgets lib/dialogs lib/utils/colors.dart lib/utils/theme_config.dart lib/l10n assets/images` — UI-relevant commits only.
4. Triage each commit's diff: **visual change** (colors/spacing/strings/icons/layout), **new UI** (needs a new twin page), or **no visual impact** (log + skip).
5. Implement visual changes in `build_twins.py` ONLY (never hand-edit generated HTML), rebuild, verify affected pages at 1440×900 and at <1280px, redeploy to Vercel (`vercel deploy --prod --yes --scope claramunros-projects` from `app_twin/`).
6. Append a journal entry (template below) and commit on the twin branch. Do not push without asking.
7. Figma recapture of affected frames is a separate, optional follow-up.

Entry template:

```
## YYYY-MM-DD — synced to origin/main@<sha>
Reviewed: <n> commits (<sha-range>)
- <commit sha> <subject> → what changed in the twin (pages touched)
- <commit sha> <subject> → no visual impact, skipped
Mock-data decisions: <anything invented/adjusted>
Deployed: https://apptwin-six.vercel.app
```

Rules: 1:1 with code (no invented visuals; only mock data is invented). All changes
stay on the `app-twin-2026-07-08` branch (or its successor) — `main` is never modified.

---

## 2026-07-11 — baseline, synced to origin/main@623dd6f1

The twin currently reflects `main` as of `623dd6f1` ("fix(windows): use
Windows-specific primary model download URL") — the commit the twin branch was
created from. 43 screens × light/dark (86 pages), interactive single-page
prototype (`app.html`), medium (<1280px) responsive breakpoint on all screens.

Deployed: https://apptwin-six.vercel.app
