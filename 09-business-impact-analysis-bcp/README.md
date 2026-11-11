# 09 · Business Impact Analysis & Continuity Plan

> Brightline Health is fictional; process-owner interviews and the restore test are simulated.

## 1. Why I built this
The [internal audit](../07-internal-audit/) found one High-severity gap: **no business continuity plan**. That would likely fail the ISO 27001 certification audit. This project carries that finding all the way through to closure.

## 2. What I built
| File | What it is |
|---|---|
| [BIA_Brightline.xlsx](BIA_Brightline.xlsx) | 8 business processes ranked by impact, with recovery time (RTO) and data-loss (RPO) targets, and tested results (met/missed is a formula) |
| [Business_Continuity_Plan.md](Business_Continuity_Plan.md) | Plan built from the BIA: priorities, activation, strategies per scenario, security during disruption, communications, testing |

## 3. Explain
A BIA asks each part of the business: if this stops, what breaks, and how long can we survive? The answers set recovery targets. The continuity plan is then built to meet them, and testing shows whether it does.

## 4. What was broken
- No business continuity plan and no agreed recovery times (ISO 27001 A.5.29; HIPAA contingency plan requirement).
- Backups ran daily but a restore had **never been tested**, so nobody knew whether 4 hours was realistic.

## 5. What was fixed
- BIA completed with owners of all 8 processes; 2 rated Critical (scheduling, telehealth).
- Continuity plan written; executive approval scheduled for 2026-12-15.
- First restore test (simulated, in a staging copy): scheduling recovered in **2 hours 40 minutes** against a 4-hour target. 3 of 4 tested processes met their target.

## 6. Business impact
- Closes the major nonconformity blocking ISO 27001 certification, and the HIPAA contingency-plan gap.
- Clinics now have a committed recovery time for scheduling, which can go into customer contracts.
- Spend is focused where downtime hurts patients (scheduling, telehealth), not spread evenly.

## 7. Remediation still open
| Item | Owner | Target |
|---|---|---|
| Billing missed its 24-hour target (30 hours): automate the billing service rebuild | Engineering Lead | 2027-03-31 |
| Test telehealth, Microsoft 365 and support recovery | IT Lead | 2027-Q2 |
| First annual BCP tabletop | COO | 2027-Q2 |

## 8. Decisions and trade-offs
- **Different targets for different processes:** scheduling 4 hours, analytics 72 hours. Clinics can't run without scheduling, but can wait for reports. Treating everything as critical would multiply cost.
- **No second active region yet:** restore-from-backup meets the 4-hour target at a fraction of the cost of running two regions all the time. Revisit if the target drops below 4 hours.
