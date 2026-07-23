# Jothish Kamal

**Backend Engineer** — building distributed systems, AI infrastructure, and developer tooling.
Currently Technology Summer Analyst @ Citi.

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/JothishKamal)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-181717?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jothishkamal/)
[![LeetCode](https://img.shields.io/badge/LeetCode-181717?style=flat-square&logo=leetcode&logoColor=white)](https://leetcode.com/u/JothishKamal/)
[![Email](https://img.shields.io/badge/Email-181717?style=flat-square&logo=gmail&logoColor=white)](mailto:jothishkamal@gmail.com)

## Currently

<!-- NOW:START -->
- **Building** — Enterprise Run Comparison Platform @ Citi
- **Learning** — Kubernetes · Go concurrency
- **Reading** — Designing Data-Intensive Applications
- **Status** — Available for backend engineering roles
<!-- NOW:END -->

## Engineering Philosophy

Reliability over cleverness. Observability over assumptions. Automation over repetition. Simple systems scale better. Good APIs disappear.

---

## Experience

### Citi — Technology Summer Analyst (SDE Intern)

Jun 2026 – Present

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/arch-citi-dark.svg">
  <img alt="Citi Run Comparison pipeline: enterprise feeds to object storage to Parquet loader to schema reconciliation to diff engine to Streamlit" src="assets/arch-citi-light.svg" width="100%">
</picture>

> **Problem** — Manual, error-prone reconciliation between consecutive enterprise feed runs.
> **Solution** — A schema-aware Parquet comparison engine with zero-copy streaming, parallel loading, and hybrid caching.
> **Impact** — 200K+ records · 8-worker parallel loading · 6 modules · 25+ automated tests

### AI-Mond — SDE Intern

Feb 2026 – Jun 2026

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/arch-aimond-dark.svg">
  <img alt="AI-Mond document pipeline: documents to FastAPI to Redis to Celery to Vertex AI to MongoDB" src="assets/arch-aimond-light.svg" width="100%">
</picture>

> **Problem** — Slow, N+1-bound document processing with no real-time feedback.
> **Solution** — Async FastAPI, Redis and Celery pipeline with batch aggregation and Gemini extraction via Vertex AI.
> **Impact** — SSE task streaming · HTTP 429 retry/backoff · RBAC/JWT · 28 rule functions

---

## Featured Projects

### Syncule — Email intelligence platform

FastAPI · Postgres · Prisma · Docker · LLMs

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/arch-syncule-dark.svg">
  <img alt="Syncule pipeline: inbox to Google OAuth to FastAPI to Postgres to job queue to LLM to calendar" src="assets/arch-syncule-light.svg" width="100%">
</picture>

Automated email ingestion, interest-based filtering, and calendar sync — Google OAuth, idempotent job queues, and a containerized async LLM pipeline.
[View repository →](https://github.com/raisaaajose/event-tracker-v2)

### DEVSOC'25 Backend — Hackathon platform

Go · Postgres · Docker

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/arch-devsoc-dark.svg">
  <img alt="DEVSOC backend pipeline: users to Go API to JWT auth to Postgres to email OTP" src="assets/arch-devsoc-light.svg" width="100%">
</picture>

Served 1,200 concurrent users at 99.9% uptime; improved API response times by 35% via query optimization, indexing, and connection pooling; JWT refresh tokens with OTP email verification.
[View repository →](https://github.com/CodeChefVIT/devsoc-be-25)

### Also maintained

| Project | Stack | Notes |
| --- | --- | --- |
| [VITTY](https://github.com/GDGVIT/vitty-app) | Kotlin | Shipped Android timetable app — 10k+ downloads, 31 stars |
| [Flutter Glimpse](https://github.com/GDGVIT/flutter-glimpse) | Dart | Server-Driven UI package with JSON and gRPC support |

---

## Tech Stack

| Languages | Backend | Infrastructure | AI |
| --- | --- | --- | --- |
| Go | FastAPI | Docker | Vertex AI |
| Python | Gin · Fiber | AWS | Gemini |
| Java | Node.js | Postgres · Redis | LLMs |
| TypeScript | Celery | MongoDB | RAG |
| SQL | | | |

---

## DSA

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/leetcode-dark.svg">
  <img alt="LeetCode statistics" src="assets/leetcode-light.svg" width="440">
</picture>

---

## Contributions

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/JothishKamal/JothishKamal/output/snake-dark.svg">
  <img alt="Contribution graph" src="https://raw.githubusercontent.com/JothishKamal/JothishKamal/output/snake.svg">
</picture>

---

## Contact

[GitHub](https://github.com/JothishKamal) · [LinkedIn](https://www.linkedin.com/in/jothishkamal/) · [LeetCode](https://leetcode.com/u/JothishKamal/) · [Email](mailto:jothishkamal@gmail.com)

<div align="center"><sub><!-- DEPLOYED:START -->last deployed 2026-07-23 · generated with GitHub Actions<!-- DEPLOYED:END --></sub></div>

<!--
$ whoami
Jothish Kamal — Backend Engineer
TODO: build something worth maintaining. repeat.
-->
