#!/usr/bin/env bash
# Remove NSG rules that allow 22/3389/* inbound from the internet. Dry run by default (APPLY=1 to change).
# Replace access with Azure Bastion or Defender for Cloud Just-In-Time VM access BEFORE applying.
set -euo pipefail
APPLY=${APPLY:-0}
az graph query -q "Resources | where type =~ 'microsoft.network/networksecuritygroups' | mv-expand r = properties.securityRules
 | where tostring(r.properties.access) =~ 'Allow' and tostring(r.properties.direction) =~ 'Inbound'
 | where tostring(r.properties.sourceAddressPrefix) in~ ('*','0.0.0.0/0','Internet','Any')
 | where tostring(r.properties.destinationPortRange) in ('22','3389','*')
 | project nsg=name, resourceGroup, rule=tostring(r.name)" --first 1000 --query "data[].[nsg,resourceGroup,rule]" -o tsv |
while IFS=$'\t' read -r nsg rg rule; do
  echo "Open management rule: $nsg / $rule ($rg)"
  if [[ "$APPLY" == "1" ]]; then
    az network nsg rule delete -g "$rg" --nsg-name "$nsg" -n "$rule"; echo "  deleted"
  fi
done
if [[ "$APPLY" != "1" ]]; then echo "Dry run only."; fi
