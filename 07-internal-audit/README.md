# 07 · Mock Internal Audit (ISO 27001 Readiness)

**Evidence:** [step-by-step screenshots from build to remediation](EVIDENCE.md)

> Brightline Health is fictional; the audit uses simulated evidence.

## 1. Why I built this
To show I can audit independently: test with evidence and report clearly.

## 2. What I built
| File | What it is |
|---|---|
| [Internal_Audit_Workbook.xlsx](Internal_Audit_Workbook.xlsx) | Audit checklist for 10 controls (test procedure, evidence, status, finding, severity, remediation), corrective action plan, summary |
| [Internal_Audit_Report.md](Internal_Audit_Report.md) | 2-page report: conclusion, findings, what went well, lessons learned, CAP |

## 3. Explain
Before paying for a certification audit, companies run an internal audit: someone independent of the control owners tests whether controls actually work, using evidence. It finds problems while they're still cheap to fix.

## 4. What was broken
- **1 non-compliant control:** no business continuity plan (A.5.29), likely a major nonconformity.
- **4 partially implemented:** overdue critical vulnerabilities, backups never restore-tested, an incomplete access review, and 3 PHI vendors not yet assessed.
- **The self-assessment was wrong on 2 controls** (A.8.8, A.8.13): marked "Implemented" but failed testing.

## 5. What was fixed
- Control matrix corrected so leadership sees the true status.
- 6 corrective actions created with owners and dates; CAP-02 (overdue vulnerabilities) already in progress.
- Rule adopted: a control is "Implemented" only with evidence that it operates.

## 6. Business impact
- Avoided a likely failed certification audit (and its cost and delay) by finding the BCP gap first.
- Leadership now knows the realistic certification timeline: about 90 days after the CAP closes.
- Fixing the restore-test and vulnerability gaps directly lowers the chance of a long outage or a breach through a known flaw.

## 7. Remediation still open
All 6 CAP items, tracked in the workbook (CAP tab) and on the [compliance dashboard](../06-compliance-dashboard/). The High finding (no BCP) is being closed in [project 09](../09-business-impact-analysis-bcp/). Re-test after each due date.

## 8. Decisions and trade-offs
I rated the missing BCP 'High' (major nonconformity) and recommended delaying the certification audit rather than risking a failure.
