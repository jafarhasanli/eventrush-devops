
terraform {
  backend "s3" {
    bucket       = "eventrush-terraform-state-1c0a623e"
    key          = "eventrush/dev/terraform.tfstate"
    region       = "eu-north-1"
    encrypt      = true
    use_lockfile = true
  }
}
