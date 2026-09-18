
import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def shell(name, title, subtitle, style):
    global PALETTE, INK, PANEL, BG, ACCENT
    themes = {
      'terminal': ('#091411','#10221d','#e7f5ee','#3fe0a0','#7e9c8d',4),
      'purple': ('#171625','#222137','#f5f1ff','#ba9bff','#9ca1c0',12),
      'indigo': ('#f4f5fb','#ffffff','#242746','#5149b9','#64708b',18),
      'coral': ('#faf7f2','#ffffff','#302a27','#c7543e','#796d65',20),
      'blue': ('#f2f6fa','#ffffff','#183348','#126bb5','#5d7486',8),
      'cyan': ('#07141d','#102330','#def5ff','#53d2ed','#8caab9',4),
      'ops': ('#0b1720','#132733','#e7f5f4','#4edbc4','#99b5bd',10),
      'editorial': ('#f8f7f3','#ffffff','#253b38','#317764','#6b7d77',6),
      'amber': ('#17212c','#223140','#f8f4e9','#efbc67','#a6b2bf',6),
    }
    BG,PANEL,INK,ACCENT,MUTED,RADIUS=themes[style]
    PALETTE=[ACCENT,'#4c9fd6','#d99455','#ae83c6','#6cae8b']
    px.defaults.color_discrete_sequence=PALETTE
    st.markdown(f"""<style>
    .stApp {{background:{BG};color:{INK}}}
    [data-testid="stHeader"] {{background:{BG};}}
    .block-container {{max-width:1480px;padding:2rem 2.5rem 4rem;}}
    [data-testid="stSidebar"] {{background:{PANEL};border-right:1px solid {MUTED}35;}}
    h1,h2,h3,p,label,[data-testid="stMarkdownContainer"], [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{color:{INK};}}
    h1 {{font-size:2.55rem!important;letter-spacing:-.055em;line-height:1.12!important;font-weight:650!important;}}
    h2,h3 {{letter-spacing:-.025em;}}
    [data-testid="stCaptionContainer"] {{opacity:1!important;}}
    [data-testid="stCaptionContainer"] p {{color:{MUTED}!important;}}
    [data-tag] {{background:{ACCENT}25!important;color:{INK}!important;border:1px solid {ACCENT}50;}}
    [data-tag] span,[data-tag] button {{color:{INK}!important;}}
    [data-testid="stMetric"] {{background:{PANEL};border:1px solid {MUTED}30;border-top:2px solid {ACCENT};border-radius:{RADIUS}px;padding:18px 20px;}}
    [data-testid="stMetricValue"] {{font-variant-numeric:tabular-nums;font-size:1.8rem;}}
    [data-testid="stPlotlyChart"] {{background:{PANEL};border:1px solid {MUTED}30;border-radius:{RADIUS}px;overflow:hidden;}}
    [data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"], textarea {{background:{PANEL}!important;color:{INK}!important;}}
    input,textarea {{color:{INK}!important;-webkit-text-fill-color:{INK}!important;}}
    [data-baseweb="tag"] {{background:{ACCENT}25!important;color:{INK}!important;}}
    [data-baseweb="tag"] span {{color:{INK}!important;}}
    button[kind="secondary"], [data-testid="stDownloadButton"] button {{background:{PANEL};color:{INK};border-color:{MUTED}65;}}
    [data-baseweb="tab"] {{color:{INK}!important;}}
    [data-testid="stAlert"] {{background:{PANEL};color:{INK};}}
    .eyebrow {{font:600 11px ui-monospace,monospace;letter-spacing:.15em;color:{ACCENT};margin-bottom:16px;}}
    .hero {{border-bottom:1px solid {MUTED}40;padding:12px 0 25px;margin-bottom:24px;}}
    .hero p {{max-width:850px;color:{MUTED};font-size:1rem;}}
    .brief {{border-left:3px solid {ACCENT};background:{PANEL};padding:16px 20px;margin:18px 0;color:{INK};}}
    @media(max-width:700px){{.block-container{{padding:1rem;}}h1{{font-size:1.8rem!important;}}}}
    </style>""",unsafe_allow_html=True)
    st.markdown(f'<div class="hero"><div class="eyebrow">MORRIS / {html.escape(name.upper())} · SYNTHETIC DEMO</div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',unsafe_allow_html=True)
    st.sidebar.caption('MORRIS · PORTFOLIO LAB')
    st.sidebar.caption('Fictional data. Explore the workflow; no external systems are connected.')

