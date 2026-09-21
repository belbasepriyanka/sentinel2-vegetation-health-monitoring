def normalized_difference(a,b,eps=1e-12):
    return (a-b)/(a+b+eps)

def ndvi(nir,red): return normalized_difference(nir,red)
def ndre(nir,red_edge): return normalized_difference(nir,red_edge)
def gndvi(nir,green): return normalized_difference(nir,green)
def ndmi(nir,swir1): return normalized_difference(nir,swir1)

def add_indices(df):
    """Return a copy with Sentinel-2-style indices from reflectance columns."""
    out = df.copy()
    out["NDVI"] = ndvi(out["B8"], out["B4"])
    out["NDRE"] = ndre(out["B8"], out["B5"])
    if "B3" in out:
        out["GNDVI"] = gndvi(out["B8"], out["B3"])
    if "B11" in out:
        out["NDMI"] = ndmi(out["B8"], out["B11"])
    return out


def add_ndvi_anomaly(df, threshold=-0.08):
    """Flag below-mean NDVI deviations in a demonstration time series."""
    out = df.copy()
    out["ndvi_anomaly"] = out["NDVI"] - out["NDVI"].mean()
    out["stress_flag"] = (out["ndvi_anomaly"] < threshold).astype(int)
    return out
