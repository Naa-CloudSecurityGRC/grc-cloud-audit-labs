# Tabletop Exercise: Phishing → Microsoft 365 Account Takeover

| | |
|---|---|
| Date / length | 2026-10-21, 2 hours (simulated) |
| Facilitator | GRC (Naa Aboagye, portfolio project) |
| Participants | CISO, Engineering Lead, IT Lead, Privacy Officer, COO, Support Manager |
| Scenario | A support agent enters credentials on an adversary-in-the-middle (AiTM) phishing page posing as a Microsoft sign-in. The attacker steals the session cookie (bypassing push MFA), creates an inbox rule forwarding mail with "referral" in the subject to an outside address, and downloads files from the Support SharePoint site. |

> Fictional company and simulated exercise. Times are the simulated incident clock.

## Incident timeline
| Time (ET) | Event / injected update | Action taken | Communication |
|---|---|---|---|
| Mon 09:12 | Agent clicks phishing link "Updated shift schedule" and signs in | (none: not yet known) | |
| Mon 09:14 | Sign-in from a new country using a stolen session token | (none: no alert configured for token replay) | |
| Mon 09:31 | Attacker creates inbox rule forwarding "referral" emails to an external address | (none: **no alert on forwarding rules**) | |
| Mon 10:05 | Attacker downloads 22 files from Support SharePoint site | (none) | |
| Tue 08:40 | Agent reports odd "sent" items to #it-help | IT Lead looks into it as a mailbox problem, not an incident | IT replies in thread |
| Tue 09:25 | IT finds the external forwarding rule | IT Lead declares **SEV-2**; Incident Lead assigned | #inc-0412 channel opened |
| Tue 09:40 | | Password reset and MFA re-registration | |
| Tue 10:10 | Inject: attacker still reading mail | Team realizes a password reset **does not revoke existing sessions**; sessions and refresh tokens revoked | |
| Tue 10:30 | | Inbox rule removed; OAuth app grants checked (none); same sender searched and purged from 7 other mailboxes | Phishing warning sent to all staff |
| Tue 11:15 | Audit log shows 22 SharePoint files accessed, 9 containing PHI for **38 patients** | Severity raised to **SEV-1**; CISO and CEO joined | Exec update |
| Tue 11:30 | Inject: who decides if this is a reportable breach? | **No one owned this decision** in the plan; Privacy Officer takes it on | |
| Tue 14:00 | | HIPAA 4-factor assessment: PHI viewed and exfiltrated, cannot rule out compromise → **breach of unsecured PHI** | Outside counsel engaged |
| Wed 10:00 | | Conditional access policy drafted: require compliant device for Microsoft 365 (blocks stolen-token replay from unmanaged devices) | |
| Day 5 | | 3 affected clinics (covered entities) notified under their BAAs; clinics ask Brightline to send the 38 patient letters | Clinic notice |
| Day 12 | | Post-incident review held | Report circulated |

## What the exercise exposed
| # | Gap | Effect |
|---|---|---|
| 1 | No alert on external mail-forwarding rules | Attacker went undetected for ~23 hours |
| 2 | First report treated as an IT ticket, not an incident | 45 minutes lost before declaring |
| 3 | Runbook said "reset password" only; sessions stayed live | Attacker kept access for 30 more minutes |
| 4 | No owner for the breach-notification decision | 2.5 hours of confusion during SEV-1 |
| 5 | Push MFA can be bypassed by token theft | MFA alone did not stop the attack |
