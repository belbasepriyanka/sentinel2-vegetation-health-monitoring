from src.data_generation import generate_demo
from src.vegetation_indices import ndvi
from src.decision_support import classify_stress

def test_indices():
    assert round(ndvi(.8,.2),3)==.6

def test_demo_and_model():
    df=generate_demo(); assert len(df)==180; assert df.risk_score.between(0,100).all()
    m,_,_,_=classify_stress(df); assert 0<=m['accuracy']<=1
