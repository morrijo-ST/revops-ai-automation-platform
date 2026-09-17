import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="RevOps AI Automation",layout="wide")
st.title("RevOps AI Automation Platform")
st.caption("Synthetic lead scoring, pipeline hygiene, SLA monitoring, and next-best-action routing.")
random.seed(8)
rows=[]
for i in range(220):
    employees=random.choice([20,50,100,250,500,1000])
    intent=random.randint(1,10)
    engagement=random.randint(1,10)
    fit=min(10,employees/100)
    score=round(intent*4+engagement*3+fit*3)
    stage=random.choice(["New","Qualified","Discovery","Proposal","Negotiation"])
    hours=random.randint(1,96)
    rows.append({"lead_id":f"L-{i+1:04}","company":f"Prospect {i+1:03}","employees":employees,"intent":intent,"engagement":engagement,"score":score,"stage":stage,"hours_since_touch":hours})
df=pd.DataFrame(rows)
df["priority"]=pd.cut(df.score,[-1,45,65,1000],labels=["Nurture","Medium","High"])
df["sla_risk"]=(df.hours_since_touch>48)&(df.priority!="Nurture")
df["next_action"]=df.apply(lambda r:"Escalate follow-up" if r.sla_risk else ("Book discovery" if r.score>=66 and r.stage in ["New","Qualified"] else "Continue sequence"),axis=1)

priorities=st.sidebar.multiselect("Priority",["High","Medium","Nurture"],default=["High","Medium","Nurture"])
f=df[df.priority.astype(str).isin(priorities)]

c1,c2,c3,c4=st.columns(4)
c1.metric("Open leads",len(f))
c2.metric("High priority",int((f.priority.astype(str)=="High").sum()))
c3.metric("SLA risks",int(f.sla_risk.sum()))
c4.metric("Avg score",f"{f.score.mean():.0f}")

st.subheader("Lead scoring")
st.plotly_chart(px.scatter(f,x="engagement",y="intent",size="employees",color=f.priority.astype(str),hover_name="company",hover_data=["score","stage"]),use_container_width=True)

left,right=st.columns(2)
with left:
    st.subheader("Pipeline stage")
    stage=f.groupby("stage",as_index=False).size()
    st.plotly_chart(px.bar(stage,x="stage",y="size"),use_container_width=True)
with right:
    st.subheader("Next-best-action mix")
    act=f.groupby("next_action",as_index=False).size()
    st.plotly_chart(px.pie(act,names="next_action",values="size"),use_container_width=True)

st.subheader("Priority work queue")
queue=f.sort_values(["sla_risk","score"],ascending=[False,False])
st.dataframe(queue[["lead_id","company","score","priority","stage","hours_since_touch","sla_risk","next_action"]].head(60),use_container_width=True,hide_index=True)
st.info("Production implementations would connect CRM webhooks, enrichment providers, email/calendar tools, and human approval controls. This public demo keeps the logic deterministic and inspectable.")
