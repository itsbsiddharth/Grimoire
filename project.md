# Grimoire — Build Prompt

## 0. What this is

A personal, single-user, read-only revision website for a DSA problem archive
that already lives in a git repo as markdown + YAML. The site's only job is
to browse, filter, and revise that content well — no backend, no database,
no auth. The git repo is the database. Static generation only.

**Identity.** The site is called **Grimoire** — "Every solved problem. Every
insight. Every spell you've mastered." Frame roadmaps as tomes and solved
problems as mastered spells; let that metaphor show up in a couple of
deliberate, load-bearing places (the tagline, one signature progress
visual — see §8) rather than reskinning every button. This gets opened under
time pressure to revise; clarity and speed win over theme whenever the two
conflict.

## 1. Existing repo — read before building

- GitHub: `itsbsiddharth/Grimoire`. Local clone:
  `C:\Users\besid\OneDrive\Desktop\STABLE BAKKI\Grimoire`.
- Current top level: `problems/`, `roadmaps/`, `templates/`,
  `.gitattributes`, `README.md`, `scaffold.py`, `update_vault.py`.
- `scaffold.py` and `update_vault.py` already exist and are the current
  authoring workflow. Read them first. Extend and wrap them rather than
  replacing them outright — only diverge where they conflict with the
  content contract in §3, and note the change in the README from §4.
- Only one roadmap exists today: the TUF+ SDE Sheet ("Striver sheet").
  NeetCode 150 and Blind 75 will be added later as additional
  `roadmaps/*.yaml` files. Nothing in the site should hardcode which
  roadmaps exist or how many — adding one should mean dropping in a new
  YAML file and its problem folders, never touching site code.

## 2. Tech stack & deployment

- Next.js (App Router) + TypeScript, statically generated at build time by
  reading the repo's markdown/YAML directly.
- No runtime backend, no database, no server-side API routes beyond the
  static build itself.
- A build step compiles every `problem.md`'s frontmatter into one JSON
  index (fields in §3). Keep it small enough (low hundreds of KB even at a
  few hundred problems) to ship to the client whole, so search and
  filtering run entirely in the browser with zero network round-trips.
- Everything else — Tailwind vs. CSS modules, which syntax highlighter,
  which YAML/frontmatter parser — is your call; pick whatever keeps this a
  static, dependency-light Next.js app. The one hard constraint: nothing
  calls a runtime API while browsing. If a build-time index can answer it,
  that's the only place it should be answered from.
- Deploy to Vercel as its own project. Do not fold this into the bsid.dev
  codebase, which is intentionally a single-file, zero-build-step static
  site. Connect it via a subdomain (e.g. `grimoire.bsid.dev`) and add one
  plain nav link on bsid.dev pointing here.

*(Why the framework is pinned but nothing below it is: the integration
constraints — subdomain of an existing site, reusing its exact theme
system, static-only hosting on Vercel — already narrow the honest choice to
the React/Vercel-native family. Naming that up front saves the build from
wandering into a stack that fights those constraints later.)*

## 3. Data source & content contract

```
problems/
  <slug>/
    problem.md
    question-1.png          (optional, 0 or more images)
    explanation.html        (optional)
    solutions/
      1-brute-force.cpp     (optional, any number of files)
      2-better.cpp
      3-optimal.cpp
roadmaps/
  tuf-plus-sde-sheet.yaml
  neetcode-150.yaml
  blind-75.yaml
templates/
  (starter files scaffold.py copies from — keep in sync with the
  frontmatter fields below)
```

**`problem.md` frontmatter:**
- `title` (string)
- `topic` (string — primary category, drives grouping)
- `subtopics` (string array)
- `platforms` (string array — leetcode, codeforces, cses, tuf-plus,
  neetcode, etc.)
- `type` (`practice` | `oa` | `interview`)
- `company` (string array — populated only for oa/interview)
- `difficulty` (`easy` | `medium` | `hard`)
- `canonical_link` (string, optional — the LeetCode-equivalent URL if known)
- `aliases` (string array — alternate names, helps search)

Body is a single `## Crux` section — a one-liner insight, gist, or key
gotcha. Not a full write-up; the thought process lives in code comments.

