from __future__ import annotations
import numpy as np
import pandas as pd


def generate_demo(seed: int = 13, n_fields: int = 180) -> pd.DataFrame:
    """Synthetic nutrient/stress dataset for portfolio demonstration only."""
    rng=np.random.default_rng(seed)
    species=rng.choice(['Red','White','Yellow'], n_fields, p=[.4,.4,.2])
    environment=rng.choice(['High tunnel','Open field'], n_fields)
    treatment=rng.choice([0,5,10,20], n_fields)
    temp=rng.normal(29,2.2,n_fields)
    rainfall=np.maximum(0,rng.normal(130,45,n_fields))
    soil_n=np.maximum(5,rng.normal(38+0.55*treatment,8,n_fields))
    soil_p=np.maximum(2,rng.normal(20+0.4*treatment,5,n_fields))
    soil_k=np.maximum(20,rng.normal(115+3.0*treatment-0.20*rainfall,18,n_fields))
    tissue_n=np.clip(1.45+0.010*soil_n+rng.normal(0,.10,n_fields),.8,3.0)
    tissue_p=np.clip(.18+0.008*soil_p+rng.normal(0,.035,n_fields),.08,.7)
    tissue_k=np.clip(.75+0.010*soil_k+rng.normal(0,.12,n_fields),.3,3.2)
    moisture=np.clip(.70-0.0020*np.maximum(temp-29,0)*10+0.0008*rainfall+rng.normal(0,.05,n_fields),.25,.95)
    chlorophyll=np.clip(26+14*(tissue_n-1.3)+rng.normal(0,3,n_fields),10,60)
    ndvi=np.clip(.36+.007*chlorophyll+.08*moisture+rng.normal(0,.025,n_fields),.2,.92)
    ndre=np.clip(.10+.0065*chlorophyll+.035*tissue_n+rng.normal(0,.018,n_fields),.08,.65)
    ndmi=np.clip(.05+.65*moisture+.05*ndvi+rng.normal(0,.025,n_fields),.05,.75)
    red_edge_slope=np.clip(.008+.030*ndre+.004*tissue_n+rng.normal(0,.002,n_fields),.005,.045)
    nir_mean=np.clip(.32+.44*ndvi+rng.normal(0,.025,n_fields),.25,.82)
    swir_mean=np.clip(.42-.35*moisture+rng.normal(0,.02,n_fields),.08,.45)
    nutrient_risk=(tissue_n<1.75) | (tissue_k<1.35)
    water_risk=(moisture<.52) | (ndmi<.42)
    stress_prob=np.clip(.08+.48*nutrient_risk.astype(float)+.38*water_risk.astype(float)+.16*(temp>31)+rng.normal(0,.06,n_fields),0,1)
    stress_flag=(stress_prob>.48).astype(int)
    risk_score=np.clip(100*(.42*stress_prob+.25*(1-ndre/.65)+.20*(1-ndmi/.75)+.13*(1-ndvi/.92)),0,100)
    priority=pd.cut(risk_score,[-1,35,60,100],labels=['Normal','Monitor','Inspect'])
    return pd.DataFrame({
        'sample_id':[f'DF-S{i:03d}' for i in range(1,n_fields+1)],'species':species,'environment':environment,'treatment_t_acre':treatment,
        'temperature_c':temp.round(3),'rainfall_mm':rainfall.round(3),'soil_n_mgkg':soil_n.round(3),'soil_p_mgkg':soil_p.round(3),'soil_k_mgkg':soil_k.round(3),
        'tissue_n_pct':tissue_n.round(3),'tissue_p_pct':tissue_p.round(3),'tissue_k_pct':tissue_k.round(3),'canopy_moisture':moisture.round(4),'chlorophyll_proxy':chlorophyll.round(3),
        'ndvi':ndvi.round(4),'ndre':ndre.round(4),'ndmi':ndmi.round(4),'red_edge_slope':red_edge_slope.round(5),'nir_mean':nir_mean.round(4),'swir_mean':swir_mean.round(4),
        'stress_flag':stress_flag,'stress_probability':stress_prob.round(4),'risk_score':risk_score.round(2),'scouting_priority':priority.astype(str)
    })
