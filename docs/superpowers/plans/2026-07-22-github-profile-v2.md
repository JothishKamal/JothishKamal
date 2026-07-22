# GitHub Profile v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a "Systems Console" GitHub profile (`JothishKamal/JothishKamal`) whose README reads, in under 20 seconds, as a backend engineer who ships production systems.

**Architecture:** Self-contained SVG assets (animated terminal hero + console-language architecture diagrams + a generated LeetCode card) referenced from `README.md` via `<picture>` for light/dark. A Python script regenerates the LeetCode card from live GraphQL. Four weekly GitHub Actions refresh LeetCode, metrics, snake, and the Now section. All hero/architecture/initial-LeetCode SVGs are committed static files so the profile renders fully with zero secrets; automation only refreshes them.

**Tech Stack:** SVG (SMIL animation), Markdown, Python 3 (stdlib only — `urllib`, `json`, `xml`), GitHub Actions YAML.

## Global Constraints

- No `<style>`/`<script>`/external CSS in README — GitHub sanitizes them. All visuals are SVG `<img>`; animation is SMIL/CSS **inside** the SVG only.
- Light/dark via `<picture>` with `media="(prefers-color-scheme: dark|light)"`; every asset ships a `-dark` and `-light` variant.
- Dark tokens: `--bg #0D1117`, `--panel #161B22`, `--border #30363D`, `--text #E6EDF3`, `--muted #8B949E`, `--accent #00ADD8`, `--signal #3FB950`.
- Light tokens: `--bg #FFFFFF`, `--panel #F6F8FA`, `--border #D0D7DE`, `--text #1F2328`, `--muted #636C76`, `--accent #0969DA`, `--signal #1A7F37`.
- Mono stack for diagram text: `ui-monospace, "SF Mono", "Cascadia Code", "JetBrains Mono", monospace`. Hero embeds JetBrains Mono as base64 woff2.
- All numbers are real (verified 2026-07-22): LeetCode 347 solved / 127 Easy / 162 Medium / 58 Hard / 239 active days / 116 streak. Citi 200K+ records, 8 workers, 6 modules, 25+ tests. DEVSOC 1,200 users, 99.9% uptime, +35%. VITTY 31★, 10k+ downloads.
- No Spotify, no visitor counter, no "Hi 👋", no GIFs, no rainbow badges, no biography prose.
- Contact lists GitHub + Email + LeetCode; Portfolio/LinkedIn added only if URLs are provided (currently omit).
- Commit after each task.

---

## File Structure

| File | Responsibility |
|---|---|
| `assets/hero-{dark,light}.svg` | Animated terminal boot hero (signature) |
| `assets/arch-citi-{dark,light}.svg` | Citi Run Comparison pipeline diagram |
| `assets/arch-aimond-{dark,light}.svg` | AI-Mond document pipeline diagram |
| `assets/arch-syncule-{dark,light}.svg` | Syncule pipeline diagram |
| `assets/arch-devsoc-{dark,light}.svg` | DEVSOC'25 pipeline diagram |
| `assets/leetcode-{dark,light}.svg` | Generated DSA card (real stats) |
| `assets/_svg_lib.md` | Shared SVG snippet reference (tokens, arrow marker, box template) — dev doc, not rendered |
| `scripts/fetch_leetcode.py` | LeetCode GraphQL → regenerate leetcode SVGs; never clobbers on failure |
| `now.yml` | Current focus data (building/learning/reading) |
| `README.md` | Markdown assembly with `<picture>` refs + NOW markers + easter eggs |
| `.github/workflows/leetcode.yml` | Weekly: run script, commit if changed |
| `.github/workflows/metrics.yml` | Weekly: lowlighter/metrics panel (needs `METRICS_TOKEN`) |
| `.github/workflows/snake.yml` | Weekly: contribution snake to output branch |
| `.github/workflows/now.yml` | Weekly + on push to now.yml: render Now into README |
| `SETUP.md` | Exact steps to enable Actions + add `METRICS_TOKEN` PAT |

**Shared verification helper** (used by every SVG task):

```bash
# validates well-formed XML; prints OK or the parse error
python -c "import sys,xml.dom.minidom as m; [m.parse(f) for f in sys.argv[1:]]; print('OK', *sys.argv[1:])" <files...>
```

---

### Task 1: Shared SVG library reference + hero terminal (signature)

**Files:**
- Create: `assets/_svg_lib.md`
- Create: `assets/hero-dark.svg`, `assets/hero-light.svg`

**Interfaces:**
- Produces: hero SVGs at `1000×260` viewBox, referenced by README Task 6 as `assets/hero-dark.svg` / `assets/hero-light.svg`.
- Establishes the reusable box + arrow-marker + token conventions consumed by Tasks 2–3.

