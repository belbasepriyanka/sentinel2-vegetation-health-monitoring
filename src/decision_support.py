from __future__ import annotations
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, IsolationForest
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, mean_absolute_error, r2_score, confusion_matrix
from sklearn.model_selection import StratifiedKFold, KFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUM=['temperature_c','rainfall_mm','soil_n_mgkg','soil_p_mgkg','soil_k_mgkg','tissue_n_pct','tissue_p_pct','tissue_k_pct','canopy_moisture','chlorophyll_proxy','ndvi','ndre','ndmi','red_edge_slope','nir_mean','swir_mean','treatment_t_acre']
CAT=['species','environment']

def prep():
    return ColumnTransformer([('num',StandardScaler(),NUM),('cat',OneHotEncoder(handle_unknown='ignore'),CAT)])

def classify_stress(df):
    model=Pipeline([('prep',prep()),('rf',RandomForestClassifier(n_estimators=400,max_depth=10,min_samples_leaf=2,class_weight='balanced',random_state=42,n_jobs=-1))])
    cv=StratifiedKFold(5,shuffle=True,random_state=42); X=df[NUM+CAT]; y=df.stress_flag
    pred=cross_val_predict(model,X,y,cv=cv,method='predict'); prob=cross_val_predict(model,X,y,cv=cv,method='predict_proba')[:,1]
    metrics={'task':'stress_classification','accuracy':accuracy_score(y,pred),'f1':f1_score(y,pred),'roc_auc':roc_auc_score(y,prob)}
    model.fit(X,y); names=model.named_steps['prep'].get_feature_names_out(); imp=pd.DataFrame({'feature':names,'importance':model.named_steps['rf'].feature_importances_}).sort_values('importance',ascending=False)
    out=df[['sample_id','stress_flag','risk_score','scouting_priority']].copy(); out['predicted_stress_probability']=prob; out['predicted_stress']=pred
    return metrics,imp,out,confusion_matrix(y,pred)

def nutrient_regression(df):
    features=['ndvi','ndre','ndmi','red_edge_slope','nir_mean','swir_mean','chlorophyll_proxy','soil_n_mgkg','soil_k_mgkg','temperature_c','rainfall_mm']
    X=df[features]; y=df.tissue_n_pct
    model=RandomForestRegressor(n_estimators=350,max_depth=9,min_samples_leaf=2,random_state=42,n_jobs=-1)
    pred=cross_val_predict(model,X,y,cv=KFold(5,shuffle=True,random_state=42))
    model.fit(X,y)
    metrics={'task':'tissue_n_regression','mae':mean_absolute_error(y,pred),'r2':r2_score(y,pred)}
    imp=pd.DataFrame({'feature':features,'importance':model.feature_importances_}).sort_values('importance',ascending=False)
    out=df[['sample_id','tissue_n_pct']].copy(); out['predicted_tissue_n_pct']=pred
    return metrics,imp,out

def anomaly_scores(df):
    X=df[['ndvi','ndre','ndmi','red_edge_slope','nir_mean','swir_mean']]
    iso=IsolationForest(contamination=.12,random_state=42).fit(X)
    score=-iso.score_samples(X)
    out=df[['sample_id','risk_score','scouting_priority']].copy(); out['spectral_anomaly_score']=score
    return out.sort_values('spectral_anomaly_score',ascending=False)
