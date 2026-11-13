
resource "aws_ecr_repository" "eventrush" {
  name                 = "eventrush-dev-api"
  image_tag_mutability = "IMMUTABLE"
  force_delete         = false

  encryption_configuration {
    encryption_type = "AES256"
  }

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "eventrush-dev-api"
  }
}

resource "aws_ecr_lifecycle_policy" "eventrush" {
  repository = aws_ecr_repository.eventrush.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep the latest 10 Docker images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
