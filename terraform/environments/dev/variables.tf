
variable "aws_region" {
  description = "AWS region for EventRush development"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name used in resource tags"
  type        = string
  default     = "eventrush"
}
