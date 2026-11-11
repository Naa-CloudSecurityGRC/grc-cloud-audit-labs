"""Run the governance checks and threat hunt against an exported inventory.
Python equivalents of queries/01-08 so the audit can run offline on the simulated data.
Usage: python scripts/audit.py data/resource_inventory_before.json output/before"""
import json, csv, sys, os, datetime as dt, ipaddress
from collections import Counter, defaultdict
RFC1918 = [ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")]
is_internal = lambda ip: any(ipaddress.ip_address(ip) in n for n in RFC1918)  # same as KQL ipv4_is_private()
inv, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
R = json.load(open(inv))["data"]; SNAP = dt.date(2026, 11, 2)
# Illustrative monthly prices (USD) for planning only; confirm with the Azure Pricing Calculator.
DISK_PRICE = {"Standard_LRS": 0.045, "StandardSSD_LRS": 0.075, "Premium_LRS": 0.135}  # per GB-month, approximate
def w(name, rows, header):
    with open(os.path.join(out, name), "w", newline="") as f:
        c = csv.writer(f); c.writerow(header); c.writerows(rows)
    return len(rows)
S = {}
# 01 orphaned disks
od = [r for r in R if r["type"] == "microsoft.compute/disks" and r["properties"]["diskState"].lower() == "unattached"]
rows = [[r["subscriptionId"][-1], r["resourceGroup"], r["name"], r["sku"]["name"], r["properties"]["diskSizeGB"],
         round(r["properties"]["diskSizeGB"] * DISK_PRICE[r["sku"]["name"]], 2), r["tags"].get("Owner", "")] for r in od]
S["orphaned_disks"] = w("01_orphaned_disks.csv", rows, ["sub", "resourceGroup", "disk", "sku", "sizeGB", "estMonthlyUSD", "owner"])
S["orphaned_disk_gb"] = sum(r[4] for r in rows); S["orphaned_disk_usd_month"] = round(sum(r[5] for r in rows), 2)
# 02 deallocated VMs (+ inactivity > 45 days)
vm = [r for r in R if r["type"] == "microsoft.compute/virtualmachines"]
dv = [r for r in vm if r["properties"]["extended"]["instanceView"]["powerState"]["code"].lower() == "powerstate/deallocated"]
rows = []
for r in dv:
    idle = (SNAP - dt.date.fromisoformat(r["properties"]["lastActivityDate"])).days
    disk = next((d for d in R if d["type"] == "microsoft.compute/disks" and d["name"] == r["name"] + "-osdisk"), None)
    cost = round(disk["properties"]["diskSizeGB"] * DISK_PRICE[disk["sku"]["name"]], 2) if disk else 0
    rows.append([r["subscriptionId"][-1], r["resourceGroup"], r["name"], idle, "Yes" if idle > 45 else "No", cost, r["tags"].get("Owner", "")])
S["deallocated_vms"] = w("02_deallocated_vms.csv", rows, ["sub", "resourceGroup", "vm", "daysSinceActivity", "inactiveOver45d", "estDiskUSDmonth", "owner"])
S["deallocated_over45"] = sum(1 for r in rows if r[4] == "Yes"); S["deallocated_over45_usd_month"] = round(sum(r[5] for r in rows if r[4] == "Yes"), 2)
# 03 NSG open management ports
rows = []
for r in R:
    if r["type"] != "microsoft.network/networksecuritygroups": continue
    for ru in r["properties"]["securityRules"]:
        p = ru["properties"]
        if p["access"] == "Allow" and p["direction"] == "Inbound" and p["sourceAddressPrefix"] in ("*", "0.0.0.0/0", "Internet", "Any") and p["destinationPortRange"] in ("22", "3389", "*"):
            rows.append([r["subscriptionId"][-1], r["resourceGroup"], r["name"], ru["name"], p["sourceAddressPrefix"], p["destinationPortRange"]])
S["open_mgmt_rules"] = w("03_nsg_open_management_ports.csv", rows, ["sub", "resourceGroup", "nsg", "rule", "source", "port"])
S["open_rdp"] = sum(1 for r in rows if r[5] == "3389"); S["open_ssh"] = sum(1 for r in rows if r[5] == "22"); S["open_all"] = sum(1 for r in rows if r[5] == "*")
# 04 storage
rows = [[r["subscriptionId"][-1], r["name"], r["properties"]["allowBlobPublicAccess"], r["properties"]["minimumTlsVersion"], r["properties"]["supportsHttpsTrafficOnly"]]
        for r in R if r["type"] == "microsoft.storage/storageaccounts" and (r["properties"]["allowBlobPublicAccess"] or r["properties"]["minimumTlsVersion"] in ("TLS1_0", "TLS1_1") or not r["properties"]["supportsHttpsTrafficOnly"])]
S["storage_issues"] = w("04_storage_findings.csv", rows, ["sub", "account", "allowBlobPublicAccess", "minimumTls", "httpsOnly"])
S["storage_public"] = sum(1 for r in rows if r[2]); S["storage_weak_tls"] = sum(1 for r in rows if r[3] in ("TLS1_0", "TLS1_1")); S["storage_http"] = sum(1 for r in rows if not r[4])
# 05 tags
miss = Counter(r["type"] for r in R if not r["tags"].get("Owner") or not r["tags"].get("ExpirationDate"))
S["untagged"] = sum(miss.values()); S["total_resources"] = len(R)
w("05_missing_tags.csv", sorted(miss.items(), key=lambda x: -x[1]), ["type", "missingOwnerOrExpiration"])
# 07/08 threat hunt
fails = defaultdict(lambda: {"n": 0, "acct": set(), "host": set(), "first": None, "last": None}); events = []
ev_path = os.path.join(os.path.dirname(inv), "security_events.csv")
if os.path.exists(ev_path):
    for e in csv.DictReader(open(ev_path)):
        events.append(e)
        if e["EventID"] == "4625" and not is_internal(e["IpAddress"]):
            f = fails[e["IpAddress"]]; f["n"] += 1; f["acct"].add(e["TargetAccount"]); f["host"].add(e["Computer"])
            f["first"] = min(f["first"] or e["TimeGenerated"], e["TimeGenerated"]); f["last"] = max(f["last"] or e["TimeGenerated"], e["TimeGenerated"])
    bad = {ip: f for ip, f in fails.items() if f["n"] > 50}
    S["bruteforce_ips"] = w("07_bruteforce_sources.csv", [[ip, f["n"], len(f["acct"]), ";".join(sorted(f["host"])), f["first"], f["last"]] for ip, f in sorted(bad.items(), key=lambda x: -x[1]["n"])],
                            ["IpAddress", "failures", "accountsTried", "hosts", "firstSeen", "lastSeen"])
    S["bruteforce_failures"] = sum(f["n"] for f in bad.values())
    hits = [[e["TimeGenerated"], e["Computer"], e["EventID"], e["TargetAccount"], e["IpAddress"]] for e in events if e["EventID"] in ("4624", "4720", "4732") and e["IpAddress"] in bad]
    S["compromise_events"] = w("08_success_after_failures.csv", hits, ["TimeGenerated", "Computer", "EventID", "TargetAccount", "IpAddress"])
json.dump(S, open(os.path.join(out, "summary.json"), "w"), indent=1)
print(json.dumps(S, indent=1))
