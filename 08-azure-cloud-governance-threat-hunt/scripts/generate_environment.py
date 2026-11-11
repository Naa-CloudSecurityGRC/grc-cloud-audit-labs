"""Generate a SIMULATED Azure environment for CareBridge Telehealth (fictional).
Output mirrors the shape of an Azure Resource Graph export and a Log Analytics SecurityEvent export.
Attacker IPs use RFC 5737 documentation ranges. Fixed seed: reproducible."""
import json, random, csv, datetime as dt, os
random.seed(2026)
OUT=os.path.join(os.path.dirname(__file__),"..","data")
subs={"sub-carebridge-prod":"11111111-aaaa-4000-8000-000000000001","sub-carebridge-dev":"11111111-aaaa-4000-8000-000000000002","sub-carebridge-labs":"11111111-aaaa-4000-8000-000000000003"}
locs=["eastus","eastus2","centralus"]
res=[]
def rid(sub,rg,prov,name): return f"/subscriptions/{subs[sub]}/resourceGroups/{rg}/providers/{prov}/{name}"
def tags(p_missing):
    t={"Environment":random.choice(["prod","dev","lab"])}
    if random.random()>p_missing: t["Owner"]=random.choice(["it-ops@carebridge.example","dev-team@carebridge.example","data@carebridge.example"])
    if random.random()>p_missing+0.2: t["ExpirationDate"]="2027-06-30"
    return t
vms=[]
for i in range(96):
    sub=random.choice(list(subs)); rg=f"rg-{sub.split('-')[-1]}-{random.choice(['app','data','legacy','sandbox'])}"
    state="PowerState/deallocated" if (sub=="sub-carebridge-labs" and random.random()<0.7) or random.random()<0.12 else "PowerState/running"
    name=f"cb-{sub.split('-')[-1]}-vm{i:02d}"
    last=(dt.date(2026,11,1)-dt.timedelta(days=random.randint(1,40) if state.endswith("running") else random.randint(10,220))).isoformat()
    vms.append(name)
    res.append({"id":rid(sub,rg,"Microsoft.Compute/virtualMachines",name),"name":name,"type":"microsoft.compute/virtualmachines","location":random.choice(locs),"resourceGroup":rg,"subscriptionId":subs[sub],
      "tags":tags(0.45),"properties":{"hardwareProfile":{"vmSize":random.choice(["Standard_B2s","Standard_D2s_v5","Standard_D4s_v5"])},"storageProfile":{"osDisk":{"name":f"{name}-osdisk"}},
      "extended":{"instanceView":{"powerState":{"code":state}}},"lastActivityDate":last}})
    res.append({"id":rid(sub,rg,"Microsoft.Compute/disks",f"{name}-osdisk"),"name":f"{name}-osdisk","type":"microsoft.compute/disks","location":res[-1]["location"],"resourceGroup":rg,"subscriptionId":subs[sub],
      "tags":res[-1]["tags"],"sku":{"name":random.choice(["Standard_LRS","StandardSSD_LRS","Premium_LRS"])},"properties":{"diskSizeGB":127,"diskState":"Reserved" if state.endswith("deallocated") else "Attached","timeCreated":"2025-03-01T00:00:00Z"}})
# legacy RDS host (the threat-hunt target)
res.append({"id":rid("sub-carebridge-prod","rg-prod-legacy","Microsoft.Compute/virtualMachines","cb-legacy-rds01"),"name":"cb-legacy-rds01","type":"microsoft.compute/virtualmachines","location":"eastus","resourceGroup":"rg-prod-legacy","subscriptionId":subs["sub-carebridge-prod"],
  "tags":{"Environment":"prod"},"properties":{"hardwareProfile":{"vmSize":"Standard_D4s_v5"},"extended":{"instanceView":{"powerState":{"code":"PowerState/running"}}},"lastActivityDate":"2026-10-31"}})
# orphaned disks
for i in range(21):
    sub=random.choice(list(subs)); rg=f"rg-{sub.split('-')[-1]}-{random.choice(['app','legacy','sandbox'])}"
    sku=random.choice(["Standard_LRS"]*3+["StandardSSD_LRS","Premium_LRS"]); size=random.choice([127,127,127,256,512,1024])
    res.append({"id":rid(sub,rg,"Microsoft.Compute/disks",f"cb-orphan-disk{i:02d}"),"name":f"cb-orphan-disk{i:02d}","type":"microsoft.compute/disks","location":random.choice(locs),"resourceGroup":rg,"subscriptionId":subs[sub],
      "tags":tags(0.7),"sku":{"name":sku},"properties":{"diskSizeGB":size,"diskState":"Unattached","timeCreated":(dt.date(2026,11,1)-dt.timedelta(days=random.randint(40,500))).isoformat()+"T00:00:00Z"}})
