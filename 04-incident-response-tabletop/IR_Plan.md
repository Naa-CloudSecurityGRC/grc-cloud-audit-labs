# Incident Response Plan: Brightline Health

| | |
|---|---|
| Version | 1.1 (updated after the November 2026 tabletop) |
| Owner | Fractional CISO |
| Applies to | All security incidents affecting Brightline systems, data (especially PHI) or vendors holding Brightline data |

> Brightline Health is fictional.

## 1. Purpose
Detect, contain and recover from security incidents quickly, protect patient data, and meet HIPAA business-associate and contractual notification deadlines.

## 2. Roles
| Role | Who | Responsibilities |
|---|---|---|
| Incident Lead | On-call engineer (week rotation); CISO for SEV-1 | Runs the response, sets severity, keeps the timeline |
| Technical responders | Engineering and IT | Investigate, contain, eradicate, recover |
| Privacy Officer | Privacy Officer | **Decides whether PHI was breached and who must be notified** (added after tabletop) |
| Communications | COO | Clinic and patient messages; regulator and media contact via counsel |
| Executive sponsor | CEO | Approves external notices and spending |
| Outside counsel / forensics | Retainer firms | Privilege, forensics, regulator advice |

## 3. Severity
| Level | Example | Response |
|---|---|---|
| SEV-1 | Confirmed PHI exposure; production down | Incident Lead + CISO within 15 min; CEO within 1 hour |
| SEV-2 | Compromised account with possible PHI access | Within 1 hour |
| SEV-3 | Malware contained on one laptop, no data access | Within 4 hours |
| SEV-4 | Policy violation, suspicious email reported | Next business day |

## 4. Detection
Sources: Microsoft 365 Defender and Entra ID risky sign-in alerts, AWS GuardDuty, CloudTrail anomalies, employee reports (report-phishing button, #security channel), vendor and clinic notices. Anyone can declare an incident.

## 5. Containment
- **Accounts:** disable the user, **revoke all sessions and refresh tokens**, reset password and MFA methods, remove malicious inbox rules and OAuth app grants.
- **Hosts:** isolate with EDR; preserve memory and disk images before wiping.
- **Cloud:** disable access keys, apply deny policies, snapshot affected resources.

## 6. Eradication
Remove persistence (inbox rules, app consents, new MFA methods, IAM keys), patch the entry point, and hunt for the same indicators across all users.

## 7. Recovery
Restore access with fresh credentials and compliant devices; monitor the account and related systems closely for 14 days.

## 8. Notification decisions (HIPAA)
- Brightline is a **business associate** of its clinic customers (the covered entities).
- The Privacy Officer runs the HIPAA 4-factor risk assessment (nature of the PHI, who received it, whether it was actually viewed or acquired, mitigation).
- If a breach of unsecured PHI occurred, Brightline must notify each affected clinic **without unreasonable delay and no later than 60 days** after discovery (45 CFR 164.410). Most BAAs require faster notice; follow the shortest.
- The clinics notify patients and HHS (individuals within 60 days; HHS annually if under 500 people, within 60 days if 500 or more; media if more than 500 residents of one state), unless they delegate this to Brightline in writing.
- Also check state breach-notification laws.

## 9. Lessons learned
Post-incident review within 10 business days for SEV-1 and SEV-2: timeline, root cause, what worked, what didn't, owners and dates for fixes. The plan is tested by tabletop at least annually.

## 10. Compliance mapping
| Plan section | ISO/IEC 27001:2022 | SOC 2 | HIPAA |
|---|---|---|---|
| Roles, severity, plan (2-3) | A.5.24 | CC7.3 | 164.308(a)(6)(i) |
| Detection (4) | A.6.8, A.8.16 | CC7.2 | 164.308(a)(1)(ii)(D) |
| Containment, eradication (5-6) | A.5.26 | CC7.4 | 164.308(a)(6)(ii) |
| Recovery (7) | A.5.26, A.5.29 | CC7.5 | 164.308(a)(7) |
| Evidence handling | A.5.28 | CC7.4 | |
| Notification (8) | A.5.26, A.5.31 | CC2.3, CC7.4 | 164.410 (and 164.404-408 for clinics) |
| Lessons learned (9) | A.5.27 | CC7.5 | 164.308(a)(6)(ii) |