def chart(fig, height=340):
    for axis in [fig.layout.xaxis,fig.layout.yaxis]:
        if axis.title.text:axis.title.text=axis.title.text.replace('_',' ').title()
    for trace in fig.data:
        if trace.name:trace.name=trace.name.replace('_',' ').title()
    fig.update_layout(template='plotly_white',paper_bgcolor=PANEL,plot_bgcolor=PANEL,font=dict(color=INK,size=12),colorway=PALETTE,height=height,margin=dict(l=55,r=25,t=55,b=55),legend=dict(orientation='h',y=-.24,x=0),hoverlabel=dict(bgcolor=PANEL,font_color=INK))
    fig.update_xaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    fig.update_yaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    st.plotly_chart(fig,use_container_width=True,theme=None)

def brief(text):
    st.markdown('<div class="brief">'+html.escape(text)+'</div>',unsafe_allow_html=True)

def money(value):
    sign='−' if value<0 else ''
    return f'{sign}${abs(value)/1e6:,.2f}M' if abs(value)>=1e6 else f'{sign}${abs(value):,.0f}'

def metrics(items):
    for col,(label,value) in zip(st.columns(len(items)),items):col.metric(label,value)

def table(df, name='detail', height=360):
    config={}
    for col in df.columns:
        label=str(col).replace('_',' ').title()
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            if any(x in str(col) for x in ['pct','margin','confidence','attainment','probability','achievement']):
                config[col]=st.column_config.NumberColumn(label,format='%.3f')
            elif any(x in str(col) for x in ['amount','revenue','arr','acv','cost','expense','cash','earned','capitalized','amortization','balance','asset','budget','forecast','variance','value','backlog','receipts','payroll','subcontractor','materials','labor']):
                config[col]=st.column_config.NumberColumn(label,format='$%.2f')
            else:config[col]=st.column_config.NumberColumn(label)
        else:config[col]=st.column_config.Column(label)
    st.dataframe(df,use_container_width=True,hide_index=True,height=height,column_config=config)
    st.download_button('Download '+name.replace('_',' ')+' CSV',df.to_csv(index=False),name+'.csv','text/csv',key='export_'+name)

def nonempty(df):
    if df.empty:
        st.info('No records in this selection. Choose at least one filter value to continue.')
        st.stop()

import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="RevOps AI Automation",layout="wide")
shell('REVENUE OPERATIONS','Make the next action obvious.','Prioritize leads by explicit scoring rules, response-time breaches, and stage-specific follow-up.','ops')
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


nonempty(f)
metrics([('Open leads',str(len(f))),('High priority',str(int(f.priority.eq('High').sum()))),('Overdue follow-ups',str(int(f.sla_risk.sum()))),('Average rule score',f'{f.score.mean():.0f} / 100')])
brief('Scores use explicit rules: intent × 4 + engagement × 3 + company-fit × 3. A follow-up breaches the demo SLA after 48 hours for medium/high priority leads. No messages are sent.')
queue=f.sort_values(['sla_risk','score'],ascending=[False,False])
a,b=st.columns([1.7,1])
with a:
    st.subheader('Action queue')
    action_filter=st.selectbox('Workstream',['All actions']+sorted(queue.next_action.unique().tolist()))
    q=queue if action_filter=='All actions' else queue[queue.next_action==action_filter]
    table(q,'revops_actions')
with b:
    st.subheader('Lead briefing')
    selected=st.selectbox('Lead',queue.lead_id.tolist())
    r=queue[queue.lead_id==selected].iloc[0]
    st.write(f'**{r.company}** · {r.stage}')
    st.progress(min(float(r.score)/100,1),text=f'{r.score}/100 rule score')
    st.write(f'{r.hours_since_touch} hours since last touch')
    st.info(r.next_action)
    st.write(f'Intent contribution: **{r.intent*4}**')
    st.write(f'Engagement contribution: **{r.engagement*3}**')
    st.write(f'Company-fit contribution: **{min(10,r.employees/100)*3:g}**')
with st.expander('Pipeline distribution'):
    stage=f.groupby('stage',as_index=False).size()
    chart(px.bar(stage,x='stage',y='size',title='Leads by stage',category_orders={'stage':['New','Qualified','Discovery','Proposal','Negotiation']}))