**`solutions/` naming rule:** files are named `{n}-{label}.{ext}`. The
leading number sets tab order; the label (kebab-case, shown in sentence
case) sets the tab name. A problem with only `1-optimal.cpp` gets exactly
one tab — derive everything from what files exist, no manual per-problem
config.

**`explanation.html`:** optional, self-contained (no external requests).
Its mere presence should make a "Visualization" tab appear for that
problem — no other wiring needed.

**`roadmaps/*.yaml` — must hold the full sheet, not just solved
problems**, or there's no way to show what's left:

```yaml
name: TUF+ SDE Sheet
problems:
  - title: Kadane's Algorithm
    slug: kadanes-algorithm       # slug present = solved, links to problems/<slug>
  - title: Some Problem Not Done Yet
    slug: null                     # slug absent = unsolved, greyed out, not clickable
```

List position = revision order. Don't add a separate "order" field
anywhere else — list position is the single source of truth, and
duplicating it risks drift.

## 4. Vault tooling & documentation

- **`scaffold.py`** — given a slug/title (ideally with topic/difficulty/
  platform flags), creates `problems/<slug>/` with a `problem.md` stub
  (frontmatter placeholders per §3) and an empty `solutions/` folder.
  Refuses to overwrite an existing slug. Keep whatever it already does;
  extend, don't replace.
- **`update_vault.py`** — reconciles `roadmaps/*.yaml` against `problems/`
  (filling in a `slug` once a matching folder exists) and/or regenerates
  the build-time JSON index. Extend it to validate the content contract —
  fail loudly on a missing required frontmatter field, a `solutions/` file
  that breaks the `{n}-{label}.{ext}` naming rule, or a roadmap entry
  whose slug has no matching folder — so bad content can never silently
  reach the site.
- **New — `ingest.py`**, for the screenshot-driven workflow: point it at
  one or more screenshots of a solved problem (statement + accepted
  solution code). It calls a vision-capable LLM (Claude API) to propose
  `title`, `topic`, `subtopics`, `platforms`, `difficulty`, `type`,
  `company` (if visible), a one-line `crux`, and the solution code with a
  suggested `{n}-{label}` filename per approach shown. It never writes
  straight into `problems/` — it stages the proposed files first and only
  commits them (and fills in the matching roadmap slug) after an explicit
  `--apply` confirmation, since screenshot extraction will occasionally
  get something wrong and this is a personal archive worth keeping clean.
  Ship this after the site and the manual scaffold/update workflow are
  solid — see §7.
- **`README-vault.md`** (or fold into the existing `README.md`): document
  the content contract from §3, example commands for each script above,
  and the exact steps to add a brand-new roadmap (drop a
  `roadmaps/<name>.yaml` with the full sheet — nothing else changes).

## 5. Pages & UX

### A. Home / Dashboard
The landing page is a dashboard built for getting back into revision fast,
not a wall of every problem.
- Header: wordmark + tagline, and an overall mastery indicator (solved /
  total across every roadmap) rendered as the signature progress sigil
  (§8).
- One card per `roadmaps/*.yaml` — name, "N / M solved," its own progress
  sigil, click-through to that roadmap's view (§C). This is the primary
  way to pick a roadmap.
- A "recently added" strip — the last handful of problems solved across
  all roadmaps, each a small card with thumbnail + title, linking straight
  to its detail page. This is the natural place to resume revision, since
  what you want to re-run through is usually what you just solved.
- One clear link to "Browse all" (§B) for anyone who wants the full
  faceted list instead of a curated roadmap.
- Topic grouping deliberately isn't a dashboard concern — it's already one
  click away, inside the roadmap view (grouped by topic, per the sheet's
  own structure) and the browse-all filters (topic as a facet). Repeating
  it here would just dilute the "resume fast" purpose of the landing page.

### B. Browse all
- Full problem list with a Codeforces-style faceted filter panel:
  clickable tag chips for topic, difficulty, platform, type, and company.
  Multiple chips within one facet is OR; chips across different facets is
  AND.
- A free-text box matching `title`, `aliases`, and `crux` only — the
  question body is intentionally not indexed, since name-level search is
  sufficient for a revision tool.
- Each row shows title, tag chips, and a thumbnail of `question-1.png`
  when present, so a problem is recognizable while scanning, not just
  after opening it.

