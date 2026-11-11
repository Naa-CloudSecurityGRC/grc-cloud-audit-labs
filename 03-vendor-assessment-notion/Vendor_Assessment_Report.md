# Vendor Assessment Report: Notion

| | |
|---|---|
| Vendor | Notion Labs, Inc.: collaborative workspace / wiki |
| Customer | Brightline Health (fictional): 60 users, internal wiki and runbooks |
| Data involved | Internal procedures; **PHI found in 14 pages** (patient names and appointment details pasted into support runbooks) |
| Sources | Notion's public security page, [notion.com/security](https://www.notion.com/security), accessed 2026-11-10. No vendor contact or non-public reports used. |
| Assessor / date | Naa Aboagye (portfolio project) / 2026-11-10 |

## Result
**Score: 57 / 64 (89%).** Strong public security posture: SOC 2 and ISO 27001 audits, ISO 27701/27018, AES-256 at rest, TLS 1.2+, annual pen tests, bug bounty, cross-region backups, and customer data excluded from AI training.

**Risk level depends on the plan:**
- **Enterprise plan with a signed BAA: Low.**
- **Brightline's original Business plan with PHI present: High.** Notion offers a HIPAA Business Associate Agreement, SAML SSO enforcement, SCIM and retention controls only on Enterprise. Without a BAA, PHI must not be stored there.

## Scorecard
| Section | Score | Notes |
|---|---:|---|
| Governance | 13/14 | SOC 2 report type and period not stated publicly |
| Access Control | 12/12 | SAML enforcement and SCIM need Enterprise |
| Data Protection | 14/16 | Data deletion at contract end not documented |
| Incident Response | 8/12 | Breach-notification timeframe and uptime SLA not documented |
| Compliance | 10/10 | BAA on Enterprise only |

## Strengths
- Independent audits (SOC 2, ISO 27001, ISO 27701, ISO 27018) with reports on the Trust Center.
- Strong encryption, customer-managed keys and data residency options.
- Clear statement that customer data is not used to train AI models.

## Weaknesses and unknowns
1. HIPAA BAA, SAML enforcement, SCIM and retention policies are **Enterprise-only**.
2. No public breach-notification timeframe.
3. No public uptime SLA.
4. Data deletion and certification at contract end not described.

## Recommendations
1. **Upgrade to Enterprise and sign the BAA before any PHI stays in Notion**, or remove PHI and block it by policy.
2. Request the SOC 2 Type II report and bridge letter from the Trust Center; review exceptions and CUECs.
3. Put a breach-notification timeframe (72 hours) and data deletion with certification into the contract / BAA.
4. Enforce SAML SSO and turn on SCIM so leavers lose access automatically.
5. Reassess annually.
