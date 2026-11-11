# Business Continuity Plan (summary): Brightline Health

> Fictional company. Built from the [BIA](BIA_Brightline.xlsx).

| | |
|---|---|
| Owner | COO |
| Status | Draft for executive approval (target 2026-12-15) |
| Closes | Internal audit finding CAP-01 (ISO 27001 A.5.29); HIPAA contingency plan, 45 CFR 164.308(a)(7) |

## Recovery priorities (from the BIA)
| Priority | Process | RTO | RPO |
|---|---|---|---|
| 1 | Appointment scheduling | 4 hours | 15 minutes |
| 1 | Telehealth video visits | 4 hours | 15 minutes |
| 2 | Patient document upload | 8 hours | 1 hour |
| 2 | Microsoft 365 (email, Teams) | 8 hours | 4 hours |
| 3 | Billing and payments | 24 hours | 1 hour |
| 3 | Support desk | 24 hours | 4 hours |
| 4 | Analytics; payroll | 72 hours | 24 hours |

## Activation
The Incident Lead or COO declares a continuity event when a Priority 1 process is down, or is expected to be down, for more than 1 hour. The crisis team (CEO, COO, CISO, Engineering Lead, Privacy Officer) meets within 30 minutes.

## Strategies
| Scenario | Strategy |
|---|---|
| AWS region failure | Restore the database from cross-region backup into us-west-2; redeploy the app from infrastructure code |
| Ransomware / data corruption | Isolate; restore from immutable backups in the AWS Backup vault; follow the [IR plan](../04-incident-response-tabletop/IR_Plan.md) |
| Critical vendor outage (video, Stripe) | Clinics switch to phone visits / take payment later; status-page notice |
| Microsoft 365 outage | Out-of-band contact list and a Slack fallback channel for the crisis team |
| Loss of key staff | Runbooks for each Priority 1 system; two trained people per system |

## Security during disruption (ISO 27001 A.5.29)
Restored systems keep the same access controls, MFA and logging; no "temporary" admin accounts; every emergency change is logged and reviewed afterwards.

## Communications
Clinics via status page and email within 1 hour of activation; updates every 2 hours. HIPAA notification decisions follow the IR plan.

## Testing
Annual tabletop of this plan; quarterly database restore test; annual failover test of Priority 1 systems.
