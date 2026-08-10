import sys
from pathlib import Path
import pandas as pd
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from vegetation_indices import add_indices

def test_ndvi():
    df = pd.DataFrame({"B3":[0.2],"B4":[0.2],"B5":[0.3],"B8":[0.6]})
    out = add_indices(df)
    assert abs(out.loc[0,"NDVI"] - 0.5) < 1e-6
