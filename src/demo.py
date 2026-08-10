from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from vegetation_indices import add_indices, add_ndvi_anomaly

ROOT = Path(__file__).resolve().parents[1]
(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "outputs").mkdir(exist_ok=True)
rng = np.random.default_rng(42)
dates = pd.date_range("2025-01-01", periods=24, freq="15D")
season = 0.08 * np.sin(np.linspace(0, 2*np.pi, len(dates)))
b8 = 0.55 + season + rng.normal(0, 0.015, len(dates))
b4 = 0.18 - season*0.3 + rng.normal(0, 0.01, len(dates))
b3 = 0.23 + rng.normal(0, 0.01, len(dates))
b5 = 0.30 + season*0.25 + rng.normal(0, 0.01, len(dates))
b8[14:17] -= 0.13

df = pd.DataFrame({"date": dates, "B3": b3, "B4": b4, "B5": b5, "B8": b8})
df = add_ndvi_anomaly(add_indices(df))
df.to_csv(ROOT/"data"/"sample_sentinel2_timeseries.csv", index=False)

plt.figure(figsize=(9,4.8))
plt.plot(df["date"], df["NDVI"], marker="o", label="NDVI")
plt.plot(df["date"], df["NDRE"], marker="s", label="NDRE")
plt.ylabel("Index value"); plt.xlabel("Date")
plt.title("Synthetic Sentinel-2 Vegetation Health Time Series")
plt.legend(); plt.tight_layout()
plt.savefig(ROOT/"outputs"/"vegetation_health_timeseries.png", dpi=180); plt.close()
summary = {"mean_ndvi": float(df["NDVI"].mean()), "minimum_ndvi": float(df["NDVI"].min()), "stress_observations": int(df["stress_flag"].sum())}
(ROOT/"outputs"/"summary.json").write_text(json.dumps(summary, indent=2))
print(summary)
