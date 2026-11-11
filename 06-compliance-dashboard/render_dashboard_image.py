import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
NAVY="#1F3A5F"; LIGHT="#A8B3C4"; INK="#1b2430"; MUTED="#5b6573"
fig=plt.figure(figsize=(13,8.2),dpi=150); fig.patch.set_facecolor("white")
fig.text(0.03,0.95,"Brightline Health: Compliance Posture",fontsize=20,fontweight="bold",color=NAVY)
fig.text(0.03,0.915,"As of 2026-11-10 · ISO 27001 controls (after internal-audit corrections), risk register, audit actions",fontsize=10,color=MUTED)
k=[("Control maturity","75%","from 43% at baseline"),("High risks","0","from 4 before treatment"),("Risk score reduction","57%","151 → 65"),("Open audit actions","6","1 High, 4 Medium, 1 Low"),("Overdue actions","0","next due 2026-11-21")]
for i,(a,b,c) in enumerate(k):
    ax=fig.add_axes([0.03+i*0.19,0.76,0.175,0.12]); ax.set_xticks([]); ax.set_yticks([]); ax.set_facecolor("#F1F5F9"); [s.set_visible(False) for s in ax.spines.values()]
    ax.text(0.07,0.75,a,fontsize=10,color=MUTED,transform=ax.transAxes); ax.text(0.07,0.32,b,fontsize=24,fontweight="bold",color=NAVY,transform=ax.transAxes); ax.text(0.07,0.1,c,fontsize=8.5,color=MUTED,transform=ax.transAxes)
def bars(rect,title,cats,before,after,lb,la,loc):
    ax=fig.add_axes(rect); x=np.arange(len(cats)); w=0.36
    b1=ax.bar(x-w/2-0.01,before,w,color=LIGHT,label=lb); b2=ax.bar(x+w/2+0.01,after,w,color=NAVY,label=la)
    for bs in (b1,b2):
        for r in bs: ax.text(r.get_x()+r.get_width()/2,r.get_height()+0.2,int(r.get_height()),ha="center",fontsize=10,color=INK)
    ax.set_xticks(x); ax.set_xticklabels(cats,fontsize=10); ax.set_title(title,loc="left",fontsize=13,fontweight="bold",color=INK)
    [ax.spines[s].set_visible(False) for s in ("top","right","left")]; ax.set_yticks([]); ax.set_ylim(0,max(before+after)*1.25); ax.legend(frameon=False,fontsize=9,loc=loc,ncol=2)
bars([0.03,0.36,0.44,0.32],"Controls (20)",["Implemented","Partial","Missing"],[2,13,5],[11,8,1],"Baseline (Aug)","Current (Nov)","upper right")
bars([0.53,0.36,0.44,0.32],"Risks (12)",["High","Medium","Low"],[4,8,0],[0,2,10],"Inherent","Residual","upper left")
ax=fig.add_axes([0.03,0.04,0.44,0.24]); ax.axis("off"); ax.text(0,0.95,"Top residual risks",fontsize=13,fontweight="bold",color=INK)
for i,r in enumerate([("R01","Phishing → Microsoft 365 account takeover","9 · Medium","IT Lead"),("R06","Vendor breach exposes PHI","8 · Medium","Operations"),("R04","Ransomware on a laptop spreads","6 · Low","IT Lead")]):
    y=0.7-i*0.24; ax.text(0,y,r[0],fontsize=10,fontweight="bold",color=NAVY); ax.text(0.1,y,r[1],fontsize=10,color=INK); ax.text(0.7,y,r[2],fontsize=10,color=INK); ax.text(0.86,y,r[3],fontsize=9,color=MUTED)
ax=fig.add_axes([0.53,0.04,0.44,0.24]); ax.axis("off"); ax.text(0,0.95,"Next audit actions",fontsize=13,fontweight="bold",color=INK)
for i,r in enumerate([("2026-11-21","Fix 3 overdue critical vulnerabilities","Medium"),("2026-12-15","First backup restore test","Medium"),("2026-12-31","Add EHR to access reviews","Medium"),("2027-01-31","Write and test business continuity plan","High")]):
    y=0.72-i*0.2; ax.text(0,y,r[0],fontsize=10,color=MUTED); ax.text(0.22,y,r[1],fontsize=10,color=INK); ax.text(0.86,y,r[2],fontsize=9,fontweight="bold",color="#b33a3a" if r[2]=="High" else "#9a5b13")
plt.savefig("dashboard.png",facecolor="white")