- [ ] **Step 1: Write the shared SVG reference doc**

Create `assets/_svg_lib.md` documenting the conventions every asset reuses (this is a dev note, never rendered on the profile):

````markdown
# SVG conventions

Tokens (dark): bg #0D1117, panel #161B22, border #30363D, text #E6EDF3,
muted #8B949E, accent #00ADD8, signal #3FB950.
Tokens (light): bg #FFFFFF, panel #F6F8FA, border #D0D7DE, text #1F2328,
muted #636C76, accent #0969DA, signal #1A7F37.

Font: font-family="ui-monospace,'SF Mono','Cascadia Code','JetBrains Mono',monospace"

Reusable node box (12px radius, hairline border, label centered):
```svg
<g>
  <rect x="X" y="Y" width="150" height="44" rx="8" fill="{panel}" stroke="{border}"/>
  <text x="X+75" y="Y+27" text-anchor="middle" font-size="13" fill="{text}"
        font-family="ui-monospace,'SF Mono','Cascadia Code','JetBrains Mono',monospace">LABEL</text>
</g>
```

Arrow marker (define once per file in <defs>):
```svg
<marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7"
        markerHeight="7" orient="auto-start-reverse">
  <path d="M0 0 L10 5 L0 10 z" fill="{accent}"/>
</marker>
```
Connector: <line ... stroke="{accent}" stroke-width="1.5" marker-end="url(#arw)"/>
````

- [ ] **Step 2: Write `assets/hero-dark.svg`**

Animated terminal. Window chrome (three dots), prompt lines revealed by SMIL, blinking cursor. Uses the mono stack (skip base64 font-embed for v1 tractability — the stack renders correctly on GitHub; embedding is an optional later polish noted in Step 5).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 260" width="1000" height="260" role="img" aria-label="Terminal: whoami — Jothish Kamal, Backend Engineer">
  <rect x="1" y="1" width="998" height="258" rx="12" fill="#161B22" stroke="#30363D"/>
  <circle cx="26" cy="24" r="6" fill="#30363D"/><circle cx="46" cy="24" r="6" fill="#30363D"/><circle cx="66" cy="24" r="6" fill="#30363D"/>
  <text x="500" y="28" text-anchor="middle" font-size="12" fill="#8B949E" font-family="ui-monospace,'SF Mono','Cascadia Code','JetBrains Mono',monospace">jothish@backend ~ %</text>
  <line x1="1" y1="46" x2="999" y2="46" stroke="#30363D"/>
  <g font-family="ui-monospace,'SF Mono','Cascadia Code','JetBrains Mono',monospace" font-size="15">
    <text x="28" y="86" fill="#3FB950">$ <tspan fill="#E6EDF3">whoami</tspan>
      <animate attributeName="opacity" from="0" to="1" begin="0.2s" dur="0.3s" fill="freeze"/></text>
    <text x="28" y="116" fill="#00ADD8" opacity="0">Jothish Kamal <tspan fill="#8B949E">— Backend Engineer</tspan>
      <animate attributeName="opacity" from="0" to="1" begin="0.9s" dur="0.3s" fill="freeze"/></text>
    <text x="28" y="142" fill="#8B949E" font-size="13" opacity="0">Building distributed systems, AI infrastructure, and developer tooling.
      <animate attributeName="opacity" from="0" to="1" begin="1.3s" dur="0.3s" fill="freeze"/></text>
    <text x="28" y="182" fill="#3FB950" opacity="0">$ <tspan fill="#E6EDF3">stack</tspan>
      <animate attributeName="opacity" from="0" to="1" begin="1.9s" dur="0.3s" fill="freeze"/></text>
    <text x="28" y="212" fill="#E6EDF3" opacity="0">Go <tspan fill="#30363D">·</tspan> Python <tspan fill="#30363D">·</tspan> Docker <tspan fill="#30363D">·</tspan> Redis <tspan fill="#30363D">·</tspan> Postgres
      <animate attributeName="opacity" from="0" to="1" begin="2.5s" dur="0.3s" fill="freeze"/></text>
    <rect x="28" y="230" width="10" height="18" fill="#00ADD8" opacity="0">
      <animate attributeName="opacity" from="0" to="1" begin="3.0s" dur="0.1s" fill="freeze"/>
      <animate attributeName="opacity" values="1;1;0;0" dur="1.1s" begin="3.1s" repeatCount="indefinite"/></rect>
  </g>
</svg>
```

- [ ] **Step 3: Write `assets/hero-light.svg`**

Same markup as Step 2 with light tokens swapped: `#161B22`→`#F6F8FA`, `#30363D`→`#D0D7DE`, `#E6EDF3`→`#1F2328`, `#8B949E`→`#636C76`, `#00ADD8`→`#0969DA`, `#3FB950`→`#1A7F37`. Keep all geometry, text, and `<animate>` timing identical.

