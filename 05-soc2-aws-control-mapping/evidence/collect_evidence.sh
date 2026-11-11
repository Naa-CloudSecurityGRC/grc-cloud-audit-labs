#!/usr/bin/env bash
# Collect SOC 2 evidence from an AWS account (read-only). Run with a role that has the
# AWS managed "SecurityAudit" policy, e.g. the soc2-auditor-readonly role from terraform/after.
# Usage: ./collect_evidence.sh <bucket-name> <trail-name> <db-identifier>
set -euo pipefail
BUCKET=${1:-brightline-patient-documents}; TRAIL=${2:-brightline-trail}; DB=${3:-brightline-app-db}
OUT="evidence_$(date +%Y%m%d_%H%M%S)"; mkdir -p "$OUT"
run() { echo "== $1"; shift; "$@" > "$OUT/$(echo "$1-$2-$3" | tr ' /' '__').json" 2>&1 || echo "  (failed: see file)"; }

run "CC6.1 root MFA + account summary"        aws iam get-account-summary
run "CC6.1 password policy"                   aws iam get-account-password-policy
run "CC6.2 IAM users (expect none)"           aws iam list-users
run "CC6.1 MFA devices"                       aws iam list-virtual-mfa-devices
run "CC6.1 S3 account public access block"    aws s3control get-public-access-block --account-id "$(aws sts get-caller-identity --query Account --output text)"
run "CC6.7 S3 default encryption"             aws s3api get-bucket-encryption --bucket "$BUCKET"
run "A1.2 S3 versioning"                      aws s3api get-bucket-versioning --bucket "$BUCKET"
run "CC7.2 CloudTrail config"                 aws cloudtrail describe-trails --trail-name-list "$TRAIL"
run "CC7.2 CloudTrail status"                 aws cloudtrail get-trail-status --name "$TRAIL"
run "CC6.1 RDS encryption and public access"  aws rds describe-db-instances --db-instance-identifier "$DB"
run "A1.2 Backup plans"                       aws backup list-backup-plans
run "CC7.2 GuardDuty detectors"               aws guardduty list-detectors
run "CC4.1 Config rule compliance"            aws configservice describe-compliance-by-config-rule
echo "Evidence saved to $OUT/ (timestamped). Pair each file with a console screenshot for the SOC 2 artifacts folder."
