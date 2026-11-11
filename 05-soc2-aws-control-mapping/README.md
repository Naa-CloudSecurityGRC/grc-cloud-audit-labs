# 05 · SOC 2 Controls Mapped to an AWS Environment (Infrastructure as Code)

**Evidence:** [step-by-step screenshots from build to remediation](EVIDENCE.md)

> Brightline Health is fictional. The AWS environment is written as Terraform and checked with a real static security scan ([Checkov](https://www.checkov.io/) 3.4.3); it has not been deployed to a live account. To capture live evidence, deploy `terraform/after` to an AWS free-tier account and run `evidence/collect_evidence.sh`.

## 1. Why I built this
To connect SOC 2 criteria to actual cloud settings, which is where audits are tested.

## 2. What I built
| File | What it is |
|---|---|
| [terraform/before/main.tf](terraform/before/main.tf) | AWS baseline as found: unencrypted, public, single-region logging, admin IAM user |
| [terraform/after/main.tf](terraform/after/main.tf) | Fixed baseline: KMS encryption, Block Public Access, multi-region CloudTrail, SSO-only access, backups, GuardDuty, AWS Config rules; each block tagged with the SOC 2 criteria it supports |
| [evidence/checkov_before.json](evidence/checkov_before.json), [checkov_after.json](evidence/checkov_after.json) | Scan results (plus CSV lists of failed checks) |
| [evidence/collect_evidence.sh](evidence/collect_evidence.sh) | Read-only AWS CLI script that saves timestamped evidence for each criterion |
| [SOC2_AWS_Control_Matrix.xlsx](SOC2_AWS_Control_Matrix.xlsx) | 19 rows: SOC 2 criterion → AWS setting → Terraform resource → evidence → status before/after |

## 3. Explain
SOC 2 criteria are written in business language ("the entity restricts logical access..."). Auditors test them through real settings. This project translates each criterion into the AWS setting that satisfies it, writes it as code so it can't silently drift, and shows the evidence an auditor would ask for.

## 4. What was broken (before)
Checkov scan of the original configuration: **34 failed checks, 17 passed.** The most serious:

| Issue | SOC 2 criteria |
|---|---|
| Patient document bucket with no public access block, no default KMS encryption, no versioning | CC6.1, CC6.6, A1.2 |
| Database not encrypted, **publicly accessible**, with **no backups** | CC6.1, CC6.6, A1.2 |
| CloudTrail in one region, no log validation, not encrypted | CC7.2 |
| `deploy-bot` IAM user with **AdministratorAccess** and long-lived access keys | CC6.2, CC6.3 |
| No AWS Config rules or GuardDuty: nothing watching for drift or attacks | CC4.1, CC7.1, CC7.2 |

## 5. What was fixed (after)
Checkov scan of the fixed configuration: **82 passed, 9 failed** (failed checks down 74%).
- KMS key with rotation encrypts S3, RDS, CloudTrail and the backup vault.
- Account-wide S3 Block Public Access; RDS private, Multi-AZ, deletion-protected.
- CloudTrail across all regions with log-file validation and 1-year retention.
- IAM user and admin policy removed; access through SSO; MFA-required read-only auditor role.
- AWS Backup daily with 35-day retention; GuardDuty; 7 AWS Config rules for continuous compliance.

Control matrix: before **0 pass / 4 partial / 14 fail** → after **15 pass / 3 partial / 0 fail** (1 criterion not AWS-related).

## 6. Business impact
- The two most likely paths to a PHI breach (a public bucket and a public, unencrypted database) are closed, and AWS Config now flags them if they reappear.
- Audit-ready: every SOC 2 criterion in scope points to a resource and an evidence command, which cuts the time to answer auditor requests.
- Infrastructure as code means every security change is reviewed and recorded (CC8.1).

## 7. Remediation still open
The 9 remaining Checkov failures, with a decision on each:

| Check | Decision | Owner | Target |
|---|---|---|---|
| CloudTrail → CloudWatch Logs + SNS alerts (CKV2_AWS_10, CKV_AWS_252) | Fix: needed for real-time alerting (CC7.3) | Engineering Lead | 2026-12-31 |
| RDS query logging (CKV2_AWS_30) | Fix with a PHI-safe log setting | Engineering Lead | 2027-01-31 |
| GuardDuty org-wide (CKV2_AWS_3) | Fix when AWS Organizations is set up | IT Lead | 2027-Q1 |
| S3 lifecycle on patient documents (CKV2_AWS_61) | Fix: align with retention policy | Privacy Officer | 2027-01-31 |
| S3 event notifications (CKV2_AWS_62 ×2) | Accept: covered by CloudTrail data events | GRC | Reviewed annually |
| S3 cross-region replication (CKV_AWS_144 ×2) | Accept for now: cost; AWS Backup covers recovery | CEO | Revisit at 2027 budget |
| Quarterly restore test (A1.3) | First test scheduled | Engineering Lead | 2026-12-15 |

## 8. Decisions and trade-offs
I accepted cross-region replication as a cost decision for later, because AWS Backup already covers recovery.