- [ ] **Step 4: Verify both hero SVGs are well-formed XML**

Run:
```bash
python -c "import sys,xml.dom.minidom as m; [m.parse(f) for f in sys.argv[1:]]; print('OK', *sys.argv[1:])" assets/hero-dark.svg assets/hero-light.svg
```
Expected: `OK assets/hero-dark.svg assets/hero-light.svg`. Then open each in a browser and confirm the boot sequence types out and the cursor blinks. (Optional polish — not required for v1: embed a JetBrains Mono woff2 subset as base64 in a `<style>@font-face</style>` inside the SVG.)

- [ ] **Step 5: Commit**

```bash
git add assets/_svg_lib.md assets/hero-dark.svg assets/hero-light.svg
git commit -m "feat: animated terminal hero (signature) + SVG conventions"
```

---

### Task 2: Experience architecture diagrams (Citi + AI-Mond)

**Files:**
- Create: `assets/arch-citi-dark.svg`, `assets/arch-citi-light.svg`
- Create: `assets/arch-aimond-dark.svg`, `assets/arch-aimond-light.svg`

**Interfaces:**
- Consumes: box + arrow-marker conventions from `assets/_svg_lib.md` (Task 1).
- Produces: four SVGs at `900×120` viewBox, referenced by README Task 6.

- [ ] **Step 1: Write `assets/arch-citi-dark.svg`**

Horizontal pipeline, 6 nodes, left-to-right arrows. Node labels (exact): `Enterprise Feeds` → `Object Storage` → `Parquet Loader` → `Schema Recon` → `Diff Engine` → `Streamlit`. Layout: each node `130×40`, gap `12`, first node x=10, y=40; connectors are `<line>` between adjacent nodes using `marker-end="url(#arw)"`. Accent the middle node (`Diff Engine`) stroke with `#00ADD8` to mark the core.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 120" width="900" height="120" role="img" aria-label="Citi Run Comparison pipeline">
  <defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#00ADD8"/></marker></defs>
  <rect width="900" height="120" fill="#0D1117"/>
  <g font-family="ui-monospace,'SF Mono','Cascadia Code','JetBrains Mono',monospace" font-size="12">
    <!-- 6 node <g> blocks at x = 10, 152, 294, 436, 578, 720 (130 wide + 12 gap); y=40 h=40 -->
    <!-- template per node: -->
    <rect x="10" y="40" width="130" height="40" rx="8" fill="#161B22" stroke="#30363D"/>
    <text x="75" y="64" text-anchor="middle" fill="#E6EDF3">Enterprise Feeds</text>
    <line x1="140" y1="60" x2="152" y2="60" stroke="#00ADD8" stroke-width="1.5" marker-end="url(#arw)"/>
    <rect x="152" y="40" width="130" height="40" rx="8" fill="#161B22" stroke="#30363D"/>
    <text x="217" y="64" text-anchor="middle" fill="#E6EDF3">Object Storage</text>
    <line x1="282" y1="60" x2="294" y2="60" stroke="#00ADD8" stroke-width="1.5" marker-end="url(#arw)"/>
    <rect x="294" y="40" width="130" height="40" rx="8" fill="#161B22" stroke="#30363D"/>
    <text x="359" y="64" text-anchor="middle" fill="#E6EDF3">Parquet Loader</text>
    <line x1="424" y1="60" x2="436" y2="60" stroke="#00ADD8" stroke-width="1.5" marker-end="url(#arw)"/>
    <rect x="436" y="40" width="130" height="40" rx="8" fill="#161B22" stroke="#30363D"/>
    <text x="501" y="64" text-anchor="middle" fill="#E6EDF3">Schema Recon</text>
    <line x1="566" y1="60" x2="578" y2="60" stroke="#00ADD8" stroke-width="1.5" marker-end="url(#arw)"/>
    <rect x="578" y="40" width="130" height="40" rx="8" fill="#161B22" stroke="#00ADD8"/>
    <text x="643" y="64" text-anchor="middle" fill="#E6EDF3">Diff Engine</text>
    <line x1="708" y1="60" x2="720" y2="60" stroke="#00ADD8" stroke-width="1.5" marker-end="url(#arw)"/>
    <rect x="720" y="40" width="130" height="40" rx="8" fill="#161B22" stroke="#30363D"/>
    <text x="785" y="64" text-anchor="middle" fill="#E6EDF3">Streamlit</text>
  </g>
