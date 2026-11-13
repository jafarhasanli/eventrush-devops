
provider "aws" {
  region = "eu-north-1"

  default_tags {
    tags = {
      Project     = "eventrush"
      Environment = "shared"
      ManagedBy   = "Terraform"
    }
  }
}
