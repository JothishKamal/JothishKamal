# GitHub Profile v2 — Design Spec

**Date:** 2026-07-22
**Repo:** `JothishKamal/JothishKamal` (special profile repo; `README.md` renders on the GitHub profile)
**Owner:** Jothish Kamal V S R

## Goal

A GitHub profile that reads, in under 20 seconds, as *"a backend engineer who ships production systems"* — not a student badge wall. Aesthetic reference: Stripe Docs + Vercel + Anthropic. Minimal, technical, elegant, dark-first.

**Chosen direction:** **Systems Console** — the profile reads like a live terminal and a set of architecture pipelines. One bold signature (an animated terminal boot hero); everything else is disciplined spec-sheet.

## Constraints (the canvas)

GitHub sanitizes README HTML: no `<style>`, no `<script>`, no external CSS. Therefore:

- Every visual (hero, architecture diagrams, terminal, LeetCode card) is a **self-contained SVG** referenced as an `<img>`.
- Light/dark handled with `<picture>` + `prefers-color-scheme` (`-dark` / `-light` asset pairs).
- Animation lives **inside** the SVG via SMIL/CSS-in-SVG (GitHub-safe, no JS).
- README body text is plain markdown in GitHub's system font — we don't fight the platform there.

## Design tokens

### Color (dark)

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#0D1117` | canvas — matches GitHub dark so SVGs blend seamlessly |
| `--panel` | `#161B22` | terminal window fill |
| `--border` | `#30363D` | hairlines, window chrome |
| `--text` | `#E6EDF3` | primary text |
| `--muted` | `#8B949E` | captions, secondary |
| `--accent` | `#00ADD8` | **Go cyan** — the single signature color (prompts, active nodes) |
| `--signal` | `#3FB950` | used sparingly: success / streak / "live" states only |

### Color (light)

| Token | Hex |
|---|---|
| `--bg` | `#FFFFFF` |
| `--panel` | `#F6F8FA` |
| `--border` | `#D0D7DE` |
| `--text` | `#1F2328` |
| `--muted` | `#636C76` |
| `--accent` | `#0969DA` (GitHub link-blue for light legibility; cyan reads weak on white) |
| `--signal` | `#1A7F37` |

Rationale: one owned accent (Go cyan) instead of the default `#58A6FF / #7EE787 / #D2A8FF` trio that every AI-generated profile uses. Ties the palette to the subject's primary language.

### Typography

- **Hero:** `JetBrains Mono`, subsetted and embedded as base64 woff2 inside the SVG — guarantees identical rendering for every viewer.
- **Diagrams / cards:** `ui-monospace, "SF Mono", "Cascadia Code", "JetBrains Mono", monospace` stack (no embed needed; graceful fallback).
- **README prose:** GitHub system font (not controllable, not fought).

### Signature element

**Animated terminal boot hero.** Sequence (SMIL-timed):

```
$ whoami
Jothish Kamal — Backend Engineer
Building distributed systems, AI infrastructure, and developer tooling.

$ stack
Go · Python · Docker · Redis · Postgres

$ _   (blinking cursor)
```

This is the single memorable element. Everything below stays quiet.

## Content (verified against resume + live sources)

All figures below are **real**, fetched 2026-07-22:

- **LeetCode** (`JothishKamal`): 347 solved — 127 Easy / 162 Medium / 58 Hard; 239 active days; 116-day streak. Source: LeetCode GraphQL.
- **Citi** — Technology Summer Analyst (SDE Intern), Jun 2026 – Present. Run Comparison platform: Parquet ingestion → schema reconciliation → diff generation → hybrid caching → Streamlit. 8-worker parallel loader, 200K+ records, 6 modules, 25+ tests.
- **AI-Mond** — SDE Intern, Feb 2026 – Jun 2026. Async document pipeline: FastAPI → Redis → Celery → Vertex AI (Gemini) → MongoDB (Beanie). SSE streaming, rule engine (28 condition fns), RBAC/JWT.
- **Syncule** (`raisaaajose/event-tracker-v2`, Python/Docker) — email ingestion + interest filtering + calendar sync; Google OAuth, idempotent job queues, LLM pipeline. **Full card.**
- **DEVSOC'25** (`CodeChefVIT/devsoc-be-25`, Go, 1★) — "Official DevSOC'25 Hackathon Backend"; 1,200 concurrent users, 99.9% uptime, +35% API latency, JWT + OTP. **Full card.**
- **VITTY** (`GDGVIT/vitty-app`, Kotlin, 31★ / 9 forks, **10k+ downloads**) — shipped Android product. **Compact card**, downloads/stars as the credibility hook.
- **Flutter Glimpse** (`GDGVIT/flutter-glimpse`, Dart, 2★) — "Server-Driven UI with JSON + gRPC support". **Compact card.**

