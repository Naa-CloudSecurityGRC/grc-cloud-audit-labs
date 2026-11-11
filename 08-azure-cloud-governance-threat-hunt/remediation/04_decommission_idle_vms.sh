#!/usr/bin/env bash
# Decommission deallocated VMs idle > 45 days, from the audit output, after owner sign-off.
# Input: CSV with columns vm,resourceGroup,ownerApproved (yes/no). Dry run by default.
set -euo pipefail
APPLY=${APPLY:-0}; LIST=${1:-idle_vms_approved.csv}
tail -n +2 "$LIST" | while IFS=, read -r vm rg approved; do
  [[ "$approved" == "yes" ]] || { echo "Skip $vm (no owner approval)"; continue; }
  echo "Decommission: $vm ($rg)"
  if [[ "$APPLY" == "1" ]]; then
    osdisk=$(az vm show -g "$rg" -n "$vm" --query storageProfile.osDisk.managedDisk.id -o tsv)
    az snapshot create -g "$rg" -n "${vm}-final-snap" --source "$osdisk" --sku Standard_LRS -o none
    az vm delete -g "$rg" -n "$vm" --yes
    az disk delete --ids "$osdisk" --yes --no-wait
  fi
done
