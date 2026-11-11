# BEFORE: Brightline Health AWS baseline as found (fictional). Intentionally insecure.
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Patient document bucket: no encryption config, no versioning, no public access block
resource "aws_s3_bucket" "patient_documents" {
  bucket = "brightline-patient-documents"
}

# CloudTrail: single region, no log file validation, no encryption
resource "aws_s3_bucket" "trail_logs" {
  bucket = "brightline-cloudtrail-logs"
}

resource "aws_cloudtrail" "main" {
  name                          = "brightline-trail"
  s3_bucket_name                = aws_s3_bucket.trail_logs.id
  is_multi_region_trail         = false
  enable_log_file_validation    = false
  include_global_service_events = false
}

# Long-lived IAM user with admin rights and access keys
resource "aws_iam_user" "deploy" {
  name = "deploy-bot"
}

resource "aws_iam_user_policy_attachment" "deploy_admin" {
  user       = aws_iam_user.deploy.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_iam_access_key" "deploy" {
  user = aws_iam_user.deploy.name
}

# Database: no backups retained, not encrypted, publicly accessible
resource "aws_db_instance" "app" {
  identifier              = "brightline-app-db"
  engine                  = "postgres"
  instance_class          = "db.t4g.micro"
  allocated_storage       = 20
  username                = "app_admin"
  manage_master_user_password = true
  storage_encrypted       = false
  backup_retention_period = 0
  publicly_accessible     = true
  skip_final_snapshot     = true
}
