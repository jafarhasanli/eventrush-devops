# EventRush DevOps Roadmap

- [ ] M0: API + tests + Docker + CI pass locally and on GitHub
- [ ] M1: PostgreSQL booking API and atomic capacity control; concurrent tests; Docker Compose volume
- [ ] M2: Terraform VPC, public/private subnet design, EC2, security group, IAM; plan review
- [ ] M3: GitHub Actions tests, image build, ECR and deployment to EC2
- [ ] M4: OIDC, least privilege, secret management, encrypted remote state with locking
- [ ] M5: CloudWatch metrics/logs, load testing, incident exercises, recovery procedure
- [ ] M6: Load balancer, managed database, replicas, optional Kubernetes lab

## Definition of Done per milestone

- Working implementation and reproducible setup
- Automated tests pass
- Short documentation explaining design choices and security/cost considerations
- Evidence (successful CI run, test output, sanitized screenshot or measured report)
- No credentials or state files committed
