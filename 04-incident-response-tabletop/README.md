# 04 · Incident Response Plan + Tabletop Test

> Brightline Health and the incident are fictional; the exercise is a simulated tabletop.

## 1. Why I built this
An untested plan fails in the first hour; I wanted to show I can run and learn from a tabletop.

## 2. What I built
| File | What it is |
|---|---|
| [IR_Plan.md](IR_Plan.md) | Plan: purpose, roles, severity, detection, containment, eradication, recovery, HIPAA notification, lessons learned, and mapping to ISO 27001 Annex A, SOC 2 CC7.x and HIPAA |
| [Tabletop_Timeline.md](Tabletop_Timeline.md) | Scenario (adversary-in-the-middle phishing → Microsoft 365 takeover), minute-by-minute timeline with injects, and gaps exposed |
| [Incident_Report.md](Incident_Report.md) | Completed incident report with root cause, notification decision and corrective actions |

## 3. Explain
A plan that has never been tested usually fails in the first hour of a real incident. A tabletop walks the team through a realistic attack step by step, with surprise updates ("injects"), to find gaps while the stakes are low.

## 4. What was broken
The tabletop exposed 5 gaps:
1. No alert on external mail-forwarding rules → attacker undetected for **~23 hours**.
2. The first user report was handled as an IT ticket → **45 minutes** lost.
3. The runbook said "reset password" but not "revoke sessions" → attacker kept access **30 more minutes**.
4. Nobody owned the HIPAA breach-notification decision → **2.5 hours** of confusion.
5. Push MFA was bypassed by session-token theft.

## 5. What was fixed
- Alerting on forwarding rules, and external auto-forwarding blocked by default.
- Runbook now revokes sessions and refresh tokens on every account compromise.
- IR plan v1.1 names the Privacy Officer as the breach-notification decision owner.
- Conditional access requires a managed device for Microsoft 365, so stolen tokens can't be replayed from an attacker's machine.

## 6. Business impact
- Expected detection time for this attack falls from ~23 hours to minutes (the forwarding-rule alert fires at the attacker's second step).
- The HIPAA business-associate notification clock (60 days, shorter under most BAAs) is now managed by a named owner, reducing regulatory and contractual risk with clinic customers.
- Fewer PHI records at risk: PHI is moving out of SharePoint into the EHR-integrated tool.

## 7. Remediation still open
| Item | Owner | Target |
|---|---|---|
| Phishing-resistant MFA (FIDO2 keys) for admins and support staff | IT Lead | 2027-01-31 |
| Help desk training on spotting incidents | IT Lead | 2026-11-30 |
| Move standing PHI out of SharePoint | Support Manager | 2026-12-31 |
| Next tabletop: ransomware on a laptop (risk R04) | GRC | Q2 2027 |

## 8. Decisions and trade-offs
As a business associate, the company notifies the clinics, not patients directly; I built that into the plan.
