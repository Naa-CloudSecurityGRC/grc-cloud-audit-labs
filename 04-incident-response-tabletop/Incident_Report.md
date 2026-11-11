# Incident Report: INC-0412 (Tabletop)

| Field | Detail |
|---|---|
| Incident ID | INC-0412 (simulated) |
| Type | Phishing → Microsoft 365 account takeover → PHI exfiltration |
| Severity | SEV-1 (raised from SEV-2) |
| Detected / declared / contained | Tue 08:40 (user report) / Tue 09:25 / Tue 10:30 |
| Dwell time | ~23 hours from compromise to detection |
| Systems | 1 Microsoft 365 mailbox; Support SharePoint site |
| Data | 9 files with PHI (names, dates of birth, referral reasons) for 38 patients |
| Root cause | AiTM phishing stole a session token, bypassing push MFA; no alerting on mailbox forwarding rules |
| Notification | Breach of unsecured PHI. As business associate, Brightline notified the 3 affected clinics within 5 days (BAA requires 10). The clinics delegated patient letters to Brightline: 38 patients notified; clinics log it for their annual HHS submission (< 500 individuals). |

## Response summary
Account disabled, sessions revoked, forwarding rule removed, phishing email purged from 7 mailboxes, staff warned. Forensic review confirmed no other accounts were compromised.

## Corrective actions
| # | Action | Owner | Due | Status |
|---|---|---|---|---|
| 1 | Alert on external forwarding rules; block auto-forwarding to external domains by default | IT Lead | 2026-11-01 | Done |
| 2 | Add "revoke sessions and refresh tokens" to the account-compromise runbook | Incident Lead | 2026-10-28 | Done |
| 3 | Name the Privacy Officer as owner of breach-notification decisions in the IR plan | CISO | 2026-10-28 | Done (plan v1.1) |
| 4 | Conditional access: require compliant (managed) device for Microsoft 365 | IT Lead | 2026-11-15 | Done |
| 5 | Phishing-resistant MFA (FIDO2 security keys) for admins and support staff | IT Lead | 2027-01-31 | In progress |
| 6 | Train help desk to treat odd mailbox behavior as a potential incident | IT Lead | 2026-11-30 | In progress |
| 7 | Remove standing PHI from the Support SharePoint site; store in EHR-integrated tool | Support Manager | 2026-12-31 | In progress |
