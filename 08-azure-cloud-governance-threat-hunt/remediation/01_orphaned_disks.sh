#!/usr/bin/env bash
# Snapshot, then delete unattached managed disks. Dry run by default; set APPLY=1 to make changes.
# Requires: az login, az extension add --name resource-graph
set -euo pipefail
APPLY=${APPLY:-0}
az graph query -q "Resources | where type =~ 'microsoft.compute/disks' and tostring(properties.diskState) =~ 'Unattached' | project id, name, resourceGroup, keep=tostring(tags['Keep'])" \
  --first 1000 --query "data[?keep!='true'].[id,name,resourceGroup]" -o tsv |
while IFS=$'\t' read -r id name rg; do
  echo "Orphaned disk: $name ($rg)"
  if [[ "$APPLY" == "1" ]]; then
    az snapshot create -g "$rg" -n "${name}-final-snap" --source "$id" --sku Standard_LRS --tags Purpose=pre-delete DeleteAfterDays=90 -o none
    az disk delete --ids "$id" --yes --no-wait
    echo "  snapshot taken, delete submitted"
  fi
done
if [[ "$APPLY" != "1" ]]; then echo "Dry run only. Re-run with APPLY=1 after owner sign-off."; fi
