# Northstar — Build Plan & Working Notes

> A personal app to rate daily happiness and correlate it with data from
> multiple sources (self-reported + automated) to learn how to become happier.
> Secondary goal: level up the owner's **data, backend, and infrastructure** skills.

This file is the source of truth across sessions/models. Read it first.

---

## Collaboration contract (how Claude helps WITHOUT doing the learning)

The owner wants to do the thinking. Claude is a tutor/pair, not a code vending machine.

| Owner owns (the learning) | Claude owns (the toil) | Together |
|---|---|---|
| All backend logic, data models, API design | The **entire frontend** (React, mobile-first) | Architecture review before each phase |
| Infra: Dockerfiles, compose, VPS deploy, debugging | Repeated boilerplate *after* owner has done one by hand | Debugging (Claude asks questions, owner finds bug) |
| Data modeling + analysis/correlation logic | Docs lookup, comparing options, reference | Code review of owner's code |

**Claude's default behaviors:**
- Stuck → **Socratic mode** (questions/hints, not answers). Owner can say **"just tell me"** to override.
- Claude writes **skeletons and failing tests**; owner fills the implementation.
- Claude reviews by pointing at problems by category, not handing over patched code.
- Claude does **not** paste large backend logic blocks unless asked.
- Owner can shift the dial (more/less hand-holding) anytime.

---

## Locked decisions

- **Backend:** Python + FastAPI
- **DB:** PostgreSQL (in Docker)
- **Infra target:** Docker on a cheap **Hetzner VPS** (~€4/mo) — chosen as "most learning per euro":
  Linux, Docker, Caddy reverse proxy w/ auto-HTTPS, Postgres backups, systemd.
- **Frontend:** mobile-first web (React/Vite), later wrapped with **Capacitor** into
  installable iOS/Android apps (also unlocks on-device health/screen-time data).
- **Data sources:** self-reported happiness (core) + Polar watch, Calendar,
  phone health/activity, screen time, weather & location.

---

## System mental model

```
Mobile app (Claude builds)  ──▶  FastAPI backend  ──▶  Postgres
                            ◀──   - auth
                                  - daily check-in endpoint
                                  - ingestion jobs ──▶ Open-Meteo (weather)
                                  - analysis/correlations ──▶ Polar AccessLink
                                                          ──▶ Google Calendar
                                                          ──▶ on-device health/screentime
```

Core backend learning lives in: **OAuth token lifecycles**, **idempotent scheduled
ingestion**, **time-series modeling**, **correlation analysis**. Everything else is scaffolding.

---

## Phased roadmap

- **Phase 0 — Foundations** ✅: repo, FastAPI hello world, Postgres in Docker, `/health`
  endpoint that pings the DB via psycopg2, passing pytest. Connection string read from
  `.env` via python-dotenv. Missing: `docker-compose.yml` (deferred — not blocking).
- **Phase 1 — Core loop:** `DailyEntry` model (date, score 1–10, notes, tags), CRUD,
  Alembic migrations. Claude builds the mobile check-in screen.
- **Phase 2 — Easiest automated source: weather.** Open-Meteo (no API key). Nightly job:
  fetch → normalize → upsert idempotently → store. Learn the reusable ingestion pattern.
- **Phase 3 — OAuth sources: Polar, then Google Calendar.** OAuth2 auth-code flow, secure
  token storage, refresh, rate limits, pagination.
- **Phase 4 — Hard part: phone health & screen time.** NO server-side API exists for
  Apple Health / iOS Screen Time / Android screen time. Realistic path = read **on-device**
  via Capacitor health plugins → POST to backend. Owner builds the receiving endpoint.
- **Phase 5 — Payoff: analysis.** pandas, time-series joins, correlations (mind confounders,
  lag, small-n), plain-language insights ("your best days had X").
- **Phase 6 — Ship.** Containerize backend, deploy to Hetzner VPS (Docker + Caddy + HTTPS +
  Postgres backups). Capacitor-wrap the frontend into real apps.

---

## CURRENT STATE (as of 2026-05-31)

**Files:**
- `hello.py` — minimal FastAPI app. ⚠️ **Has a bug:** line 2 reads
  `from FastAPI import FastAPI` — package is lowercase `fastapi`. Owner to fix.
- No `docker-compose.yml` yet. No `requirements.txt`. No `.env`. No `venv`/`.venv`.
- No git remote configured (local repo only).

**Postgres container (started manually via `docker run`, not compose):**
- Name: `test1`, image `postgres:latest` (PG 18)
- Only env set: `POSTGRES_PASSWORD=password` → so user=`postgres`, db=`postgres` (defaults)
- Port: **random** host port `32770` → 5432 (will change on restart — pin it later in compose)
- ⚠️ No named volume → data is lost if container removed (fine for Phase 0).

**Connection strings:**
- From host (where FastAPI runs): `postgresql://postgres:password@localhost:32770/postgres`
- From inside another container: swap host → `host.docker.internal`
- Test (no host installs needed):
  `docker run --rm postgres:18 psql "postgresql://postgres:password@host.docker.internal:32770/postgres" -c "SELECT 1;"`

**Blocker hit:** `uvicorn` not recognized → it's not installed in the active Python env
(no virtualenv set up yet). This is the next thing to resolve.

---

## IMMEDIATE NEXT STEPS (ordered to-do)

1. **Set up a virtual environment** (`python -m venv .venv`, activate it) and
   `pip install fastapi uvicorn sqlalchemy psycopg`. Freeze to `requirements.txt`.
   Add `.venv/`, `.env`, `__pycache__/` to `.gitignore`. → fixes the uvicorn error.
2. **Fix the import bug** in `hello.py` (`fastapi` lowercase) and run
   `uvicorn hello:app --reload`; hit http://127.0.0.1:8000 and /docs.
3. **Verify the DB connection string** with the one-liner above (prove it before coding).
4. **Connect app → DB:** read the connection string from an **env var** (never hard-code),
   add a `/health` endpoint that runs `SELECT 1` and returns ok/fail.
   (Claude can provide a failing test to implement against.)
5. **Write `docker-compose.yml`** (owner writes; Claude reviews): a `db` service
   (`postgres:18`), `POSTGRES_PASSWORD/USER/DB`, **fixed** port `5432:5432`, a **named
   volume** for persistence. This replaces the manual `docker run` + random port.
6. **Set up a git remote** and commit (with secrets gitignored).

## Key concepts already learned (don't re-explain unless asked)
- A container is a sealed appliance; your folder does NOT go into the Postgres container —
  your app **connects out** to it via a connection string.
- Two ways code enters a container: `COPY` in a Dockerfile (prod) vs volume/bind-mount (dev/data).
- Connection string is **assembled** from 5 parts, not stored anywhere to copy-paste.
- `localhost` vs `host.docker.internal` vs service-name depends on **where the code runs**.
- Random Docker port comes from an unpinned `docker run`; compose fixes it.
