# Cloud Provider
provider "aws" {
  region = var.aws_region
}

# Availability Zones
data "aws_availability_zones" "available" {}

# Armazenamento de estado remoto no S3
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket-9384742384"
    key            = "state/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock-table"
  }
}