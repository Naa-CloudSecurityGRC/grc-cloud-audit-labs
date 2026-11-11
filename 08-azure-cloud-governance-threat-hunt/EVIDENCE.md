# Evidence: Azure Cloud Governance & Threat Hunt

Inventory → findings → intrusion found → contained → fixed → re-audited → prevented.

> Screenshots are taken from the files in this repository. Data is fictional or simulated.

## Step 1 · Built: Resource Graph query

KQL used to find NSG rules open to the internet (same logic runs offline in scripts/audit.py).

![Resource Graph query](evidence/01_built.png)

## Step 2 · Broken: exposed management ports

20 rules allow SSH, RDP or all ports from the internet.

![exposed management ports](evidence/02_broken.png)

## Step 3 · Broken: threat hunt: brute force

14,100 failed RDP logons in 6 days from 3 internet IPs.

![threat hunt: brute force](evidence/03_broken.png)

## Step 4 · Broken: threat hunt: successful intrusion

Successful logon from the top attacking IP, then a new local admin account 6 minutes later.

![threat hunt: successful intrusion](evidence/04_broken.png)

## Step 5 · Fixed: preventive policy

Azure Policy that denies new internet-exposed SSH/RDP rules.

![preventive policy](evidence/05_fixed.png)

## Step 6 · Verified: re-audit after remediation

Audit re-run on the remediated state.

![re-audit after remediation](evidence/06_verified.png)

## Step 7 · Verified: before vs after

Findings before and after remediation.

![before vs after](evidence/07_verified.png)
