#!/usr/bin/env bash
# Disable anonymous blob access, require HTTPS and TLS 1.2 on all storage accounts. Dry run by default.
set -euo pipefail
APPLY=${APPLY:-0}
az graph query -q "Resources | where type =~ 'microsoft.storage/storageaccounts'
 | where tobool(properties.allowBlobPublicAccess) == true or tostring(properties.minimumTlsVersion) != 'TLS1_2' or tobool(properties.supportsHttpsTrafficOnly) == false
 | project name, resourceGroup" --first 1000 --query "data[].[name,resourceGroup]" -o tsv |
while IFS=$'\t' read -r name rg; do
  echo "Storage account to harden: $name ($rg)"
  if [[ "$APPLY" == "1" ]]; then
    az storage account update -n "$name" -g "$rg" --allow-blob-public-access false --https-only true --min-tls-version TLS1_2 -o none; echo "  hardened"
  fi
done
if [[ "$APPLY" != "1" ]]; then echo "Dry run only. Check apps that read public blobs first (move them to SAS tokens or a CDN with a private origin)."; fi
