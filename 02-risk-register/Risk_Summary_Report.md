# Risk Summary Report: Top 3 Risks

**To:** CEO and security steering group · **From:** GRC · **Date:** 2026-11-06 · Brightline Health (fictional)

**Bottom line:** 12 risks assessed. Before treatment, 4 were High and 8 Medium. After the controls below, none are High, 2 are Medium and 10 are Low; total risk score fell 57% (151 → 65). Three risks drove most of the exposure.

## 1. Phishing leads to Microsoft 365 account takeover (R01): inherent 20, High → residual 9, Medium
- **Why it ranked first:** staff receive targeted phishing weekly, and PHI is sometimes shared in email.
- **Treatment:** MFA with number matching, conditional access blocking legacy sign-in, alerts on new mail-forwarding rules, quarterly phishing simulations.
- **Why still Medium:** phishing will keep getting through; the residual risk depends on staff reporting quickly. Tested in the [IR tabletop](../04-incident-response-tabletop/).

## 2. Former staff keep access to PHI systems (R05): inherent 16, High → residual 6, Low
- **Why it ranked high:** no access review had ever been done; contractors were offboarded by email request.
- **Treatment:** HR-triggered offboarding and quarterly access reviews (first review removed 11 stale accounts).

## 3. Stolen AWS credentials / public S3 bucket (R02, R03): inherent 15 each, High → residual 5 each, Low
- **Why they ranked high:** AWS root and 3 IAM users had no MFA, and one S3 bucket lacked Block Public Access.
- **Treatment:** MFA everywhere, IAM users replaced with SSO roles, account-level Block Public Access, AWS Config rules. Evidence in [project 05](../05-soc2-aws-control-mapping/).

## Decisions requested
1. Accept residual Medium risk on R01 and R06 (vendor breach), reviewed quarterly.
2. Fund an email security add-on (~$4/user/month) to reduce R01 further.
