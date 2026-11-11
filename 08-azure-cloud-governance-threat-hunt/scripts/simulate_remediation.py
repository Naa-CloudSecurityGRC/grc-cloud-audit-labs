"""Apply the approved remediation to the SIMULATED inventory, producing the 'after' state used to verify the fixes.
Decisions mirror the remediation plan: 3 disks and 3 idle VMs kept at owners' request (tagged Keep/ExpirationDate)."""
import json, copy, datetime as dt, os
B=os.path.join(os.path.dirname(__file__),"..","data")
inv=json.load(open(os.path.join(B,"resource_inventory_before.json"))); R=inv["data"]; SNAP=dt.date(2026,11,2)
out=[]; kept_disks=0; kept_vms=0
idle=[r for r in R if r["type"]=="microsoft.compute/virtualmachines" and r["properties"]["extended"]["instanceView"]["powerState"]["code"]=="PowerState/deallocated" and (SNAP-dt.date.fromisoformat(r["properties"]["lastActivityDate"])).days>45]
keep_vm={r["name"] for r in idle[:3]}; drop_vm={r["name"] for r in idle[3:]}
for r in R:
    r=copy.deepcopy(r); t=r["type"]
    if t=="microsoft.compute/disks" and r["properties"]["diskState"]=="Unattached":
        if kept_disks<3: kept_disks+=1; r["tags"].update({"Owner":"data@carebridge.example","ExpirationDate":"2027-01-31","Keep":"true"}); r["properties"]["diskState"]="Unattached"
        else: continue
    if t=="microsoft.compute/virtualmachines" and r["name"] in drop_vm: continue
    if t=="microsoft.compute/disks" and r["name"].replace("-osdisk","") in drop_vm: continue
    if t=="microsoft.compute/virtualmachines" and r["name"] in keep_vm: r["tags"].update({"Owner":"it-ops@carebridge.example","ExpirationDate":"2026-12-31"})
    if t=="microsoft.network/networksecuritygroups":
        r["properties"]["securityRules"]=[x for x in r["properties"]["securityRules"] if not (x["properties"]["sourceAddressPrefix"] in ("*","Internet","0.0.0.0/0") and x["properties"]["destinationPortRange"] in ("22","3389","*"))]
    if t=="microsoft.storage/storageaccounts":
        r["properties"].update({"allowBlobPublicAccess":False,"minimumTlsVersion":"TLS1_2","supportsHttpsTrafficOnly":True})
    if r["name"]=="cb-legacy-rds01": r["properties"]["extended"]["instanceView"]["powerState"]["code"]="PowerState/deallocated"; r["properties"]["lastActivityDate"]="2026-11-01"; r["tags"].update({"Owner":"security@brightline.example","ExpirationDate":"2027-02-01","Hold":"forensics"})
    # tag inheritance policy remediation: resource groups now carry Owner/ExpirationDate
    r["tags"].setdefault("Owner","rg-owner@carebridge.example"); r["tags"].setdefault("ExpirationDate","2027-06-30")
    out.append(r)
os.makedirs(os.path.join(B,"after"),exist_ok=True)
json.dump({"generatedFor":inv["generatedFor"],"snapshotDate":"2026-11-30","data":out},open(os.path.join(B,"after","resource_inventory_after.json"),"w"),indent=1)
print(len(R),"->",len(out),"resources")