### C. Roadmap / sheet view
- A switcher to pick a sheet (TUF+ SDE, NeetCode 150, Blind 75, etc. —
  driven entirely by what's in `roadmaps/`).
- Renders the sheet's full list in original order, grouped by topic as the
  sheet itself groups them. Solved problems are live links with a
  checkmark and thumbnail; unsolved problems are greyed out, plain text,
  not clickable.
- A progress indicator at the top (e.g. "39 / 198 solved").

### D. Problem detail page — three zones, left to right
1. **Progress rail (collapsible).** The active roadmap's ordered list,
   current problem highlighted, solved items checkmarked, unsolved items
   dimmed. Clicking any item navigates instantly client-side. This is the
   persistent "where am I in the sheet" panel — visible without going back
   to a list page.
2. **Problem pane.** Breadcrumb (topic / subtopic), title, tag chips,
   screenshot(s) in a light-colored card (rounded corners, subtle border)
   regardless of the site's dark theme — screenshots come from white-UI
   platforms, and forcing them dark would distort them. Below that, the
   Crux text.
3. **Solutions pane.** A tab strip auto-generated from whatever's in that
   problem's `solutions/` folder, in numeric-prefix order, plus a
   conditional Visualization tab. Switching tabs is instant, in-page. Code
   renders read-only with syntax highlighting. The Visualization tab
   renders `explanation.html` inside a sandboxed `<iframe>` — each
   `explanation.html` is independently LLM-generated over time with
   inconsistent inline CSS/JS, and the sandbox boundary keeps that from
   ever leaking into the rest of the site.

## 6. MVP checklist
- Build-time JSON index generated from all `problem.md` frontmatter
- Dashboard home (roadmap cards, recently-added strip, overall progress
  sigil)
- Faceted tag-chip filter + name/alias/crux search on Browse all, fully
  client-side
- Roadmap switcher with full ordered list, solved/unsolved gap display,
  progress indicator
- Persistent collapsible progress rail on problem detail pages
- Auto-derived solution tabs from filenames (no manual per-problem config)
- Conditional sandboxed-iframe Visualization tab
- Thumbnail previews in all list views
- Extended `scaffold.py` / `update_vault.py` with content-contract
  validation, plus `README-vault.md`

## 7. Phase 2 — optional, don't block the MVP on these
- **Command palette (Cmd+K):** fuzzy-jump to any problem by typing its
  name. Mirror the interaction pattern of the Monkeytype-style palette
  already built for bsid.dev.
- **Revision mode:** a toggle that hides the solutions/visualization panes
  behind a "Reveal" action, so the problem is recalled before the answer
  is shown. Off by default.
- **`ingest.py` screenshot pipeline** (§4) — the highest-leverage addition
  long-term, but the riskiest to get right (vision extraction errors, LLM
  API cost/latency), so build it once the manual workflow and the site
  itself are stable.

## 8. Visual design direction
- Inherit bsid.dev's language: dark background, phosphor-green accent,
  JetBrains Mono for code, Inter for UI text. Reuse the existing
  three-theme system (Phosphor / Flame / Paper) rather than inventing a
  new palette.
- One deliberate signature flourish: render progress (overall,
  per-roadmap, per-topic) as a glowing sigil/rune-style arc instead of a
  flat bar. It's the natural home for the "spell mastered" metaphor
  because it's tied to real data, not decoration for its own sake. Use it
  on the dashboard, roadmap cards, and roadmap view header.
- Keep the grimoire voice to small, load-bearing touches — the tagline,
  the sigil, maybe solution tabs read as "01 · Brute force → 02 · Better →
  03 · Optimal" (a real progression, not just a label) — rather than
  reskinning every button and word on the site. This gets opened daily
  under time pressure; fun should never cost a click or a second of
  clarity.
- Every interaction (tab switch, filter, roadmap switch, sidebar nav)
  should feel instant — static generation + client-side filtering, no
  runtime API call anywhere a build-time index would do the job.
- On narrow viewports, the progress rail collapses into a drawer and the
  solution tabs become a horizontally scrollable strip.

## 9. Explicit non-goals
- No code execution or test-case judging of any kind.
- No authentication, no multi-user support — single-user, public
  visibility is fine.
- Read-only site. All authoring happens in the git repo (locally, or via
  the tooling in §4) — the site never writes back to it.
- No full-text search of the question statement body — title, aliases,
  tags, and crux are the intended and sufficient search surface.