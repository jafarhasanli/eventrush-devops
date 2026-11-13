
output "ecr_repository_url" {
  description = "Amazon ECR repository URL for EventRush API"
  value       = aws_ecr_repository.eventrush.repository_url
}
