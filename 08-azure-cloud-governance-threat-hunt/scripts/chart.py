import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
b=json.load(open("output/before/summary.json")); a=json.load(open("output/after/summary.json"))
items=[("Internet-exposed SSH/RDP/all-port rules","open_mgmt_rules"),("Orphaned managed disks","orphaned_disks"),("Idle VMs (deallocated > 45 days)","deallocated_over45"),("Storage accounts: public / weak TLS / HTTP","storage_issues")]
fig,(ax,ax2)=plt.subplots(1,2,figsize=(13,4.6),dpi=150,gridspec_kw={"width_ratios":[1.6,1]})
y=np.arange(len(items))[::-1]; h=0.36
for i,(lab,k) in enumerate(items):
    ax.barh(y[i]+h/2,b[k],h,color="#A8B3C4"); ax.barh(y[i]-h/2,a[k],h,color="#1F3A5F")
    ax.text(b[k]+0.4,y[i]+h/2,str(b[k]),va="center",fontsize=10); ax.text(a[k]+0.4,y[i]-h/2,str(a[k]),va="center",fontsize=10,fontweight="bold")
ax.set_yticks(y); ax.set_yticklabels([i[0] for i in items],fontsize=10); ax.set_xticks([])
[ax.spines[s].set_visible(False) for s in ("top","right","bottom")]
ax.set_title("Findings before (grey) and after (navy) remediation",loc="left",fontsize=13,fontweight="bold")
ax2.axis("off"); ax2.text(0,0.92,"Threat hunt: cb-legacy-rds01",fontsize=13,fontweight="bold",color="#1b2430")
lines=[(f"{b['bruteforce_failures']:,}","failed RDP logons in 6 days from 3 internet IPs"),("1","successful logon (svc_backup) after brute force"),("1","new local admin created 6 minutes later"),("0","exposed management ports after remediation")]
for i,(n,t) in enumerate(lines):
    yy=0.72-i*0.2; ax2.text(0,yy,n,fontsize=18,fontweight="bold",color="#b33a3a" if i<3 else "#2e7d32"); ax2.text(0.3,yy+0.02,t,fontsize=10,color="#1b2430",wrap=True)
fig.suptitle("CareBridge Telehealth Azure audit (simulated data)",x=0.01,ha="left",fontsize=15,fontweight="bold",color="#1F3A5F")
plt.tight_layout(); plt.savefig("audit_summary.png",facecolor="white")
