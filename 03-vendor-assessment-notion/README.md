# 03 · Third-Party Vendor Assessment: Notion (real public documentation)

> Brightline Health is fictional. The vendor answers come only from Notion's public security page ([notion.com/security](https://www.notion.com/security), accessed 2026-11-10); anything not stated there is marked "Not documented".

## 1. Why I built this
To assess a real vendor from public evidence, the way TPRM teams do before onboarding.

## 2. What I built
- A 32-question vendor security questionnaire in 5 sections: Governance, Access Control, Data Protection, Incident Response, Compliance.
- Scoring model: Yes = 2, Partial = 1, No / Not documented = 0, with section scores and a risk level (formulas).
- Completed the questionnaire for Notion from public evidence, plus a scorecard and a one-page [Vendor Assessment Report](Vendor_Assessment_Report.md).

| File | What it is |
|---|---|
| [Vendor_Assessment_Notion.xlsx](Vendor_Assessment_Notion.xlsx) | Questionnaire with evidence and follow-ups; scorecard |
| [Vendor_Assessment_Report.md](Vendor_Assessment_Report.md) | Strengths, weaknesses, risk level, recommendations |

## 3. Explain
Every SaaS tool a company adopts becomes part of its attack surface. A vendor assessment checks, before and during the relationship, whether the vendor protects the data well enough, and whether the contract (for healthcare, a HIPAA Business Associate Agreement) covers it.

## 4. What was broken
- Notion was adopted by teams without any assessment.
- A search found **PHI in 14 Notion pages**: support runbooks with pasted patient names and appointment details.
- Brightline was on the **Business plan**, which has no HIPAA BAA, no enforced SAML SSO and no SCIM. Storing PHI there was a HIPAA compliance gap.

## 5. What was fixed
| Problem | Fix |
|---|---|
| PHI in a tool with no BAA | Upgraded to Enterprise and signed Notion's BAA; PHI pages moved to the EHR-integrated support tool and deleted from Notion |
| Password logins; leavers kept access | Enforced SAML SSO through Microsoft Entra ID; turned on SCIM deprovisioning |
| Public sharing allowed | Enterprise policy disables public page sharing and restricts guests |
| Unknowns (breach notice, deletion, SLA) | Added 72-hour breach notice and certified deletion to the contract / BAA; requested SOC 2 Type II report |

## 6. Business impact
- Closed a HIPAA gap: PHI is no longer held by a vendor without a BAA.
- Leavers now lose Notion access automatically when removed from Entra ID.
- The questionnaire is reusable: it is now the standard intake for every new SaaS tool, starting with the other 3 PHI vendors.

## 7. Remediation still open
| Item | Owner | Target |
|---|---|---|
| Review Notion's SOC 2 Type II report exceptions and CUECs | GRC | 2026-12-15 |
| Quarterly search for PHI in Notion (DLP rule) | Privacy Officer | Quarterly |
| Assess the remaining 3 PHI vendors with the same questionnaire | Operations Manager | 2027-01-31 |


## 8. Decisions and trade-offs
I scored 'not publicly documented' as zero and listed it as a follow-up, instead of assuming the vendor does it.

Source: [Notion security](https://www.notion.com/security).
