# Compliance Program Overview: Brightline Health

| | |
|---|---|
| Company | Brightline Health (fictional): appointment scheduling and telehealth software for 140 outpatient clinics |
| People | 60 staff, fully remote, U.S. only |
| Data | Protected health information (PHI) for ~410,000 patients; clinic staff accounts; payment tokens (card data handled by Stripe) |
| Framework | ISO/IEC 27001:2022 (target certification: Q3 2027), with HIPAA Security Rule and SOC 2 mapped alongside |
| Program owner | Fractional CISO, reporting to the CEO |

## Scope
| In scope | Out of scope |
|---|---|
| Production platform on AWS (us-east-1, us-west-2): web app, API, PostgreSQL (RDS), S3 document storage | Clinics' own systems and devices |
| Microsoft 365 tenant (email, Teams, SharePoint) | Physical offices (none) |
| 22 SaaS tools, 4 of which hold PHI | Stripe card processing (Stripe is PCI DSS Level 1) |
| All employees and contractors with system access | |

## Goals (12 months)
1. Reach a maturity score of 80%+ across the 20 applicable controls (baseline 43%).
2. Close every "Missing" control that affects PHI.
3. Pass an internal audit with no high-severity findings before booking the certification audit.

## Baseline maturity (August 2026)
2 implemented · 13 partially implemented · 5 missing → **43% maturity**. Full detail in [ISO27001_Control_Matrix.xlsx](ISO27001_Control_Matrix.xlsx).

## Governance
- Monthly security steering meeting (CEO, CISO, Engineering Lead, Privacy Officer).
- Control owners update status monthly; the [compliance dashboard](../06-compliance-dashboard/) reports progress.
- Risks are tracked in the [risk register](../02-risk-register/); audits in the [internal audit](../07-internal-audit/).
