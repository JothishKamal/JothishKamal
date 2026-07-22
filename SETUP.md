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
