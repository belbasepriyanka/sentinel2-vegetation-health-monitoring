from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]
st.set_page_config(page_title='Dragon Fruit Stress Decision Support',layout='wide')
st.title('Dragon Fruit Nutrient & Stress Decision Support')
st.caption('Synthetic demonstration data only — not a diagnosis or fertilizer recommendation.')
df=pd.read_csv(ROOT/'data'/'sample_nutrient_stress_demo.csv')
priority=st.selectbox('Scouting priority',['All','Inspect','Monitor','Normal'])
view=df if priority=='All' else df[df.scouting_priority==priority]
c1,c2,c3=st.columns(3); c1.metric('Samples',len(view)); c2.metric('Mean risk score',f"{view.risk_score.mean():.1f}"); c3.metric('Stress flags',int(view.stress_flag.sum()))
st.dataframe(view[['sample_id','species','environment','ndvi','ndre','ndmi','tissue_n_pct','tissue_k_pct','risk_score','scouting_priority']].sort_values('risk_score',ascending=False),use_container_width=True)
st.scatter_chart(view,x='ndre',y='tissue_n_pct',color='scouting_priority')
