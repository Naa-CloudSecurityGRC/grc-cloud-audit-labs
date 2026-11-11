# 01 · Mini Compliance Program (ISO/IEC 27001:2022)

> Brightline Health is a fictional 60-person healthcare SaaS company. All findings and data are simulated for this portfolio.

## 1. Why I built this
To show how to stand up a compliance program from nothing: scope, controls, gaps, owners.

## 2. What I built
- Defined scope for a healthcare SaaS on AWS and Microsoft 365: assets, users, data types, exclusions ([Compliance_Program_Overview.md](Compliance_Program_Overview.md)).
- Selected 20 applicable ISO 27001:2022 Annex A controls and built a control matrix: Control ID, requirement, status, finding, owner, needed action ([ISO27001_Control_Matrix.xlsx](ISO27001_Control_Matrix.xlsx)).
- Re-assessed every control 90 days later to measure progress.

## 3. Explain
ISO 27001 certification is often a contract requirement for selling to larger health systems. Before paying an auditor, a company needs to know where it stands. The matrix turns "are we secure?" into 20 specific yes/partly/no answers, each with a named owner and a next step.

## 4. What was broken (baseline, August 2026)
Maturity was **43%**: 2 controls implemented, 13 partial, 5 missing. The five most serious gaps:

| # | Gap | Control | Why it matters |
|---|---|---|---|
| 1 | No incident response plan | A.5.24 | A PHI breach would be handled ad hoc; HIPAA breach-notification deadlines could be missed |
| 2 | MFA missing on the AWS root account and 3 IAM users | A.5.17 | One stolen password could expose the production database |
| 3 | No user access reviews, ever | A.5.18 | Former staff or over-privileged users could still reach PHI |
| 4 | No vendor assessments; 4 vendors hold PHI, only 2 BAAs signed | A.5.19, A.5.20 | HIPAA requires BAAs with every business associate |
| 5 | CloudTrail in one region, 30-day retention | A.8.15 | Activity in other regions is invisible; too little history to investigate a breach |

## 5. What was fixed (by November 2026)
| Gap | Fix | Evidence |
|---|---|---|
| 1 | IR plan written and tested in a tabletop exercise | [Project 04](../04-incident-response-tabletop/) |
| 2 | MFA enforced on root and all users; IAM users replaced with SSO roles | [Project 05](../05-soc2-aws-control-mapping/) |
| 3 | First quarterly access review completed for AWS and Microsoft 365 (EHR integration still pending) | Control matrix, A.5.18 |
| 4 | Vendor questionnaire built; first PHI vendor assessed; BAAs signed with 2 remaining PHI vendors | [Project 03](../03-vendor-assessment-notion/) |
| 5 | Multi-region CloudTrail with log-file validation and 1-year retention | [Project 05](../05-soc2-aws-control-mapping/) |

Maturity rose from **43% to 80%** on the 90-day self-assessment: 13 implemented, 6 partial, 1 missing.

> **Audit correction:** the [internal audit](../07-internal-audit/) later found two controls (A.8.8 vulnerabilities, A.8.13 backups) marked "Implemented" without evidence that they operate. Corrected maturity is **75%** (11 implemented, 8 partial, 1 missing); the [dashboard](../06-compliance-dashboard/) shows the corrected figures.

## 6. Business impact
- **Sales:** the company can now answer enterprise security questionnaires with evidence instead of promises, which unblocks two health-system deals waiting on security review.
- **Regulatory:** BAAs now cover all four PHI vendors, closing a direct HIPAA compliance gap.
- **Breach readiness:** a tested IR plan and a year of CloudTrail history mean a breach can be investigated and reported on time.

## 7. Remediation still open
| Item | Owner | Target |
|---|---|---|
| Business continuity plan (A.5.29): BIA and draft plan done in [project 09](../09-business-impact-analysis-bcp/); approval pending | COO | 2026-12-15 |
| Data classification labels on all PHI stores (A.5.12) | Privacy Officer | 2027-02-28 |
| HIPAA Security Rule risk analysis (A.5.34) | Privacy Officer | 2027-01-31 |
| SSO for remaining PHI apps (A.8.5) | IT Lead | 2027-03-31 |
| Access reviews for the EHR integration (A.5.18) | IT Lead | Next quarterly cycle |

## 8. Decisions and trade-offs
I prioritized controls protecting patient data first and left SSO for non-PHI apps until later.
