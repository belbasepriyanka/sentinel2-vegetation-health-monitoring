import pandas as pd

EPS = 1e-9

def safe_ratio(a, b):
    return a / (b + EPS)

def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["NDVI"] = safe_ratio(out["B8"] - out["B4"], out["B8"] + out["B4"])
    out["NDRE"] = safe_ratio(out["B8"] - out["B5"], out["B8"] + out["B5"])
    out["GNDVI"] = safe_ratio(out["B8"] - out["B3"], out["B8"] + out["B3"])
    out["NDWI"] = safe_ratio(out["B3"] - out["B8"], out["B3"] + out["B8"])
    return out

def add_ndvi_anomaly(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    out = df.copy()
    baseline = out["NDVI"].rolling(window=window, center=True, min_periods=2).median()
    out["NDVI_anomaly"] = out["NDVI"] - baseline
    out["stress_flag"] = out["NDVI_anomaly"] < -0.08
    return out
