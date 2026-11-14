# 🎟️ EventRush — End-to-End AWS DevOps & Cloud Infrastructure Project

**A hands-on DevOps portfolio project featuring a containerized ticket reservation API, Infrastructure as Code, automated CI/CD, AWS deployment, system monitoring, failure notifications, database backups, disaster recovery, and automatic rollback.**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-232F3E?logo=amazonwebservices&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?logo=terraform&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=githubactions&logoColor=white)

**Project status:** Core implementation completed and validated through functional, deployment, backup/recovery, and isolated rollback tests.

**Repository:** [github.com/jafarhasanli/eventrush-devops](https://github.com/jafarhasanli/eventrush-devops)

---

## 1. Project Overview

EventRush is a simulated event ticket reservation application developed as a practical environment for learning and implementing modern DevOps engineering concepts.

The project began as a lightweight FastAPI application and progressively evolved into an AWS-hosted system incorporating infrastructure provisioning, container orchestration fundamentals, automated testing, continuous delivery, monitoring, security controls, and disaster recovery.

The primary objective is not to build a commercial ticketing platform. Instead, EventRush demonstrates how the different layers of a software delivery platform work together.

The application provides a real PostgreSQL-backed ticket reservation workflow, while the infrastructure demonstrates how to deploy, monitor, update, secure, back up, and recover that application.

### Project objectives

- Develop a functional REST API with persistent database storage.
- Prevent ticket overselling under concurrent requests.
- Containerize the application and its dependencies.
- Build repeatable AWS infrastructure using Terraform.
- Implement automated testing and Docker image publishing.
- Deploy application updates to an EC2 instance.
- Detect application and database failures.
- Send operational notifications through Telegram.
- Automate PostgreSQL database backups.
- Store backups independently in Amazon S3.
- Validate recovery from an S3-hosted database backup.
- Implement and test automatic rollback after an unhealthy deployment.
- Apply practical security principles, including least-privilege IAM and restricted network access.

---

## 2. Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python 3.12, FastAPI, Uvicorn |
| Database | PostgreSQL, SQLAlchemy, Psycopg |
| Containerization | Docker, Docker Compose |
| Cloud infrastructure | AWS EC2, S3, IAM, VPC, Security Groups |
| Infrastructure as Code | HashiCorp Terraform |
| CI/CD | GitHub Actions |
| Container registry | GitHub Container Registry (GHCR) |
| Server administration | AWS Systems Manager Session Manager |
| Operating system | Amazon Linux 2023 |
| Service automation | systemd services and timers |
| Scripting | Bash |
| Monitoring | HTTP health checks, systemd, Linux system metrics |
| Alerting | Telegram Bot API |
| Backup and recovery | `pg_dump`, `pg_restore`, Amazon S3 |
| Testing | pytest, httpx, concurrent request testing |
| Version control | Git, GitHub, feature branches, pull requests |

### Development versus AWS environment

The local development environment and AWS deployment use slightly different configurations.

| Component | Local environment | AWS environment |
|---|---|---|
| Database | PostgreSQL 17 | PostgreSQL 16 |
| Application | Docker Compose | Docker on EC2 |
| API port | `127.0.0.1:8000` | `127.0.0.1:8000` |
| Database storage | Docker named volume | Persistent Docker named volume |
| Deployment | Local Docker build | GHCR image pulled by EC2 |
| Monitoring | Docker health checks | systemd monitoring and Telegram alerts |
| Backups | Local development data | Automated PostgreSQL and S3 backups |

---

## 3. High-Level Architecture

The application, delivery pipeline, infrastructure, and operations form the following architecture:

```text
                 DEVELOPER
                     |
                  Git Push
                     |
                     v
              GitHub Repository
                     |
                     v
                Pull Request
                     |
                     v
              GitHub Actions
                 CI Pipeline
                     |
            +--------+--------+
            |                 |
        Run pytest       Docker Build
            |                 |
            +--------+--------+
                     |
               Merge to main
                     |
                     v
           Publish Docker Image
                     |
                     v
          GitHub Container Registry
                   GHCR
                     |
                     |
            EC2 Deployment Timer
                     |
                     v
         AWS EC2 — Amazon Linux 2023
                     |
               Docker Engine
                     |
             +-------+-------+
             |               |
             v               v
          FastAPI        PostgreSQL
             |               |
             +-------+-------+
                     |
              Health Checks
                     |
                 systemd
                     |
              Telegram Alerts


       DATABASE PROTECTION PIPELINE

               PostgreSQL
                    |
                 pg_dump
                    |
                    v
             Local Backup
                    |
                    v
                Amazon S3
                    |
            Backup Retention
                    |
                    v
             Recovery Testing
```

### Architectural principles

The system follows several practical operational principles:

**Separation of concerns:** The API, database, infrastructure definitions, CI/CD workflows, and monitoring automation have distinct responsibilities.

**Infrastructure as Code:** AWS infrastructure is provisioned and tracked through Terraform rather than relying entirely on manual console configuration.

**Restricted access:** The EC2 security group has no inbound rules, and remote administration is performed through Systems Manager.

**Automated delivery:** Docker images are published automatically after successful changes to the main branch.

**Recoverability:** Both application rollback and database restoration are supported and have been tested in controlled scenarios.

---

## 4. Backend Application

EventRush uses FastAPI to expose REST endpoints for event discovery, ticket availability, reservations, and operational health checks.

### Implemented endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Returns application health |
| GET | `/db-health` | Verifies the PostgreSQL connection |
| GET | `/events` | Lists available events |
| GET | `/events/{event_id}/availability` | Returns capacity and remaining ticket availability |
| POST | `/reservations` | Creates a ticket reservation |

### Example: Application health

Request:

```bash
curl http://127.0.0.1:8000/health
```

Response:

```json
{
  "status": "ok"
}
```

### Example: Database health

```bash
curl http://127.0.0.1:8000/db-health
```

Response:

```json
{
  "database": "connected"
}
```

### Example: Ticket availability

```bash
curl http://127.0.0.1:8000/events/1/availability
```

Example response:

```json
{
  "id": 1,
  "title": "Demo Concert",
  "capacity": 100,
  "available_tickets": 99
}
```

### Example: Create a reservation

```bash
curl -X POST http://127.0.0.1:8000/reservations \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "customer_email": "customer@example.com"
  }'
```

Successful response:

```json
{
  "reservation_id": 1,
  "event_id": 1,
  "status": "confirmed"
}
```

A successful reservation returns HTTP `201 Created`.

A reservation conflict, unavailable event, or sold-out inventory returns HTTP `409 Conflict`.

Database connection failures are handled through HTTP `503 Service Unavailable` responses.

### Interactive API documentation

FastAPI generates OpenAPI documentation automatically.

Available locally at:

```text
http://127.0.0.1:8000/docs
```

The API version validated during deployment testing was `0.2.1`.

---

## 5. PostgreSQL Database Design

The application uses a relational database with two main tables.

### `events`

Stores event inventory information.

| Column | Purpose |
|---|---|
| `id` | Unique event identifier |
| `title` | Event name |
| `capacity` | Maximum number of available tickets |
| `available_tickets` | Remaining ticket inventory |

### `reservations`

Stores customer reservations.

| Column | Purpose |
|---|---|
| `id` | Unique reservation identifier |
| `event_id` | Reference to the event |
| `customer_email` | Customer identifier |
| `created_at` | Reservation creation timestamp |

### Database constraints

PostgreSQL enforces important data integrity rules:

- Ticket capacity must be nonnegative.
- Available tickets cannot become negative.
- Available tickets cannot exceed event capacity.
- Reservations reference valid events through a foreign key.
- A customer cannot reserve the same event twice using the same email address.

These constraints provide database-level protection in addition to application validation.

---

## 6. Concurrency Control and Overselling Prevention

One of the main functional challenges is preventing multiple simultaneous requests from overselling limited ticket inventory.

For example, an event with 100 available tickets should never produce 120 successful reservations.

### Implementation approach

EventRush uses a conditional PostgreSQL `UPDATE` executed inside a database transaction.

```sql
UPDATE events
SET available_tickets = available_tickets - 1
WHERE id = :event_id
  AND available_tickets > 0
RETURNING id;
```

The database only decrements availability if tickets remain.

The reservation insertion takes place within the same transaction.

If reservation insertion fails because the customer has already booked the event, the transaction is rolled back, including the attempted inventory decrement.

A unique constraint on `(event_id, customer_email)` prevents duplicate customer reservations.

### Why this matters

A simple application-level read followed by a write can introduce race conditions when multiple requests execute concurrently.

Using a conditional database update makes the ticket decrement atomic and allows PostgreSQL to enforce inventory correctness.

### Measured concurrency test

The project includes a documented local concurrency test using Python, HTTP requests, and a thread pool.

| Metric | Recorded result |
|---|---:|
| Initial ticket capacity | 100 |
| Total reservation attempts | 150 |
| Maximum concurrent workers | 25 |
| Successful reservations | 100 |
| Rejected reservations | 50 |
| Other errors | 0 |
| Remaining tickets | 0 |
| Database reservation count | 100 |
| Execution time | 21.42 seconds |

**Result:** The application correctly enforced the available inventory limit during this test. No overselling was observed.

The result was verified both from API responses and from PostgreSQL database queries.

This is a functional concurrency test, not a production-scale load or latency benchmark.

Full details are available in [Concurrency Test Report](docs/concurrency-test.md).

---

## 7. Containerization with Docker

The project uses Docker to package the application and provide reproducible development environments.

### API container

The application image uses:

```text
python:3.12-slim
```

The Dockerfile:

- Installs Python dependencies.
- Copies the FastAPI source code.
- Creates a dedicated non-root application user.
- Runs Uvicorn on port 8000.
- Avoids running the application process as root.

### PostgreSQL container

PostgreSQL runs in a separate container with persistent storage.

The database is attached to a Docker named volume so its data survives ordinary container restarts and recreation.

### Docker networking

The AWS deployment uses a dedicated Docker network:

```text
eventrush-net
```

The API communicates with PostgreSQL using Docker container networking.

PostgreSQL does not publish its database port to the EC2 host.

### Restart behavior

The AWS containers use:

```text
unless-stopped
```

This restart policy allows Docker to restart the containers after unexpected process exits or server restarts, subject to Docker's restart-policy behavior.

---

## 8. Local Development

### Prerequisites

- Python 3.12 or a compatible Python version
- Docker Engine or Docker Desktop
- Docker Compose
- Git

### Clone the repository

```bash
git clone https://github.com/jafarhasanli/eventrush-devops.git
cd eventrush-devops
```

### Start the application with Docker Compose

```bash
docker compose up -d --build
```

### Check container status

```bash
docker compose ps
```

### Verify the API

```bash
curl http://127.0.0.1:8000/health
```

### Verify PostgreSQL connectivity

```bash
curl http://127.0.0.1:8000/db-health
```

### Open API documentation

```text
http://127.0.0.1:8000/docs
```

### Stop the environment

```bash
docker compose down
```

This stops and removes the Compose containers without deleting the named database volume.

### Run automated tests

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

**Note:** The Docker Compose configuration uses development-only database credentials. These values must not be reused for production environments.

---

## 9. AWS Infrastructure with Terraform

Terraform manages the primary AWS infrastructure in the `terraform/environments/dev` directory.

### Provisioned resources

The infrastructure includes:

- A dedicated VPC.
- Networking resources including a subnet, route table, and internet gateway.
- An EC2 instance running Amazon Linux 2023.
- A security group with restricted access.
- An EC2 IAM role and instance profile.
- Systems Manager permissions.
- An Amazon ECR repository.
- An S3 bucket for PostgreSQL backups.
- S3 encryption and public access restrictions.
- S3 versioning and lifecycle policies.
- Least-privilege S3 backup access permissions.

### EC2 configuration

| Property | Configuration |
|---|---|
| Instance type | `t3.micro` |
| Operating system | Amazon Linux 2023 |
| AWS region | `eu-north-1` |
| Root volume | 12 GiB gp3 |
| Root volume encryption | Enabled |
| IMDSv2 | Required |
| Remote administration | AWS Systems Manager |
| Application API | Localhost port 8000 |

The instance is configured with a public IP, but its security group has no inbound rules. Direct public connections to the application or SSH are therefore not allowed through that security group.

### Terraform remote state

Terraform state is stored in an encrypted S3 backend.

The backend also uses S3-based state locking to reduce the risk of conflicting infrastructure modifications.

### Common Terraform commands

```bash
terraform init
terraform fmt
terraform validate
terraform plan
```

Infrastructure changes are reviewed using `terraform plan` before applying them.

### Infrastructure validation

During implementation, Terraform plans were reviewed to confirm that only the intended resources would be created or changed.

After applying the backup infrastructure configuration, a subsequent plan reported:

```text
No changes. Your infrastructure matches the configuration.
```

This indicates that Terraform detected no configuration drift at the time of that check.

---

## 10. CI/CD with GitHub Actions

EventRush implements automated testing, Docker image building, and container publishing using GitHub Actions.

### Continuous Integration

The CI workflow is triggered by:

- Pull requests.
- Pushes to the `main` branch.

The workflow performs the following operations:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs application dependencies.
4. Runs automated tests using pytest.
5. Builds the Docker image after the test job succeeds.

### Container publishing

A separate workflow builds and publishes images to GitHub Container Registry.

Published image:

```text
ghcr.io/jafarhasanli/eventrush-devops
```

Images are tagged using both:

```text
latest
```

and the Git commit SHA.

The SHA tag provides a reference to a particular build, while `latest` is used by the current EC2 deployment mechanism.

### CI/CD pipeline

```text
Developer pushes code
        |
        v
GitHub Pull Request
        |
        v
Automated Python Tests
        |
        v
Docker Build Validation
        |
        v
Merge to main
        |
        v
Build and Publish Image
        |
        v
GitHub Container Registry
        |
        v
EC2 Deployment Polling
        |
        v
Docker Image Update
        |
        v
Application Health Checks
```

### Why GHCR was selected

The infrastructure includes an ECR repository, but the active delivery pipeline uses GitHub Container Registry.

A direct GitHub-to-AWS OIDC configuration was explored. Creating the required AWS IAM OIDC provider was blocked by an explicit organizational Service Control Policy restriction.

Rather than introducing long-lived AWS access keys into GitHub Actions, the project adopted an EC2 pull-based deployment architecture.

This allows the server to obtain published container images without giving GitHub Actions AWS deployment credentials.

---

## 11. Automated Deployment on AWS EC2

The AWS EC2 instance runs the application using Docker.

Deployment automation is implemented with Bash and systemd.

### Deployment components

| Component | Responsibility |
|---|---|
| `deploy.sh` | Pull and deploy the application image |
| `eventrush-deploy.service` | Execute the deployment process |
| `eventrush-deploy.timer` | Periodically check for new images |
| GHCR | Store published application images |
| Docker | Run the application container |

### Deployment interval

The deployment timer is configured to check for new images approximately every 10 minutes.

The service uses `flock` to prevent overlapping deployment executions.

### Deployment process

When the deployment service runs:

1. Pulls the current `latest` image from GHCR.
2. Retrieves the image ID.
3. Compares it with the currently running container image.
4. Exits without changes if the image is already current.
5. Preserves the previous container as a rollback candidate.
6. Starts the replacement container.
7. Checks both application and PostgreSQL connectivity.
8. Removes the rollback candidate after a successful deployment.
9. Restores the previous container if the replacement fails its checks.

### Actual deployment validation

The initial deployed API version was:

```text
0.2.0
```

A new version was merged to the main branch and published through GitHub Actions.

The EC2 deployment service then successfully deployed:

```text
0.2.1
```

Deployment logs confirmed:

```text
Deploying new image...
Checking API and database health...
SUCCESS: EventRush deployment completed.
```

The running application version was independently verified through the OpenAPI document.

### Important operational distinction

The updated image was deployed successfully by the deployment service during a manually initiated service run.

The polling timer was separately verified to be enabled and active. A fully unattended image-change deployment was not independently documented in this test.

---

## 12. Health Monitoring and Observability

EventRush includes lightweight infrastructure and application monitoring using Bash, systemd, curl, and Linux system metrics.

The monitoring script checks:

- FastAPI application health.
- PostgreSQL connectivity.
- Disk utilization.
- Available system memory.

### Example health check output

```text
OK: EventRush API
OK: PostgreSQL connection
OK: Disk usage 23%
OK: Available RAM 399 MiB
```

### Monitoring execution

A dedicated systemd timer runs the monitoring service approximately once per minute.

Main components:

```text
/opt/eventrush/health-check.sh
eventrush-health.service
eventrush-health.timer
```

### Resource thresholds

The monitoring script includes warning thresholds for:

- Disk utilization at or above 85%.
- Available memory below 150 MiB.

The existing implementation treats these resource conditions as warnings. Application and database connectivity failures cause the health-check script to return a failure status.

### Log inspection

Operational events are visible through the systemd journal.

Example:

```bash
sudo journalctl -u eventrush-health.service -n 30 --no-pager
```

### Monitoring scope

This project uses lightweight host-level monitoring.

A centralized observability stack such as Prometheus/Grafana, CloudWatch Logs, or distributed tracing is not part of the validated implementation.

---

## 13. Telegram Incident Notifications

EventRush integrates with the Telegram Bot API to deliver operational failure notifications.

### Supported notification categories

| Alert | Trigger |
|---|---|
| Application health failure | Failed health-check service |
| Deployment failure | Failed deployment service |
| Database backup failure | Failed backup service |
| S3 upload failure | Backup service exits unsuccessfully |

Example messages:

```text
CRITICAL: EventRush health check failed
```

```text
CRITICAL: EventRush deployment failed
```

```text
CRITICAL: EventRush PostgreSQL backup or S3 upload failed
```

### How alert delivery works

The monitoring, deployment, and backup services use systemd's `OnFailure` mechanism.

When a configured service fails, systemd starts the corresponding alert service.

The alert script sends a message to Telegram through an HTTPS request.

### Credential management

Telegram credentials are kept outside the Git repository in a restricted environment file:

```text
/opt/eventrush/telegram.env
```

The file permissions were verified as:

```text
600 root:root
```

The bot token and chat ID are not stored in the repository.

### Validation performed

Telegram notifications were tested during the project.

The application outage monitoring path was tested by temporarily stopping the API and observing a failure notification.

Backup and deployment notification messages were also tested.

A separate intentionally failing systemd test unit confirmed that the systemd `OnFailure` mechanism could trigger a backup-related Telegram alert.

These tests validate alert delivery mechanisms without claiming that every possible real-world failure has been reproduced.

---

## 14. Automated PostgreSQL Backups

Database persistence is essential for the reservation system.

EventRush uses a dedicated backup script to create PostgreSQL backups and store them locally and in Amazon S3.

### Backup workflow

```text
PostgreSQL Database
        |
        v
   pg_dump -Fc
        |
        v
Temporary Backup File
        |
        v
Archive Structure Validation
        |
        v
Local Backup File
        |
        v
    Upload to S3
        |
        v
Backup Retention Cleanup
```

### Backup format

The system uses PostgreSQL's custom dump format:

```bash
pg_dump -Fc
```

This format supports restoration using `pg_restore`.

### Backup validation

After generating a dump, the script:

1. Verifies the file is nonempty.
2. Checks that `pg_restore` can read the archive structure.
3. Saves the completed local backup.
4. Uploads the file to S3.
5. Performs local retention cleanup after a successful upload.

If the upload fails, the service reports failure and retains the local dump.

### Scheduling

The backup service is scheduled daily at:

```text
03:00 UTC
```

The systemd timer uses:

```text
Persistent=true
```

This allows a missed scheduled execution to be triggered after the timer becomes active again.

For example, if the EC2 instance was powered off during the scheduled backup time, the timer can catch up when the instance is restarted.

### Local backup retention

The script removes date-named local backup files after approximately seven days.

Backup files have restrictive file permissions.

### Validation

The backup system was tested successfully by running the backup service.

Operational logs confirmed:

```text
Starting EventRush database backup...
Local backup created: ...
Uploading backup to AWS S3...
SUCCESS: Backup uploaded to S3.
Backup completed.
```

---

## 15. Amazon S3 Backup Storage

A dedicated S3 bucket stores database backups independently from the EC2 instance's local disk.

### S3 security configuration

The backup bucket uses:

- S3 Block Public Access.
- Default SSE-S3 encryption (AES256).
- Bucket versioning.
- Terraform-managed lifecycle rules.
- Scoped IAM permissions.

### Backup storage prefix

Database backups are stored under:

```text
database/
```

Example object path:

```text
s3://<backup-bucket>/database/eventrush-YYYYMMDD-HHMMSS.dump
```

### Retention policy

| Backup category | Retention |
|---|---|
| Local date-named backups | Approximately 7 days |
| Current S3 objects | 30 days |
| Noncurrent S3 object versions | 7 days |

S3 lifecycle policies are managed using Terraform.

The 30-day expiration policy applies to the current objects under the database backup prefix. Versioning and S3 lifecycle behavior can affect when historical object versions are permanently removed.

### IAM permissions

The EC2 instance role is granted narrowly scoped permissions:

```text
s3:PutObject
s3:GetObject
```

These permissions are restricted to the designated database backup prefix.

The role does not require general access to every S3 bucket, and no persistent AWS access keys are stored on the EC2 instance for this workflow.

### Security benefit

Separating backup storage from the EC2 disk improves recoverability if the instance or its local storage becomes unavailable.

However, backup copies in the same AWS account are not equivalent to a fully isolated cross-account or cross-region disaster recovery architecture.

---

## 16. Disaster Recovery and Database Restoration

A backup is only useful if the stored data can be restored.

EventRush therefore includes an actual recovery test using a database backup downloaded from Amazon S3.

### Recovery scenario

The test followed this sequence:

1. A PostgreSQL backup was created on EC2.
2. The dump was uploaded to Amazon S3.
3. EC2 downloaded the stored dump using its IAM role.
4. The PostgreSQL archive structure was inspected.
5. A separate test database was created.
6. The S3-hosted backup was restored into the test database.
7. Database contents were verified.
8. Production API and database health were checked.
9. Temporary test databases were removed.

### Recovery verification results

The restored test database contained the expected sample event:

| Field | Value |
|---|---|
| Event | Demo Concert |
| Capacity | 100 |
| Available tickets | 99 |
| Reservation count | 1 |

The restoration completed successfully without overwriting the production database.

A subsequent health check confirmed that the running API and PostgreSQL database remained healthy.

### What this test demonstrates

The test validates the following recovery path:

```text
PostgreSQL
    |
    v
Database Dump
    |
    v
Amazon S3
    |
    v
Backup Download
    |
    v
pg_restore
    |
    v
Recovered Database
    |
    v
Data Verification
```

This demonstrates that the backup artifacts were not merely created but could also be used to recover application data.

### Recovery limitations

The tested recovery was performed using a separate test database on the existing PostgreSQL server.

It was not a complete rebuild of the EC2 host, Docker environment, and application infrastructure from zero.

Formal recovery time objectives (RTO) and recovery point objectives (RPO) have not been established.

---

## 17. Automatic Deployment Rollback

A failed deployment should not leave an application permanently unavailable.

EventRush includes automatic rollback logic in its deployment script.

### Rollback strategy

During a new deployment, the existing application container is preserved temporarily.

The new container is started and evaluated using application and database health checks.

If the new container does not pass the checks, the deployment script attempts to remove it and restore the previously working container.

### Rollback sequence

```text
Current Healthy Container
           |
           v
   New Image Available
           |
           v
  Preserve Old Container
           |
           v
  Start Replacement Image
           |
           v
      Health Check
           |
      +----+----+
      |         |
   Healthy    Failed
      |         |
      v         v
  Complete   Rollback
  Deployment     |
                 v
          Restore Old Container
                 |
                 v
          Service Recovery
```

### Actual rollback test

An isolated deployment test was performed using a separate application container bound to port `18000`.

The test deliberately substituted an Nginx image for the expected FastAPI image.

Although the replacement container started, it could not satisfy the required EventRush API health checks.

The deployment script detected the failure and initiated rollback.

### Recorded rollback output

```text
Deploying new image...
Checking API and database health...
Deployment failed. Rolling back...
Previous container restored.
```

After rollback, the test API returned:

```json
{
  "status": "ok"
}
```

The production application and database were also checked independently and remained healthy.

The temporary test container and test script were removed afterward.

### Result

**The isolated rollback test succeeded.**

It demonstrated successful recovery from a replacement container that started but did not provide the expected API functionality.

The same rollback design is used by the production deployment script, although a deliberately broken image was not deployed against the production API during this test.

---

## 18. Security Measures

Security was considered throughout infrastructure and deployment implementation.

### 18.1 Network isolation

The EC2 security group was verified to have:

```json
[]
```

for inbound permissions.

The FastAPI service is bound to:

```text
127.0.0.1:8000
```

The database port is not published on the EC2 host.

This prevents direct public access through the configured security group and Docker port bindings.

### 18.2 AWS Systems Manager

Server administration is performed through AWS Systems Manager Session Manager.

This removes the requirement to expose SSH port 22 publicly for routine administrative access.

The SSH daemon may still run locally, but external access is restricted by the security group.

### 18.3 IAM roles

The EC2 instance uses an IAM instance profile to access AWS services.

S3 backup permissions are restricted to the relevant bucket prefix and required operations.

Long-lived AWS access keys are not required by the backup automation.

### 18.4 Secrets protection

Application, database, and Telegram environment files were verified to use restrictive permissions:

```text
600 root:root
```

Sensitive credentials are not included in the Git repository.

### 18.5 Container isolation

The Dockerfile runs the application process using a non-root user.

The database and API run as separate Docker containers.

### 18.6 AWS instance metadata

Terraform configures the EC2 instance to require IMDSv2 tokens.

### 18.7 Data encryption

The EC2 root EBS volume is encrypted.

The database backup S3 bucket uses server-side encryption.

Terraform state is stored in an encrypted S3 backend.

### Security limitations

The project is a DevOps learning environment rather than a fully hardened production platform.

It does not currently implement a public TLS endpoint, WAF, customer authentication, automated container vulnerability gate, centralized security monitoring, or a full secrets-management service.

---

## 19. Incident Response and Operational Commands

The following commands are useful for troubleshooting the EC2 environment.

They are intended to run inside the EC2 instance through Systems Manager.

### Check Docker containers

```bash
sudo docker ps
```

### Inspect API logs

```bash
sudo docker logs --tail 50 eventrush-api
```

### Check application health

```bash
curl -fsS http://127.0.0.1:8000/health
```

### Check database connectivity

```bash
curl -fsS http://127.0.0.1:8000/db-health
```

### Run the monitoring script

```bash
sudo /opt/eventrush/health-check.sh
```

### Inspect deployment logs

```bash
sudo journalctl -u eventrush-deploy.service -n 50 --no-pager
```

### Inspect backup logs

```bash
sudo journalctl -u eventrush-backup.service -n 50 --no-pager
```

### Inspect monitoring logs

```bash
sudo journalctl -u eventrush-health.service -n 50 --no-pager
```

### Show scheduled EventRush tasks

```bash
systemctl list-timers --all 'eventrush-*'
```

### Verify container restart policies

```bash
sudo docker inspect eventrush-api eventrush-db \
  --format '{{.Name}}: {{.HostConfig.RestartPolicy.Name}}'
```

### List local database backups

```bash
sudo ls -lh /opt/eventrush/backups/
```

### Important operational warning

Database restoration, manual deployment, and container replacement should be performed carefully.

Never overwrite the production database as part of routine recovery testing.

The backup and deployment automation scripts currently reside on the EC2 host. Their complete operational definitions are not yet packaged as a reproducible provisioning module inside this repository.

---

## 20. Repository Structure

```text
eventrush-devops/
|
|-- .github/
|   +-- workflows/
|       |-- ci.yml
|       +-- publish-ghcr.yml
|
|-- app/
|   |-- __init__.py
|   |-- main.py
|   +-- database.py
|
|-- database/
|   +-- init.sql
|
|-- docs/
|   |-- ROADMAP.md
|   +-- concurrency-test.md
|
|-- scripts/
|   +-- load_test.py
|
|-- terraform/
|   +-- environments/
|       +-- dev/
|           |-- backend.tf
|           |-- ec2.tf
|           |-- ecr.tf
|           |-- iam.tf
|           |-- security.tf
|           |-- main.tf
|           |-- providers.tf
|           |-- variables.tf
|           |-- outputs.tf
|           |-- versions.tf
|           |-- backup_s3.tf
|           |-- backup_iam.tf
|           +-- ...
|
|-- tests/
|   +-- test_api.py
|
|-- .dockerignore
|-- .gitignore
|-- Dockerfile
|-- compose.yaml
|-- requirements.txt
+-- README.md
```

### Directory responsibilities

**`app/`** contains the FastAPI application, database connectivity, and reservation business logic.

**`database/`** contains the PostgreSQL schema initialization script and sample event data.

**`tests/`** contains automated API tests.

**`scripts/`** contains the application load-testing utility.

**`.github/workflows/`** defines CI and container publishing automation.

**`terraform/`** contains Infrastructure as Code for AWS networking, compute, identity, and backup storage.

**`docs/`** contains supporting project documentation and concurrency testing evidence.

The historical roadmap in `docs/ROADMAP.md` represents an earlier project plan and does not fully describe the architecture ultimately implemented.

---

## 21. Development Process and Git Workflow

The project was developed incrementally using Git feature branches and GitHub pull requests.

Each major change was implemented, tested, reviewed, and merged into the main branch.

### Main development milestones

| Milestone | Delivered functionality |
|---|---|
| M0 | Initial application, Docker setup, and testing foundation |
| M1 | PostgreSQL-backed ticket reservations and concurrency protection |
| M2 | AWS infrastructure provisioning with Terraform |
| M3–M5 | Container publishing, EC2 deployment, operational monitoring, and alerting foundations |
| M6 | Automated deployment polling, GHCR updates, and deployment health checks |
| M7 | Automated PostgreSQL backups, S3 retention, and recovery testing |
| M8 | Security validation, rollback testing, and portfolio documentation |

The final documentation pull request was also merged into the main branch.

The milestone table reflects the actual implementation path, which evolved from the original roadmap.

### Version control practices

The project uses:

- Feature branches for isolated development.
- Pull requests for merging changes.
- Automated CI verification.
- Descriptive commit messages.
- Infrastructure configuration tracked alongside application code.

---

## 22. Key Challenges and Engineering Decisions

### Challenge 1: Concurrent ticket reservations

**Problem:** Multiple simultaneous requests could potentially oversell limited inventory.

**Approach:** PostgreSQL conditional updates, transactions, and unique constraints.

**Result:** The 150-request concurrency test produced exactly 100 successful reservations for a 100-ticket event.

### Challenge 2: Secure AWS deployment authentication

**Problem:** The AWS environment restricted creation of the GitHub Actions OIDC provider through an organizational policy.

**Approach:** Use GitHub Container Registry and EC2-initiated image polling instead of adding permanent AWS credentials to GitHub.

**Result:** Container publishing and EC2 deployment were implemented without GitHub-held AWS deployment keys.

### Challenge 3: Remote server administration

**Problem:** Administrative access was needed without opening the instance to inbound SSH connections.

**Approach:** Configure the EC2 IAM role and use AWS Systems Manager Session Manager.

**Result:** EC2 administration was possible with no inbound security group rules.

### Challenge 4: Database reliability

**Problem:** Database data stored only on an EC2-attached volume could be lost if storage became unavailable.

**Approach:** Automated PostgreSQL dumps, local backups, independent S3 storage, and retention policies.

**Result:** A backup was successfully downloaded from S3 and restored into a PostgreSQL test database.

### Challenge 5: Detecting and reporting failures

**Problem:** An unhealthy application or failed deployment could otherwise remain unnoticed.

**Approach:** systemd monitoring, health endpoints, failure-triggered services, and Telegram alerts.

**Result:** Health-related alerts and failure notification mechanisms were tested successfully.

### Challenge 6: Safe application updates

**Problem:** An unhealthy replacement container could interrupt application availability.

**Approach:** Preserve the previous container during deployment, validate the replacement, and restore the old container on failure.

**Result:** A deliberately unhealthy image triggered successful rollback in an isolated test.

---

## 23. Verification Summary

The following outcomes were observed during project implementation.

| Test | Observed outcome |
|---|---|
| Automated API tests | Passed in GitHub Actions |
| Docker image build | Passed |
| GHCR image publishing | Passed |
| PostgreSQL persistence | Verified |
| Concurrent reservations | 100 accepted, 50 rejected |
| EC2 API health | Passed |
| EC2 database health | Passed |
| Deployment service | Successfully deployed v0.2.1 |
| Deployment timer | Enabled and active |
| Health monitoring | Operational |
| Telegram notification delivery | Verified |
| PostgreSQL local backup | Successful |
| Automated S3 backup upload | Successful |
| S3 lifecycle configuration | Verified |
| S3 backup download | Successful |
| Database restoration | Successful |
| Isolated automatic rollback | Successful |
| Terraform infrastructure validation | No changes detected after deployment |
| Security group inbound access | No inbound rules |

These results represent the tests performed during development, not an ongoing production uptime or performance guarantee.

---

## 24. Current Limitations and Potential Improvements

EventRush successfully demonstrates the principal components of a practical DevOps workflow.

It is intentionally not presented as a fully production-ready commercial ticketing service.

Possible future improvements include:

1. **Reproducible server configuration:** Version the operational Bash scripts and systemd units in Git and automate their installation.
2. **Stronger deployment guarantees:** Pin deployments to immutable image digests or explicitly approved release versions.
3. **Centralized observability:** Add CloudWatch Logs, Prometheus, Grafana, or structured application metrics.
4. **Managed database:** Evaluate Amazon RDS instead of container-hosted PostgreSQL.
5. **High availability:** Add multiple application instances and a load balancer.
6. **Infrastructure resilience:** Extend recovery testing to full instance replacement.
7. **Secrets management:** Integrate AWS Systems Manager Parameter Store or Secrets Manager.
8. **Automated security scanning:** Add dependency and container vulnerability checks to CI.
9. **Public HTTPS access:** Introduce an authenticated, TLS-protected application endpoint if external access becomes necessary.
10. **Disaster recovery isolation:** Evaluate cross-account or cross-region backup replication.
11. **Operational metrics:** Define measurable RTO, RPO, and service-level objectives.

These improvements are optional future extensions, not requirements for the completed portfolio lab.

---

## 25. What I Learned

Building EventRush provided practical experience across multiple stages of software delivery and cloud operations.

### Software development

- Building REST APIs using FastAPI.
- Working with PostgreSQL transactions.
- Designing relational schemas and integrity constraints.
- Understanding race conditions and concurrency control.
- Writing automated tests.

### Containerization and Linux

- Building Docker images.
- Configuring container networks and volumes.
- Managing container lifecycle and restart behavior.
- Working with Linux permissions.
- Writing Bash automation scripts.
- Managing systemd services and timers.
- Debugging application and service logs.

### AWS and Infrastructure as Code

- Provisioning networking and EC2 infrastructure with Terraform.
- Managing IAM roles and instance profiles.
- Using Systems Manager instead of public SSH access.
- Configuring S3 storage, encryption, versioning, and lifecycle policies.
- Working with encrypted remote Terraform state.
- Applying least-privilege access principles.

### CI/CD and reliability

- Designing GitHub Actions workflows.
- Publishing Docker images to GHCR.
- Automating image deployment.
- Checking application health after deployment.
- Implementing rollback behavior.
- Sending Telegram operational alerts.
- Creating and restoring PostgreSQL backups.
- Verifying disaster recovery procedures through controlled tests.

### Engineering mindset

The most important lesson was that successful application development involves more than writing backend code.

A reliable delivery workflow must also consider deployment automation, secure access, observability, persistent storage, recovery, and the ability to respond when something fails.

---

## 26. Running Costs and Resource Management

The project uses real AWS services, so running the infrastructure may generate charges.

Potential costs include:

- EC2 compute usage.
- EBS storage.
- Public IPv4 addressing.
- S3 backup storage and requests.
- Terraform state storage.
- Other applicable AWS services and data transfer.

The EC2 instance can be stopped between development sessions to reduce compute charges.

Stopping EC2 does not automatically eliminate charges for EBS volumes, allocated public IPv4 resources, S3 storage, or other retained infrastructure.

Terraform-managed resources should not be destroyed without considering backup retention and recovery requirements.

---

## 27. Project Scope

**EventRush is an educational and portfolio-focused DevOps project.**

It simulates event ticket reservations and uses real cloud infrastructure for deployment and operations.

It does not process real payments, issue commercial tickets, or provide a public production booking service.

The system is intended to demonstrate applied knowledge of backend development, cloud infrastructure, containerization, automation, security, and reliability engineering.

---

## 28. Final Outcome

EventRush evolved from a small FastAPI starter application into an AWS-hosted, containerized system with an automated software delivery pipeline and validated operational recovery mechanisms.

The completed project demonstrates:

- Functional database-backed application development.
- Concurrency-safe ticket reservation logic.
- Docker containerization.
- AWS infrastructure provisioned through Terraform.
- CI/CD automation with GitHub Actions.
- Container publishing through GitHub Container Registry.
- Automated EC2 deployment checks.
- Application and database health monitoring.
- Telegram operational notifications.
- Scheduled PostgreSQL database backups.
- Independent encrypted S3 backup storage.
- Successful database recovery from S3.
- Tested automatic rollback for an unhealthy replacement container.
- Practical network and IAM security controls.

**The core goal of the project was achieved: to build, deploy, operate, monitor, protect, and recover a real containerized application using modern DevOps engineering practices.**

---

## Author

**Jafar Hasanli**

DevOps / Cloud Engineering Portfolio

- **GitHub:** [jafarhasanli](https://github.com/jafarhasanli)
- **Project Repository:** [EventRush DevOps](https://github.com/jafarhasanli/eventrush-devops)

---

*Built as a hands-on learning project focused on AWS, Terraform, Docker, Linux, GitHub Actions, automation, monitoring, and disaster recovery.*
