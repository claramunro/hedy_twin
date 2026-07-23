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
5. Implement visual changes in `build_twins.py` ONLY (never hand-edit generated HTML), rebuild, verify affected pages at 1440×900 and at <1280px.
6. Publish: copy `app_twin/*.html` + generator sources (`build_twins.py`, `glyphs.py`, `fonts.css`, `lucide/`, `JOURNAL.md`) into a clone of `https://github.com/claramunro/hedy_twin`, commit, push `main`. Vercel auto-deploys https://apptwin-six.vercel.app from that repo. (CLI `vercel deploy` is the fallback only.)
7. Append a journal entry (template below) and commit on the twin branch of hedy_mobile. Do not push hedy_mobile without asking.
8. Figma leg (manual, ~30s/screen): tell Clara which screens changed with their URLs; she runs the html.to.design plugin in Figma → Import from URL → pastes each changed page's URL. New frames land wherever she runs the plugin; she deletes/replaces the stale frames.

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

## 2026-07-23 — pipeline drill (simulated change, later reverted)

End-to-end test of the sync pipeline using local branch `twin-sync-sim` standing in
for origin/main. Reviewed: 1 commit (28b5a9cd "style: darken count badge background
in light mode").
- 28b5a9cd → visual: count badge light bg grey.shade200 (#EEEEEE) → grey.shade300
  (#E0E0E0). Implemented as `.count` change + dark override `.count{background:#424242}`
  (because #E0E0E0 already dark-maps to #3D3D3D for borders — selector override keeps
  the badge's dark color correct). Pages touched: all pages with count badges
  (dashboard, topics, highlights bars); verified light #E0E0E0 / dark #424242.
- Published via hedy_twin push de07467 → Vercel auto-deploy. REVERTED after
  verification because the sim commit is not on real main (1:1 rule).
Mock-data decisions: none.
Deployed: https://apptwin-six.vercel.app

## 2026-07-11 — baseline, synced to origin/main@623dd6f1

The twin currently reflects `main` as of `623dd6f1` ("fix(windows): use
Windows-specific primary model download URL") — the commit the twin branch was
created from. 43 screens × light/dark (86 pages), interactive single-page
prototype (`app.html`), medium (<1280px) responsive breakpoint on all screens.

Deployed: https://apptwin-six.vercel.app
