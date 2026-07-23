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
   **Depth rule (Clara, 2026-07-23): go past the default render.** For every touched
   component, enumerate its conditional visual STATES from the Dart (every branch that
   changes visuals: assigned/unassigned, empty/filled, open dropdown incl. its search
   field, hover, active, error, disabled) and either represent each state in the twin
   (page state or prototype interaction) or explicitly log it as not-shown. The
   "Select Topic" unassigned-chip miss is the cautionary example.
5. Implement visual changes in `build_twins.py` ONLY (never hand-edit generated HTML), rebuild, verify affected pages at 1440×900 and at <1280px.
6. Publish: copy `app_twin/*.html` + generator sources (`build_twins.py`, `glyphs.py`, `fonts.css`, `lucide/`, `JOURNAL.md`) into a clone of `https://github.com/claramunro/hedy_twin`, commit, push `main`. Vercel auto-deploys https://apptwin-six.vercel.app from that repo. (CLI `vercel deploy` is the fallback only.)
7. Append a journal entry (template below) and commit on the twin branch of hedy_mobile. Do not push hedy_mobile without asking.
8. Figma leg — consult `FIGMA_KEY.md` (screen ↔ twin URL ↔ Dart source ↔ Figma node IDs)
   to find which frames are stale, then pick per screen:
   a. **Small delta** (color, text, spacing, icon swap): patch the EXISTING frames
      in place via the Figma MCP `use_figma` (load the /figma-use skill first; target
      the frame subtree by its node ID from the key). No reimport; Clara's file needs
      to be open in the Figma desktop app.
   b. **Structural change or new screen**: reimport just that screen — Clara pastes
      the page URL into html.to.design → Import from URL, deletes the stale frame,
      and the key's node ID gets updated.
   Keep FIGMA_KEY.md current: add rows for new screens, refresh node IDs after imports.

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

## 2026-07-23 — Mobile 390 begins: Sessions Dashboard + Figma side-by-side layout

- Built the mobile (iPhone 390×844) Sessions Dashboard 1:1 from _buildMobileLayout /
  _buildSmallScreenTopBar @ dbb0f260c: 47px status inset, scrolling header (title +
  count + Filters pill + overflow ⋮ — no inline Merge/Select/Refresh on iOS), sort
  row, full-width cards, glass bottom nav (Start Session first item, 5 icon items).
- The main dashboard URL is now RESPONSIVE <768px (mobile layout embedded behind a
  media query, device-width viewport) — one URL covers wide/medium/mobile like the
  real app. Dedicated *-mobile-{light,dark}-390.html pages remain as Figma capture
  targets.
- Figma: Brand-page rows re-spaced to 2000px slots (mobile sits right of each
  desktop frame). Mobile dashboard captured + cropped to 390×844, placed, named
  "App Twin — Sessions Dashboard ({Theme} · Mobile 390)" (839:4 / 840:4).
- Remaining screens' mobile layouts: queued (one-screen-at-a-time from _buildMobile*).

## 2026-07-23 — FIRST REAL SYNC (partial): Sessions Dashboard → origin/main@dbb0f260c

origin/main moved 1,464 commits past baseline (≈380 UI-relevant) — too many for
commit-by-commit triage, so the strategy is **re-baseline per screen** (read each
screen's current Dart, update the twin to match). This entry covers the Sessions
Dashboard only:
- NEW Filters button (sliders-horizontal 300, first in right cluster) — session_filter/filter_button.dart
- Select button icon: listFilter300 → squareCheck300 — transcript_screen.dart:2196
- Import menu now 3 items: Import Audio File / Import Online Video / Create Session
  from Transcript (audio_file_outlined, play_circle_outline, text_snippet_outlined)
- Sort menu gains "Grouped by date" option
- NEW iCloud-synced corner badge on audio session cards (#5BC8FF→#0A8EF0 gradient
  circle, cloud_done 8px, 1.5px card border, top-right of icon) — icloud_synced_badge.dart
- Count badge: verified unchanged on desktop (drill revert was correct)
Mock-data decisions: all 4 audio sessions shown as iCloud-synced.
**All other screens remain at 623dd6f1 and are now known-stale** — queued for
per-screen re-baseline. FIGMA_KEY rows for the dashboard are stale in Figma until
re-imported.
Deployed: https://apptwin-six.vercel.app

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
