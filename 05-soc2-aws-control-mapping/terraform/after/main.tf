# AFTER: Brightline Health AWS baseline with SOC 2 controls applied (fictional).
# Each block notes the SOC 2 criteria it supports.
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = "us-east-1"
}

data "aws_caller_identity" "current" {}

# ---------- Encryption key (CC6.1, CC6.7) ----------
resource "aws_kms_key" "data" {
  description         = "Brightline data and log encryption"
  enable_key_rotation = true
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AccountAdmin"
        Effect    = "Allow"
        Principal = { AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root" }
        Action    = "kms:*"
        Resource  = "*"
      },
      {
        Sid       = "CloudTrailEncrypt"
        Effect    = "Allow"
        Principal = { Service = "cloudtrail.amazonaws.com" }
        Action    = ["kms:GenerateDataKey*", "kms:DescribeKey"]
        Resource  = "*"
      }
    ]
  })
}

# ---------- Account-wide S3 Block Public Access (CC6.1, CC6.6) ----------
resource "aws_s3_account_public_access_block" "account" {
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ---------- Patient document bucket (CC6.1, CC6.7, A1.2) ----------
resource "aws_s3_bucket" "patient_documents" {
  bucket = "brightline-patient-documents"
}

resource "aws_s3_bucket_public_access_block" "patient_documents" {
  bucket                  = aws_s3_bucket.patient_documents.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "patient_documents" {
  bucket = aws_s3_bucket.patient_documents.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_versioning" "patient_documents" {
  bucket = aws_s3_bucket.patient_documents.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_logging" "patient_documents" {
  bucket        = aws_s3_bucket.patient_documents.id
  target_bucket = aws_s3_bucket.trail_logs.id
  target_prefix = "s3-access/patient-documents/"
}

# ---------- CloudTrail: all regions, validated, encrypted, 1-year retention (CC7.2, CC4.1) ----------
resource "aws_s3_bucket" "trail_logs" {
  bucket = "brightline-cloudtrail-logs"
}

resource "aws_s3_bucket_public_access_block" "trail_logs" {
  bucket                  = aws_s3_bucket.trail_logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "trail_logs" {
  bucket = aws_s3_bucket.trail_logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "trail_logs" {
  bucket = aws_s3_bucket.trail_logs.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data.arn
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "trail_logs" {
  bucket = aws_s3_bucket.trail_logs.id
  rule {
    id     = "retain-1-year"
    status = "Enabled"
    filter {}
    expiration {
      days = 365
    }
    noncurrent_version_expiration {
      noncurrent_days = 30
    }
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

resource "aws_s3_bucket_policy" "trail_logs" {
  bucket = aws_s3_bucket.trail_logs.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AWSCloudTrailAclCheck"
        Effect    = "Allow"
        Principal = { Service = "cloudtrail.amazonaws.com" }
        Action    = "s3:GetBucketAcl"
        Resource  = aws_s3_bucket.trail_logs.arn
      },
      {
        Sid       = "AWSCloudTrailWrite"
        Effect    = "Allow"
        Principal = { Service = "cloudtrail.amazonaws.com" }
        Action    = "s3:PutObject"
        Resource  = "${aws_s3_bucket.trail_logs.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*"
        Condition = { StringEquals = { "s3:x-amz-acl" = "bucket-owner-full-control" } }
      }
    ]
  })
}

resource "aws_cloudtrail" "main" {
  name                          = "brightline-trail"
  s3_bucket_name                = aws_s3_bucket.trail_logs.id
  is_multi_region_trail         = true
  include_global_service_events = true
  enable_log_file_validation    = true
  kms_key_id                    = aws_kms_key.data.arn
  depends_on                    = [aws_s3_bucket_policy.trail_logs]
}

# ---------- Least-privilege access: no IAM users; read-only auditor role (CC6.2, CC6.3) ----------
# Engineers sign in through IAM Identity Center (SSO) with MFA; deploys use short-lived GitHub OIDC roles.
resource "aws_iam_role" "auditor" {
  name = "soc2-auditor-readonly"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root" }
      Action    = "sts:AssumeRole"
      Condition = { Bool = { "aws:MultiFactorAuthPresent" = "true" } }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "auditor" {
  role       = aws_iam_role.auditor.name
  policy_arn = "arn:aws:iam::aws:policy/SecurityAudit"
}

resource "aws_iam_account_password_policy" "strict" {
  minimum_password_length        = 14
  require_lowercase_characters   = true
  require_uppercase_characters   = true
  require_numbers                = true
  require_symbols                = true
  password_reuse_prevention      = 24
  max_password_age               = 90
  allow_users_to_change_password = true
}

# ---------- Database: encrypted, private, backups (CC6.1, A1.2) ----------
resource "aws_db_instance" "app" {
  identifier                          = "brightline-app-db"
  engine                              = "postgres"
  instance_class                      = "db.t4g.micro"
  allocated_storage                   = 20
  username                            = "app_admin"
  manage_master_user_password         = true
  storage_encrypted                   = true
  kms_key_id                          = aws_kms_key.data.arn
  backup_retention_period             = 35
  publicly_accessible                 = false
  deletion_protection                 = true
  multi_az                            = true
  iam_database_authentication_enabled = true
  auto_minor_version_upgrade          = true
  copy_tags_to_snapshot               = true
  performance_insights_enabled        = true
  performance_insights_kms_key_id     = aws_kms_key.data.arn
  enabled_cloudwatch_logs_exports     = ["postgresql"]
  monitoring_interval                 = 60
  monitoring_role_arn                 = aws_iam_role.rds_monitoring.arn
  skip_final_snapshot                 = false
  final_snapshot_identifier           = "brightline-app-db-final"
}

resource "aws_iam_role" "rds_monitoring" {
  name = "rds-enhanced-monitoring"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "monitoring.rds.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  role       = aws_iam_role.rds_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# ---------- AWS Backup: daily, 35-day retention, encrypted vault (A1.2, CC9.1) ----------
resource "aws_backup_vault" "main" {
  name        = "brightline-vault"
  kms_key_arn = aws_kms_key.data.arn
}

resource "aws_backup_plan" "daily" {
  name = "daily-35d"
  rule {
    rule_name         = "daily"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 5 * * ? *)"
    lifecycle {
      delete_after = 35
    }
  }
}

# ---------- Detection: GuardDuty (CC7.2) ----------
resource "aws_guardduty_detector" "main" {
  enable = true
}

# ---------- Continuous compliance: AWS Config managed rules (CC4.1, CC7.1) ----------
resource "aws_iam_role" "config" {
  name = "aws-config-recorder"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "config.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "config" {
  role       = aws_iam_role.config.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWS_ConfigRole"
}

resource "aws_config_configuration_recorder" "main" {
  name     = "default"
  role_arn = aws_iam_role.config.arn
  recording_group {
    all_supported                 = true
    include_global_resource_types = true
  }
}

locals {
  config_rules = {
    "root-account-mfa-enabled"           = "ROOT_ACCOUNT_MFA_ENABLED"
    "iam-user-mfa-enabled"               = "IAM_USER_MFA_ENABLED"
    "s3-bucket-public-read-prohibited"   = "S3_BUCKET_PUBLIC_READ_PROHIBITED"
    "s3-bucket-sse-enabled"              = "S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED"
    "cloudtrail-enabled"                 = "CLOUD_TRAIL_ENABLED"
    "rds-storage-encrypted"              = "RDS_STORAGE_ENCRYPTED"
    "rds-instance-public-access-check"   = "RDS_INSTANCE_PUBLIC_ACCESS_CHECK"
  }
}

resource "aws_config_config_rule" "managed" {
  for_each = local.config_rules
  name     = each.key
  source {
    owner             = "AWS"
    source_identifier = each.value
  }
  depends_on = [aws_config_configuration_recorder.main]
}
