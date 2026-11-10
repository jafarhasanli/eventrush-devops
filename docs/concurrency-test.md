# EventRush — Concurrency Test Report

## Objective
Verify that the reservation system does not oversell tickets when multiple requests are processed concurrently.

## Test Environment
- Application: FastAPI
- Database: PostgreSQL 17
- Containerization: Docker Compose
- Test client: Python with httpx and ThreadPoolExecutor
- Environment: Local Windows development machine

## Test Configuration
- Event capacity: 100 tickets
- Total reservation requests: 150
- Maximum concurrent workers: 25

## Results

| Metric | Result |
|---|---|
| Successful reservations (HTTP 201) | 100 |
| Rejected reservations (HTTP 409) | 50 |
| Other errors | 0 |
| Execution time | 21.42 seconds |
| Remaining tickets | 0 |
| Database reservation count | 100 |

## Conclusion
The application correctly enforced the 100-ticket capacity limit in this test.

The result was verified through both HTTP responses and PostgreSQL queries.

## Limitations
This was a local concurrency test, not a production-scale performance benchmark. Further testing under different loads and failure conditions is required.