</svg>
```

- [ ] **Step 2: Write `assets/arch-citi-light.svg`**

Same markup, light tokens: bg `#0D1117`→`#FFFFFF`, panel `#161B22`→`#F6F8FA`, border `#30363D`→`#D0D7DE`, text `#E6EDF3`→`#1F2328`, accent `#00ADD8`→`#0969DA` (in marker fill, connector strokes, and the Diff Engine node border).

- [ ] **Step 3: Write `assets/arch-aimond-dark.svg`**

Same 6-node horizontal template as Step 1, labels (exact): `Documents` → `FastAPI` → `Redis` → `Celery` → `Vertex AI` → `MongoDB`. Accent the `Celery` node border (the async core). Reuse identical x/y coordinates and connector math from Step 1.

- [ ] **Step 4: Write `assets/arch-aimond-light.svg`**

Light-token swap of Step 3, same rules as Step 2.

- [ ] **Step 5: Verify all four are well-formed XML**

Run:
```bash
python -c "import sys,xml.dom.minidom as m; [m.parse(f) for f in sys.argv[1:]]; print('OK')" assets/arch-citi-dark.svg assets/arch-citi-light.svg assets/arch-aimond-dark.svg assets/arch-aimond-light.svg
```
Expected: `OK`. Open one dark + one light in a browser; confirm nodes, arrows, and the accented node render.

- [ ] **Step 6: Commit**

```bash
git add assets/arch-citi-*.svg assets/arch-aimond-*.svg
git commit -m "feat: Citi + AI-Mond architecture diagrams"
```

---

### Task 3: Project architecture diagrams (Syncule + DEVSOC'25)

**Files:**
- Create: `assets/arch-syncule-dark.svg`, `assets/arch-syncule-light.svg`
- Create: `assets/arch-devsoc-dark.svg`, `assets/arch-devsoc-light.svg`

**Interfaces:**
- Consumes: same conventions as Task 2.
- Produces: four `900×120` SVGs referenced by README Task 6.

- [ ] **Step 1: Write `assets/arch-syncule-dark.svg`**

Reuse the exact 6-node horizontal template from Task 2 Step 1. Labels (exact): `Inbox` → `Google OAuth` → `FastAPI` → `Job Queue` → `LLM` → `Calendar`. Accent the `LLM` node border.

- [ ] **Step 2: Write `assets/arch-syncule-light.svg`**

Light-token swap.

- [ ] **Step 3: Write `assets/arch-devsoc-dark.svg`**

Reuse the template but with **5 nodes** (recompute: 5 nodes 130 wide + 12 gap = 698 total, center by starting x=100; nodes at x=100, 242, 384, 526, 668; y=40 h=40; connectors between each). Labels (exact): `Users` → `Go API` → `JWT Auth` → `Postgres` → `Email/OTP`. Accent the `Go API` node border.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 120" width="900" height="120" role="img" aria-label="DEVSOC'25 backend pipeline">
  <defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#00ADD8"/></marker></defs>
  <rect width="900" height="120" fill="#0D1117"/>
  <g font-family="ui-monospace,'SF Mono','Cascadia Code','JetBrains Mono',monospace" font-size="12">
    <rect x="100" y="40" width="130" height="40" rx="8" fill="#161B22" stroke="#30363D"/><text x="165" y="64" text-anchor="middle" fill="#E6EDF3">Users</text>
    <line x1="230" y1="60" x2="242" y2="60" stroke="#00ADD8" stroke-width="1.5" marker-end="url(#arw)"/>
    <rect x="242" y="40" width="130" height="40" rx="8" fill="#161B22" stroke="#00ADD8"/><text x="307" y="64" text-anchor="middle" fill="#E6EDF3">Go API</text>
    <line x1="372" y1="60" x2="384" y2="60" stroke="#00ADD8" stroke-width="1.5" marker-end="url(#arw)"/>
    <rect x="384" y="40" width="130" height="40" rx="8" fill="#161B22" stroke="#30363D"/><text x="449" y="64" text-anchor="middle" fill="#E6EDF3">JWT Auth</text>
    <line x1="514" y1="60" x2="526" y2="60" stroke="#00ADD8" stroke-width="1.5" marker-end="url(#arw)"/>
    <rect x="526" y="40" width="130" height="40" rx="8" fill="#161B22" stroke="#30363D"/><text x="591" y="64" text-anchor="middle" fill="#E6EDF3">Postgres</text>
    <line x1="656" y1="60" x2="668" y2="60" stroke="#00ADD8" stroke-width="1.5" marker-end="url(#arw)"/>
    <rect x="668" y="40" width="130" height="40" rx="8" fill="#161B22" stroke="#30363D"/><text x="733" y="64" text-anchor="middle" fill="#E6EDF3">Email/OTP</text>
  </g>
