# EventRush — AWS DevOps Portfolio Project

EventRush is a simulated ticket reservation API built to demonstrate cloud infrastructure, containerization, CI/CD, observability, and disaster recovery.

## Technology Stack

- Python, FastAPI, PostgreSQL
- Docker and Docker Compose
- AWS EC2, S3, IAM, Systems Manager
- Terraform Infrastructure as Code
- GitHub Actions and GitHub Container Registry
- Linux, Bash, systemd
- Telegram monitoring alerts

## Architecture

GitHub -> GitHub Actions -> GHCR -> EC2 -> Docker -> FastAPI -> PostgreSQL

PostgreSQL -> Daily Backup -> AWS S3

Health Check / Deployment / Backup Failure -> Telegram Alerts

## Implemented Features

- REST API for events and ticket reservations
- PostgreSQL persistence and duplicate booking protection
- Automated tests and Docker image publishing
- EC2 deployment through systemd and GHCR
- Automated health checks
- Telegram failure notifications
- Daily PostgreSQL backups
- Private, encrypted, versioned S3 backup storage
- S3 lifecycle retention policies
- Successfully tested database recovery from S3
- Successfully tested container deployment rollback
- IAM least-privilege permissions
- EC2 access through AWS Systems Manager

## Verification

- CI and image publishing passed
- API and database health checks passed
- Database backup and S3 restoration passed
- Isolated automatic rollback test passed
- Terraform configuration validated

## Operations

The EC2 host uses systemd services and timers for deployment, monitoring, and backups. Operational Bash scripts were configured directly on the EC2 host and are not yet fully reproducible from this repository.

The API is bound to localhost on EC2. No public inbound access is configured.

## Security

No real payment processing. Do not commit credentials, environment files, database dumps, or Terraform state.

AWS resources may incur charges. Stop or destroy unused lab infrastructure when appropriate.