# NSGs
def rule(n,port,src,access="Allow",prio=100):
    return {"name":n,"properties":{"access":access,"direction":"Inbound","protocol":"Tcp","sourceAddressPrefix":src,"destinationPortRange":port,"priority":prio}}
for i in range(34):
    sub=random.choice(list(subs)); rg=f"rg-{sub.split('-')[-1]}-net"; rules=[rule("allow-https","443","*",prio=100)]
    r=random.random()
    if r<0.35: rules.append(rule("allow-rdp","3389",random.choice(["*","Internet","0.0.0.0/0"]),prio=110))
    elif r<0.55: rules.append(rule("allow-ssh","22",random.choice(["*","Internet"]),prio=120))
    elif r<0.62: rules.append(rule("allow-all-inbound","*","*",prio=130))
    else: rules.append(rule("allow-rdp-corp","3389","10.20.0.0/16",prio=110))
    res.append({"id":rid(sub,rg,"Microsoft.Network/networkSecurityGroups",f"cb-nsg{i:02d}"),"name":f"cb-nsg{i:02d}","type":"microsoft.network/networksecuritygroups","location":random.choice(locs),"resourceGroup":rg,"subscriptionId":subs[sub],"tags":tags(0.5),"properties":{"securityRules":rules}})
res.append({"id":rid("sub-carebridge-prod","rg-prod-legacy","Microsoft.Network/networkSecurityGroups","cb-legacy-rds01-nsg"),"name":"cb-legacy-rds01-nsg","type":"microsoft.network/networksecuritygroups","location":"eastus","resourceGroup":"rg-prod-legacy","subscriptionId":subs["sub-carebridge-prod"],"tags":{},"properties":{"securityRules":[rule("RDP","3389","*",prio=300)]}})
# storage accounts
for i,(n,pub,tls,https) in enumerate([("cbpatientintake",True,"TLS1_2",True),("cbreportsexport",True,"TLS1_0",True),("cbfrontendassets",True,"TLS1_2",True),("cbdevscratch",True,"TLS1_0",False),("cbbackupsprod",False,"TLS1_2",True),("cblogsarchive",False,"TLS1_2",True),("cbmlsandbox",False,"TLS1_1",True),("cbwebstatic",False,"TLS1_2",True),("cbetlstaging",False,"TLS1_2",True)]):
    sub="sub-carebridge-prod" if i<6 else "sub-carebridge-dev"
    res.append({"id":rid(sub,"rg-data","Microsoft.Storage/storageAccounts",n),"name":n,"type":"microsoft.storage/storageaccounts","location":"eastus","resourceGroup":"rg-data","subscriptionId":subs[sub],"tags":tags(0.4),
      "properties":{"allowBlobPublicAccess":pub,"minimumTlsVersion":tls,"supportsHttpsTrafficOnly":https}})
json.dump({"generatedFor":"CareBridge Telehealth (fictional)","snapshotDate":"2026-11-02","data":res},open(os.path.join(OUT,"resource_inventory_before.json"),"w"),indent=1)
# Security events on exposed RDP hosts
rows=[]; start=dt.datetime(2026,10,26,0,0)
attackers=["203.0.113.45","198.51.100.23","192.0.2.77"]
users=["administrator","admin","svc_backup","user","test","scanner"]
for ip,n in zip(attackers,[6200,4800,3100]):
    for k in range(n):
        t=start+dt.timedelta(seconds=random.randint(0,6*86400))
        rows.append([t.isoformat(),"cb-legacy-rds01",4625,10 if random.random()<0.5 else 3,random.choice(users),ip])
# noise: legit failures
for k in range(140):
    t=start+dt.timedelta(seconds=random.randint(0,7*86400)); rows.append([t.isoformat(),random.choice(vms[:20]),4625,10,random.choice(["j.patel","m.owusu","a.kim"]),"10.20."+str(random.randint(1,40))+"."+str(random.randint(2,250))])
for k in range(260):
    t=start+dt.timedelta(seconds=random.randint(0,7*86400)); rows.append([t.isoformat(),random.choice(vms[:20]),4624,10,random.choice(["j.patel","m.owusu","a.kim"]),"10.20."+str(random.randint(1,40))+"."+str(random.randint(2,250))])
# compromise: success after failures, then new local admin
comp=dt.datetime(2026,10,31,3,14,22)
rows.append([comp.isoformat(),"cb-legacy-rds01",4624,10,"svc_backup","203.0.113.45"])
rows.append([(comp+dt.timedelta(minutes=6)).isoformat(),"cb-legacy-rds01",4720,0,"helpdesk_tmp","203.0.113.45"])
rows.append([(comp+dt.timedelta(minutes=7)).isoformat(),"cb-legacy-rds01",4732,0,"helpdesk_tmp","203.0.113.45"])
rows.sort()
with open(os.path.join(OUT,"security_events.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["TimeGenerated","Computer","EventID","LogonType","TargetAccount","IpAddress"]); w.writerows(rows)
print(len(res),"resources;",len(rows),"events")
