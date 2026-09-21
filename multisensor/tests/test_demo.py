"""Tests for the standalone synthetic multi-sensor extension."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run_demo import FEATURES, generate_synthetic_grid, grouped_prediction, main


def test_generated_features_and_blocks():
    df = generate_synthetic_grid()
    assert len(df) == 324 and df.spatial_block.nunique() == 9
    assert set(FEATURES).issubset(df.columns)
    assert df.stress_label.nunique() == 2


def test_grouped_cv_and_outputs(tmp_path):
    df = generate_synthetic_grid()
    prediction, metrics, importance = grouped_prediction(df)
    assert len(prediction) == len(df)
    assert prediction.stress_probability.between(0, 1).all()
    assert prediction.validation_fold.between(1, 5).all()
    assert 0 <= metrics["roc_auc"] <= 1
    assert set(importance.feature) == set(FEATURES)
    for fold in metrics["folds"]:
        assert set(fold["train_blocks"]).isdisjoint(fold["validation_blocks"])
    main(tmp_path)
    obj = json.loads((tmp_path / "scouting_priority_points.geojson").read_text())
    assert len(obj["features"]) == 324
    assert (tmp_path / "validation_metrics.json").exists()
