# EventRush — DevOps Portfolio Lab

A simulated ticketing API used to practice Docker, Linux, AWS, Terraform, CI/CD, security, and observability.

**Current status:** M0 starter only. Not a ticket-booking system yet; no real AWS infrastructure is created.

## Quick start (WSL/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs or call `curl http://127.0.0.1:8000/health`.

## Docker

```bash
docker compose up -d --build
curl http://127.0.0.1:8000/events
docker compose down
```

## CI

`.github/workflows/ci.yml` runs Python tests, then builds the Docker image on push to `main` and on pull requests. It does not publish or deploy anything yet.

## Architecture (M0)

Browser -> localhost:8000 -> Docker container -> FastAPI; example event data is in memory.

## Planned features

See [docs/ROADMAP.md](docs/ROADMAP.md). PostgreSQL, reservation operations, AWS, and Terraform are planned, not currently implemented.

## Safety

No actual payment processing. Avoid committing AWS keys, `.env`, or Terraform state. AWS resources may incur fees later.