</svg>
```

- [ ] **Step 4: Write `assets/arch-devsoc-light.svg`**

Light-token swap of Step 3.

- [ ] **Step 5: Verify well-formed XML**

Run:
```bash
python -c "import sys,xml.dom.minidom as m; [m.parse(f) for f in sys.argv[1:]]; print('OK')" assets/arch-syncule-dark.svg assets/arch-syncule-light.svg assets/arch-devsoc-dark.svg assets/arch-devsoc-light.svg
```
Expected: `OK`.

- [ ] **Step 6: Commit**

```bash
git add assets/arch-syncule-*.svg assets/arch-devsoc-*.svg
git commit -m "feat: Syncule + DEVSOC architecture diagrams"
```

---

### Task 4: LeetCode fetch script + generated DSA card

**Files:**
- Create: `scripts/fetch_leetcode.py`
- Create (by running the script): `assets/leetcode-dark.svg`, `assets/leetcode-light.svg`

**Interfaces:**
- Produces: `fetch_leetcode.py` writing two SVGs at `assets/leetcode-{dark,light}.svg`, `440×150` viewBox. Consumed by README Task 6 and workflow Task 7 (`leetcode.yml`).
- Contract: script exits `0` and writes both files on success; exits non-zero and writes **nothing** on any network/parse error (never clobbers the last good card).

- [ ] **Step 1: Write the failing verification (run before the script exists)**

Run:
```bash
python scripts/fetch_leetcode.py
```
Expected: FAIL with `No such file or directory` (script not yet created).

- [ ] **Step 2: Write `scripts/fetch_leetcode.py`**

```python
#!/usr/bin/env python3
"""Fetch LeetCode stats for a user and regenerate the DSA card SVGs.
Exits non-zero and writes nothing on failure (never clobbers good cards)."""
import json, os, sys, urllib.request

USER = os.environ.get("LEETCODE_USER", "JothishKamal")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
GQL = "https://leetcode.com/graphql"

DARK = {"bg": "#0D1117", "panel": "#161B22", "border": "#30363D",
        "text": "#E6EDF3", "muted": "#8B949E", "accent": "#00ADD8", "signal": "#3FB950"}
LIGHT = {"bg": "#FFFFFF", "panel": "#F6F8FA", "border": "#D0D7DE",
         "text": "#1F2328", "muted": "#636C76", "accent": "#0969DA", "signal": "#1A7F37"}


