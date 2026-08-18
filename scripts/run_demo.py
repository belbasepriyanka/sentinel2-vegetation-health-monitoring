from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from src.data_generation import generate_demo
from src.decision_support import classify_stress,nutrient_regression,anomaly_scores
for d in [ROOT/'data',ROOT/'results',ROOT/'figures']: d.mkdir(exist_ok=True)
df=generate_demo(); df.to_csv(ROOT/'data'/'sample_nutrient_stress_demo.csv',index=False)
sm,si,sp,cm=classify_stress(df); nm,ni,npred=nutrient_regression(df); anom=anomaly_scores(df)
pd.DataFrame([sm,nm]).to_csv(ROOT/'results'/'model_metrics.csv',index=False); si.to_csv(ROOT/'results'/'stress_feature_importance.csv',index=False); ni.to_csv(ROOT/'results'/'nutrient_feature_importance.csv',index=False); sp.to_csv(ROOT/'results'/'stress_predictions.csv',index=False); npred.to_csv(ROOT/'results'/'nutrient_predictions.csv',index=False); anom.to_csv(ROOT/'results'/'spectral_anomaly_scores.csv',index=False)
fig,ax=plt.subplots(figsize=(6,5)); ax.scatter(df.tissue_n_pct,df.ndre,c=df.risk_score,alpha=.75); ax.set(xlabel='Tissue N (%)',ylabel='NDRE',title='Synthetic nutrient–spectral relationship'); fig.tight_layout(); fig.savefig(ROOT/'figures'/'nutrient_spectral_relationship.svg'); plt.close(fig)
fig,ax=plt.subplots(figsize=(5,4)); ax.imshow(cm,cmap='Blues'); ax.set(xticks=[0,1],yticks=[0,1],xlabel='Predicted',ylabel='Observed',title='Stress classification confusion matrix');
for i in range(2):
 for j in range(2): ax.text(j,i,cm[i,j],ha='center',va='center')
fig.tight_layout(); fig.savefig(ROOT/'figures'/'confusion_matrix.svg'); plt.close(fig)
imp=si.head(10).sort_values('importance'); fig,ax=plt.subplots(figsize=(8,5)); ax.barh(imp.feature.str.replace('num__','').str.replace('cat__',''),imp.importance); ax.set(title='Stress-model feature importance',xlabel='Importance'); fig.tight_layout(); fig.savefig(ROOT/'figures'/'feature_importance.svg'); plt.close(fig)
counts=df.scouting_priority.value_counts().reindex(['Normal','Monitor','Inspect']).fillna(0); fig,ax=plt.subplots(figsize=(6,4)); ax.bar(counts.index,counts.values); ax.set(ylabel='Samples',title='Decision-support scouting priorities'); fig.tight_layout(); fig.savefig(ROOT/'figures'/'scouting_priority.svg'); plt.close(fig)
fig,ax=plt.subplots(figsize=(6,5)); ax.scatter(npred.tissue_n_pct,npred.predicted_tissue_n_pct,alpha=.75); lo=min(npred.tissue_n_pct.min(),npred.predicted_tissue_n_pct.min()); hi=max(npred.tissue_n_pct.max(),npred.predicted_tissue_n_pct.max()); ax.plot([lo,hi],[lo,hi],'--'); ax.set(xlabel='Observed synthetic tissue N (%)',ylabel='Predicted tissue N (%)',title='Nutrient prediction'); fig.tight_layout(); fig.savefig(ROOT/'figures'/'nutrient_prediction.svg'); plt.close(fig)
print(pd.DataFrame([sm,nm]).to_string(index=False))
