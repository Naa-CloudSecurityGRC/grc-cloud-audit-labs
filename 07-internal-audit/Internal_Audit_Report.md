# Internal Audit Report: ISO/IEC 27001 Readiness

| | |
|---|---|
| Organization | Brightline Health (fictional) |
| Audit period | 2026-11-03 to 2026-11-06 |
| Scope | 10 of 20 Annex A controls in the compliance program, chosen for PHI risk |
| Auditor | Naa Aboagye (independent of control owners; portfolio project) |
| Criteria | ISO/IEC 27001:2022 Annex A; Brightline policies |
| Workpapers | [Internal_Audit_Workbook.xlsx](Internal_Audit_Workbook.xlsx) |

## 1. Overall conclusion
**Not yet ready for the certification audit.** 5 controls are compliant, 4 partially implemented and 1 non-compliant. The non-compliance (no business continuity plan) would likely be a **major nonconformity** in a certification audit and must be fixed first. Readiness can be reached in about 90 days if the corrective action plan holds.

| Result | Controls |
|---|---:|
| Compliant | 5 |
| Partially implemented | 4 |
| Non-compliant | 1 |

## 2. Key findings

**High: A.5.29 No business continuity plan.** No plan exists for keeping security in place during an outage or disaster. A certification auditor would expect one, and HIPAA requires a contingency plan (164.308(a)(7)).

**Medium: A.8.8 Critical vulnerabilities past SLA.** 3 critical container vulnerabilities have been open 22-41 days against a 15-day SLA. The self-assessment had marked this control "Implemented".

**Medium: A.8.13 Backups never restore-tested.** Backups run daily, but no restore has been tested. Also marked "Implemented" in the self-assessment.

**Medium: A.5.18 Access review incomplete.** The EHR integration was left out of the Q3 review, and 2 of 11 removals took 9 and 12 days (target 5).

**Medium: A.5.19 Vendor assessments incomplete.** 1 of 4 PHI vendors assessed. BAAs are now in place with all four.

**Low: A.6.3 Training.** Compliant; only one phishing simulation so far.

## 3. What went well
- MFA everywhere and SSO-only AWS access (A.5.17) were fully evidenced.
- The IR plan was approved and tested by tabletop, with corrective actions already closed (A.5.24).
- Logging meets the target: all regions, log validation, 1-year retention (A.8.15).

## 4. Lessons learned
1. **Self-assessments overstate.** Two controls marked "Implemented" (A.8.8, A.8.13) failed when tested. Status should only be "Implemented" when evidence of operation exists, not just configuration.
2. **Scope creep in reviews.** Systems added after the access-review procedure was written (the EHR integration) were missed. The system inventory should drive review scope automatically.
3. **Evidence was easy to collect where it was automated** (CloudTrail, IAM reports) and slow where it was manual (training records, vendor files).

## 5. Corrective action plan
| CAP | Control | Action | Owner | Due |
|---|---|---|---|---|
| CAP-01 | A.5.29 | Write, approve and test a BCP | COO | 2027-01-31 |
| CAP-02 | A.8.8 | Fix 3 overdue criticals; weekly SLA report | Engineering Lead | 2026-11-21 |
| CAP-03 | A.8.13 | First restore test with RTO/RPO recorded | Engineering Lead | 2026-12-15 |
| CAP-04 | A.5.18 | Add EHR integration to reviews; enforce 5-day removals | IT Lead | 2026-12-31 |
| CAP-05 | A.5.19 | Assess remaining 3 PHI vendors | Operations Manager | 2027-01-31 |
| CAP-06 | A.6.3 | Q1 phishing simulation | IT Lead | 2027-03-31 |

**Follow-up:** the auditor will re-test each CAP item after its due date. The control matrix status for A.8.8 and A.8.13 has been corrected to "Partially implemented".