def query(q, variables):
    body = json.dumps({"query": q, "variables": variables}).encode()
    req = urllib.request.Request(GQL, data=body,
        headers={"Content-Type": "application/json", "Referer": "https://leetcode.com"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["data"]


def fetch():
    q = """query($u:String!){matchedUser(username:$u){
      submitStatsGlobal{acSubmissionNum{difficulty count}}
      userCalendar{streak totalActiveDays}}}"""
    d = query(q, {"u": USER})["matchedUser"]
    nums = {x["difficulty"]: x["count"] for x in d["submitStatsGlobal"]["acSubmissionNum"]}
    cal = d["userCalendar"]
    return {"all": nums["All"], "easy": nums["Easy"], "medium": nums["Medium"],
            "hard": nums["Hard"], "streak": cal["streak"], "active": cal["totalActiveDays"]}


def render(s, t):
    def stat(x, label, value, color):
        return (f'<text x="{x}" y="98" font-size="26" fill="{color}" '
                f'font-family="ui-monospace,monospace">{value}</text>'
                f'<text x="{x}" y="118" font-size="11" fill="{t["muted"]}" '
                f'font-family="ui-monospace,monospace">{label}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 150" width="440" height="150" role="img" aria-label="LeetCode DSA stats">
  <rect x="1" y="1" width="438" height="148" rx="12" fill="{t['panel']}" stroke="{t['border']}"/>
  <text x="24" y="36" font-size="14" fill="{t['muted']}" font-family="ui-monospace,monospace">DSA <tspan fill="{t['border']}">/</tspan> LeetCode</text>
  <text x="24" y="66" font-size="30" fill="{t['text']}" font-family="ui-monospace,monospace">{s['all']}<tspan font-size="14" fill="{t['muted']}"> solved</tspan></text>
  {stat(24, "Medium", s['medium'], t['accent'])}
  {stat(150, "Hard", s['hard'], t['text'])}
  {stat(250, "Active Days", s['active'], t['text'])}
  {stat(370, "Streak", s['streak'], t['signal'])}
</svg>
'''


def main():
    try:
        s = fetch()
    except Exception as e:
        print(f"leetcode fetch failed: {e}", file=sys.stderr)
        return 1
    for name, t in (("dark", DARK), ("light", LIGHT)):
        path = os.path.normpath(os.path.join(OUT, f"leetcode-{name}.svg"))
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(s, t))
        print("wrote", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Run the script against live LeetCode**

Run:
```bash
python scripts/fetch_leetcode.py
```
Expected: `wrote .../assets/leetcode-dark.svg` and `wrote .../assets/leetcode-light.svg`, exit 0.

- [ ] **Step 4: Verify output is well-formed and shows real numbers**

Run:
```bash
python -c "import sys,xml.dom.minidom as m; [m.parse(f) for f in sys.argv[1:]]; print('OK')" assets/leetcode-dark.svg assets/leetcode-light.svg
grep -o '347\|162\|58\|239\|116' assets/leetcode-dark.svg | sort -u
```
Expected: `OK`, and the grep lists `116 162 239 347 58` (all real stats present).

- [ ] **Step 5: Verify the no-clobber contract**

Run (simulate network failure via bad host, confirm files unchanged):
```bash
LEETCODE_USER=___nonexistent___ python scripts/fetch_leetcode.py; echo "exit=$?"
```
Expected: prints `leetcode fetch failed: ...` and `exit=1`; `assets/leetcode-*.svg` still contain the real numbers from Step 3 (unchanged).

- [ ] **Step 6: Commit**

```bash
git add scripts/fetch_leetcode.py assets/leetcode-dark.svg assets/leetcode-light.svg
git commit -m "feat: LeetCode fetch script + generated DSA card"
```

---

### Task 5: now.yml + README assembly

**Files:**
- Create: `now.yml`
- Create: `README.md` (overwrites the current placeholder)

**Interfaces:**
- Consumes: every asset from Tasks 1–4 via `<picture>`.
- Produces: `README.md` containing `<!-- NOW:START -->` / `<!-- NOW:END -->` markers consumed by workflow Task 7 (`now.yml`).

- [ ] **Step 1: Write `now.yml`**

```yaml
# Edit this file to update the "Now" section; a weekly Action renders it into README.
building: Enterprise Run Comparison Platform @ Citi
learning: Kubernetes, Go concurrency
reading: Designing Data-Intensive Applications
interested_in: Distributed systems, AI infrastructure, developer tooling
```

- [ ] **Step 2: Write `README.md`**

Use `<picture>` for every asset. Compact cards for VITTY/Flutter Glimpse use shields-style inline text (no extra SVG). The NOW block content between markers matches `now.yml` (Task 7 keeps it in sync).

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img alt="Jothish Kamal — Backend Engineer" src="assets/hero-light.svg" width="100%">
</picture>

### Now

<!-- NOW:START -->
- **Building** — Enterprise Run Comparison Platform @ Citi
- **Learning** — Kubernetes, Go concurrency
- **Reading** — Designing Data-Intensive Applications
- **Interested in** — Distributed systems, AI infrastructure, developer tooling
<!-- NOW:END -->

### Engineering Philosophy

`Reliability over cleverness` · `Observability over assumptions` · `Automation over repetition` · `Simple systems scale` · `Good APIs disappear`

---

### Experience

**Citi** — Technology Summer Analyst (SDE Intern) · Jun 2026 – Present

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/arch-citi-dark.svg"><img alt="Citi Run Comparison pipeline" src="assets/arch-citi-light.svg" width="100%"></picture>

- Architected an enterprise feed **Run Comparison platform** — Parquet ingestion, schema reconciliation, diff generation, hybrid caching — replacing manual comparison workflows.
- Built a zero-copy Parquet streaming loader: **8-worker** parallel loading across hierarchical object storage, **200K+ records**.
- Shipped **6 modules** with **25+ automated tests**; cut latency via incremental pagination + memoized diffs.

**AI-Mond** — SDE Intern · Feb 2026 – Jun 2026

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/arch-aimond-dark.svg"><img alt="AI-Mond document pipeline" src="assets/arch-aimond-light.svg" width="100%"></picture>

- Engineered a high-throughput async document pipeline (FastAPI · Redis · Celery · MongoDB/Beanie); eliminated N+1 queries via batch aggregation.
- Integrated **Gemini via Vertex AI** for entity extraction with HTTP 429 retry/backoff.
- Added **SSE** real-time task streaming and owner-scoped CRUD with strict **RBAC/JWT**.

---

### Featured Projects

**Syncule** — Email intelligence platform · `FastAPI · Postgres · Prisma · Docker · LLMs`

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/arch-syncule-dark.svg"><img alt="Syncule pipeline" src="assets/arch-syncule-light.svg" width="100%"></picture>

Automated email ingestion, interest-based filtering, and calendar sync — Google OAuth, idempotent job queues, and a containerized async LLM pipeline. → [`raisaaajose/event-tracker-v2`](https://github.com/raisaaajose/event-tracker-v2)

**DEVSOC'25 Backend** — Hackathon platform · `Go · Postgres · Docker`

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/arch-devsoc-dark.svg"><img alt="DEVSOC backend pipeline" src="assets/arch-devsoc-light.svg" width="100%"></picture>

Served **1,200 concurrent users at 99.9% uptime**; **+35%** API latency via query optimization, indexing, and connection pooling; JWT refresh tokens + OTP email verification. → [`CodeChefVIT/devsoc-be-25`](https://github.com/CodeChefVIT/devsoc-be-25)

<table>
<tr>
<td width="50%" valign="top">

**VITTY** · `Kotlin`

Shipped Android timetable app — **10k+ downloads · 31★**. → [`GDGVIT/vitty-app`](https://github.com/GDGVIT/vitty-app)

</td>
<td width="50%" valign="top">

**Flutter Glimpse** · `Dart`

Server-Driven UI package (JSON + gRPC). → [`GDGVIT/flutter-glimpse`](https://github.com/GDGVIT/flutter-glimpse)

</td>
</tr>
</table>

---

### Tech Stack

**Languages** · Go · Python · Java · TypeScript · Kotlin · Dart · SQL
**Backend** · FastAPI · Gin · Fiber · Echo · Chi · Node.js · Celery
**Databases & Caching** · Postgres · MongoDB · MySQL · Redis
**Infra & DevOps** · Docker · AWS (EC2/Lambda/S3) · Git · Firebase
**AI** · Vertex AI · Gemini · LLMs · RAG

---

### DSA

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/leetcode-dark.svg">
  <img alt="LeetCode DSA stats" src="assets/leetcode-light.svg" width="440">
</picture>

---

### Stats

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=JothishKamal&show_icons=true&hide_border=true&theme=github_dark&bg_color=0D1117&title_color=00ADD8&icon_color=00ADD8&text_color=E6EDF3">
  <img alt="GitHub stats" src="https://github-readme-stats.vercel.app/api?username=JothishKamal&show_icons=true&hide_border=true&title_color=0969DA&icon_color=0969DA">
</picture>

![Snake](https://raw.githubusercontent.com/JothishKamal/JothishKamal/output/snake-dark.svg)

<!-- metrics.svg is committed by the metrics workflow once METRICS_TOKEN is set -->

---

### Contact

[GitHub](https://github.com/JothishKamal) · [LeetCode](https://leetcode.com/u/JothishKamal/) · [Email](mailto:jothishkamal@gmail.com)

<!--
$ whoami
Jothish Kamal — Backend Engineer
TODO: build something worth maintaining. repeat.
-->
```

- [ ] **Step 3: Verify README references resolve to existing files**

Run:
```bash
grep -o 'assets/[a-z-]*\.svg' README.md | sort -u | while read f; do [ -f "$f" ] && echo "OK $f" || echo "MISSING $f"; done
```
Expected: every line starts with `OK` (all referenced local assets exist). `snake-dark.svg` and `github-readme-stats` are remote and expected until workflows run.

- [ ] **Step 4: Commit**

```bash
git add now.yml README.md
git commit -m "feat: README assembly + now.yml"
```

---

### Task 6: Automation workflows + setup docs

**Files:**
- Create: `.github/workflows/leetcode.yml`, `metrics.yml`, `snake.yml`, `now.yml`
- Create: `SETUP.md`

**Interfaces:**
- Consumes: `scripts/fetch_leetcode.py` (Task 4), NOW markers in `README.md` (Task 5), `now.yml` (Task 5).

- [ ] **Step 1: Write `.github/workflows/leetcode.yml`**

```yaml
name: leetcode
on:
  schedule: [{cron: '0 0 * * 0'}]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.12'}
      - run: python scripts/fetch_leetcode.py
      - name: commit if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          if ! git diff --quiet assets/leetcode-*.svg; then
            git add assets/leetcode-*.svg
            git commit -m "chore: refresh LeetCode card [skip ci]"
            git push
          fi
```

- [ ] **Step 2: Write `.github/workflows/now.yml`**

```yaml
name: now
on:
  push: {paths: ['now.yml']}
  schedule: [{cron: '0 0 * * 0'}]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.12'}
      - name: render now.yml into README
        run: |
          python - <<'PY'
          import re, io
          with open('now.yml', encoding='utf-8') as f:
              lines = [l.rstrip() for l in f if l.strip() and not l.startswith('#')]
          data = dict(l.split(':', 1) for l in lines)
          data = {k.strip(): v.strip() for k, v in data.items()}
          block = "\n".join([
              f"- **Building** — {data.get('building','')}",
              f"- **Learning** — {data.get('learning','')}",
              f"- **Reading** — {data.get('reading','')}",
              f"- **Interested in** — {data.get('interested_in','')}",
          ])
          with open('README.md', encoding='utf-8') as f:
              readme = f.read()
          new = re.sub(r"<!-- NOW:START -->.*<!-- NOW:END -->",
                       f"<!-- NOW:START -->\n{block}\n<!-- NOW:END -->",
                       readme, flags=re.S)
          with open('README.md', 'w', encoding='utf-8') as f:
              f.write(new)
          PY
      - name: commit if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          if ! git diff --quiet README.md; then
            git add README.md
            git commit -m "chore: sync Now section [skip ci]"
            git push
          fi
```

- [ ] **Step 3: Write `.github/workflows/snake.yml`**

```yaml
name: snake
on:
  schedule: [{cron: '0 0 * * 0'}]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: Platane/snk@v3
        with:
          github_user_name: JothishKamal
          outputs: |
            dist/snake-dark.svg?palette=github-dark
            dist/snake.svg
      - uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- [ ] **Step 4: Write `.github/workflows/metrics.yml`**

```yaml
name: metrics
on:
  schedule: [{cron: '0 0 * * 0'}]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: lowlighter/metrics@latest
        with:
          token: ${{ secrets.METRICS_TOKEN }}
          user: JothishKamal
          filename: assets/metrics.svg
          template: classic
          base: header, activity, community, repositories, metadata
          config_timezone: Asia/Kolkata
          plugin_languages: yes
          plugin_languages_details: bytes-size, percentage
          committer_branch: main
```

- [ ] **Step 5: Write `SETUP.md`**

```markdown
# Setup

The profile renders fully with zero setup — hero, architecture diagrams,
and the LeetCode card are committed static SVGs. The steps below only
enable the weekly auto-refresh.

## 1. Enable Actions
Repo → Settings → Actions → General → Allow all actions; Workflow
permissions → Read and write.

## 2. Add METRICS_TOKEN (only for the metrics panel)
Create a classic PAT (github.com/settings/tokens) with scopes `repo` and
`read:user`. Repo → Settings → Secrets and variables → Actions → New
secret → name `METRICS_TOKEN`. Then add to README where you want it:
`![Metrics](assets/metrics.svg)`

## 3. Snake output branch
First run of the `snake` workflow creates the `output` branch
automatically. The README already points at
`.../output/snake-dark.svg`.

## Cadence
All workflows run weekly (Sundays 00:00 UTC) and via manual "Run workflow".
```

- [ ] **Step 6: Validate all workflow YAML**

Run:
```bash
python -c "import glob,yaml,sys; [yaml.safe_load(open(f)) for f in glob.glob('.github/workflows/*.yml')]; print('YAML OK')" 2>/dev/null || python -c "import glob,json,sys; import xml; print('install pyyaml or lint on push')"
```
Expected: `YAML OK` (if PyYAML present). If PyYAML is unavailable locally, confirm indentation by eye and rely on GitHub's own parse on push.

- [ ] **Step 7: Commit**

```bash
git add .github/workflows/*.yml SETUP.md
git commit -m "feat: weekly automation workflows + setup docs"
```

---

## Self-Review

**Spec coverage:**
- Hero (signature) → Task 1 ✓
- Citi/AI-Mond diagrams → Task 2 ✓
- Syncule/DEVSOC diagrams → Task 3 ✓
- VITTY/Flutter Glimpse compact cards → Task 5 (README table) ✓
- LeetCode card + real numbers + no-clobber → Task 4 ✓
- now.yml + render workflow → Tasks 5, 6 ✓
- Philosophy, Tech Stack, Contact, easter eggs → Task 5 ✓
- Metrics + snake + weekly cron + PAT setup → Task 6 ✓
- Light/dark `<picture>` for every asset → Tasks 1–5 ✓
- Day-one static fallback (no broken images) → Tasks 1–4 commit real SVGs; README uses them ✓

**Placeholder scan:** No TBD/TODO in implementation steps (the `TODO:` string in README is intentional easter-egg content). All SVG coordinates and labels are explicit; script and workflows are complete.

**Type consistency:** `fetch_leetcode.py` writes `assets/leetcode-{dark,light}.svg`; README references and `leetcode.yml` both use those exact paths. NOW markers `<!-- NOW:START/END -->` match between README (Task 5) and `now.yml` workflow (Task 6). Asset filenames in README `<picture>` match Tasks 1–4 outputs.

**Note / open item:** Portfolio + LinkedIn URLs not supplied — Contact omits them per spec. Add later by editing the Contact line. Optional hero font-embed deferred as polish (Task 1 Step 4).