Contact: Portfolio · LinkedIn · GitHub (`JothishKamal`) · Email.

## README section order

1. **Hero** — animated terminal (signature).
2. **Now** — rendered from `now.yml` between markers (current focus / learning / reading).
3. **Engineering Philosophy** — 5 one-line principles.
4. **Experience** — Citi + AI-Mond, each as a console-style architecture SVG + 3 bullets max.
5. **Projects** — Syncule + DEVSOC'25 (full cards with architecture SVGs); VITTY + Flutter Glimpse (compact cards).
6. **Tech Stack** — categorized (Languages / Backend / Databases & Caching / Infra / AI), not an icon dump.
7. **DSA dashboard** — custom LeetCode SVG card (real numbers).
8. **Metrics / Stats** — generated panel + contribution graph.
9. **Contact** — Portfolio · LinkedIn · GitHub · Email.
10. **Hidden** — `TODO`/`whoami` easter eggs in HTML comments.

## Asset & file structure

```
README.md
assets/
  hero-dark.svg          hero-light.svg
  arch-citi-dark.svg     arch-citi-light.svg
  arch-aimond-dark.svg   arch-aimond-light.svg
  arch-syncule-dark.svg  arch-syncule-light.svg
  arch-devsoc-dark.svg   arch-devsoc-light.svg
  leetcode-dark.svg      leetcode-light.svg   (generated)
scripts/
  fetch_leetcode.py      (GraphQL → regenerate leetcode SVGs)
now.yml                  (current focus data)
.github/workflows/
  leetcode.yml   metrics.yml   snake.yml   now.yml
docs/superpowers/specs/2026-07-22-github-profile-v2-design.md
```

Architecture diagrams share one visual language: monospace boxes, hairline borders, cyan arrows, active nodes accented — the same console vocabulary as the hero. Cross-section consistency is what makes the profile feel like a product.

## Automation (all weekly cron)

| Workflow | Action | Secret needed |
|---|---|---|
| `leetcode.yml` | run `fetch_leetcode.py`, regenerate SVG card, commit only if numbers changed | none (uses `GITHUB_TOKEN`) |
| `metrics.yml` | `lowlighter/metrics` panel (languages, activity, habits) | **`METRICS_TOKEN`** (classic PAT, `repo` + `read:user`) |
| `snake.yml` | generate contribution snake to output branch | none (`GITHUB_TOKEN`) |
| `now.yml` | render `now.yml` into README between `<!-- NOW:START -->` / `<!-- NOW:END -->` markers | none |

Schedule: weekly (`cron: '0 0 * * 0'`, Sundays 00:00 UTC) + `workflow_dispatch` for manual runs.

## Error handling & day-one behavior

- **No broken images before setup.** All hero, architecture, and the initial LeetCode SVGs are committed static files that render with zero secrets. Automation only *refreshes* them.
- **LeetCode fetch failure never clobbers** the good SVG: `fetch_leetcode.py` exits non-zero and writes nothing on network/parse error; the last committed card stays.
- **Metrics/snake** images 404 only until the PAT is added and Actions enabled — documented with exact steps. They are enhancements, not load-bearing.
- Generated commits use a bot identity and `[skip ci]` to avoid workflow loops.

## Testing / verification

- `fetch_leetcode.py` dry-run locally (LeetCode GraphQL already confirmed reachable) → valid, well-formed SVG output.
- All SVGs validated as well-formed XML and visually spot-checked in a browser (light + dark).
- Workflow YAML linted; crons and permissions blocks correct.
- README rendered-preview check: `<picture>` swaps correctly, no raw HTML leaks, links resolve.

## Out of scope (YAGNI)

Spotify widget, visitor counter, "Hi 👋" banner, anime/GIFs, rainbow badge walls, hobbies/biography prose.
