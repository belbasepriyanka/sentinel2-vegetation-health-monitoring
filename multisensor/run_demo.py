"""Synthetic multi-sensor crop-stress demo with spatial cross-validation.

Run: python multisensor/run_demo.py
All data and metrics in this extension are synthetic, NOT field-validated.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, roc_auc_score
from sklearn.model_selection import GroupKFold

FEATURES = [
    "ndvi", "ndre", "evi", "ndwi", "uav_canopy_height_m", "uav_texture",
    "hs_red_edge_slope", "hs_nir_reflectance", "hs_water_index",
    "soil_moisture", "soil_n_mgkg", "rainfall_7d_mm", "temperature_c",
]


def generate_synthetic_grid(seed: int = 42) -> pd.DataFrame:
    """324 fictional sample locations, distributed across nine spatial blocks."""
    rng = np.random.default_rng(seed)
    rows, cols = np.indices((18, 18))
    row, col = rows.ravel(), cols.ravel()
    n = len(row)
    longitude = -80.5 + col * 0.00015
    latitude = 25.5 + row * 0.00015
    spatial_block = (row // 6) * 3 + (col // 6)
    dryness = 0.17 * (row / 17) + 0.12 * (col / 17)
    moisture = np.clip(0.76 - dryness + rng.normal(0, 0.09, n), 0.12, 0.95)
    soil_n = np.clip(48 - 15 * (col / 17) + rng.normal(0, 9, n), 4, 85)
    temperature = 26.5 + 5 * (row / 17) + rng.normal(0, 1.1, n)
    rain = np.clip(30 - 15 * (row / 17) + rng.normal(0, 6, n), 0, 55)
    latent = (
        4.4 * (0.55 - moisture) + 0.038 * (38 - soil_n)
        + 0.20 * (temperature - 29) - 0.018 * rain
        + rng.normal(0, 0.65, n)
    )
    true_prob = 1 / (1 + np.exp(-latent))
    label = rng.binomial(1, true_prob)
    return pd.DataFrame({
        "sample_id": [f"DEMO-{i:04d}" for i in range(n)],
        "row": row, "col": col, "longitude": longitude, "latitude": latitude,
        "spatial_block": spatial_block,
        "ndvi": np.clip(0.81 - 0.28 * true_prob + rng.normal(0, 0.045, n), -1, 1),
        "ndre": np.clip(0.46 - 0.22 * true_prob + rng.normal(0, 0.035, n), -1, 1),
        "evi": np.clip(0.68 - 0.26 * true_prob + rng.normal(0, 0.055, n), -1, 1),
        "ndwi": np.clip(0.37 - 0.35 * true_prob + rng.normal(0, 0.05, n), -1, 1),
        "uav_canopy_height_m": np.clip(1.45 - 0.35 * true_prob + rng.normal(0, 0.12, n), 0.2, 2.0),
        "uav_texture": np.clip(0.08 + 0.38 * true_prob + rng.normal(0, 0.04, n), 0, 1),
        "hs_red_edge_slope": np.clip(0.031 - 0.014 * true_prob + rng.normal(0, 0.002, n), 0, 1),
        "hs_nir_reflectance": np.clip(0.59 - 0.20 * true_prob + rng.normal(0, 0.035, n), 0, 1),
        "hs_water_index": np.clip(0.64 - 0.29 * true_prob + rng.normal(0, 0.04, n), 0, 1),
        "soil_moisture": moisture, "soil_n_mgkg": soil_n,
        "rainfall_7d_mm": rain, "temperature_c": temperature,
        "stress_label": label,
    })


def grouped_prediction(df: pd.DataFrame):
    """Held-out predictions and RF tree-disagreement proxy by disjoint spatial blocks."""
    groups = df["spatial_block"].to_numpy()
    y = df["stress_label"].to_numpy()
    x = df[FEATURES]
    cv = GroupKFold(n_splits=5)
    probabilities = np.full(len(df), np.nan)
    disagreement = np.full(len(df), np.nan)
    fold_number = np.zeros(len(df), dtype=int)
    validation_groups = []
    for fold, (train_idx, valid_idx) in enumerate(cv.split(x, y, groups), start=1):
        assert not (set(groups[train_idx]) & set(groups[valid_idx]))
        model = RandomForestClassifier(
            n_estimators=160, min_samples_leaf=3, max_depth=9,
            class_weight="balanced", random_state=100 + fold, n_jobs=-1,
        )
        model.fit(x.iloc[train_idx], y[train_idx])
        probabilities[valid_idx] = model.predict_proba(x.iloc[valid_idx])[:, 1]
        # Indicative tree disagreement only; NOT calibrated predictive uncertainty.
        tree_probs = np.array([
            tree.predict_proba(x.iloc[valid_idx])[:, 1] for tree in model.estimators_
        ])
        disagreement[valid_idx] = tree_probs.std(axis=0)
        fold_number[valid_idx] = fold
        validation_groups.append({
            "fold": fold, "train_blocks": sorted(set(groups[train_idx].tolist())),
            "validation_blocks": sorted(set(groups[valid_idx].tolist())),
        })
    assert np.isfinite(probabilities).all() and np.isfinite(disagreement).all()
    pred = (probabilities >= 0.5).astype(int)
    result = df[["sample_id", "row", "col", "longitude", "latitude",
                 "spatial_block", "stress_label"]].copy()
    result["validation_fold"] = fold_number
    result["stress_probability"] = probabilities
    result["uncertainty_proxy"] = disagreement
    result["risk_class"] = np.select(
        [probabilities >= 0.7, probabilities >= 0.3], ["high", "moderate"], default="low",
    )
    result["scouting_priority"] = np.select(
        [probabilities >= 0.7, probabilities >= 0.3], [1, 2], default=3,
    ).astype(int)
    metrics = {
        "data_kind": "synthetic demonstration; no field validation",
        "validation": "5-fold spatially grouped out-of-fold",
        "samples": int(len(df)), "spatial_blocks": int(df.spatial_block.nunique()),
        "accuracy": float(accuracy_score(y, pred)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y, probabilities)),
        "brier_score": float(mean_squared_error(y, probabilities)),
        "uncertainty_interpretation": "RF tree disagreement proxy, not calibrated uncertainty",
        "folds": validation_groups,
    }
    full_model = RandomForestClassifier(
        n_estimators=160, min_samples_leaf=3, max_depth=9,
        class_weight="balanced", random_state=42, n_jobs=-1,
    ).fit(x, y)
    importance = pd.DataFrame({
        "feature": FEATURES, "importance": full_model.feature_importances_,
    }).sort_values("importance", ascending=False)
    return result, metrics, importance


def save_geojson(predictions: pd.DataFrame, path: Path) -> None:
    """GIS-ready synthetic Point features; NOT actual surveyed farm locations."""
    props = ["sample_id", "spatial_block", "validation_fold", "stress_probability",
             "uncertainty_proxy", "risk_class", "scouting_priority"]
    features = []
    for record in predictions.to_dict("records"):
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [
                float(record["longitude"]), float(record["latitude"])]},
            "properties": {
                key: int(record[key]) if key in ("spatial_block", "validation_fold", "scouting_priority")
                else float(record[key]) if key in ("stress_probability", "uncertainty_proxy")
                else record[key] for key in props
            },
        })
    path.write_text(json.dumps({"type": "FeatureCollection", "features": features}, indent=2))


def main(output: Path = Path("multisensor/outputs")) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    df = generate_synthetic_grid()
    predictions, metrics, importance = grouped_prediction(df)
    df.to_csv(output / "synthetic_multisensor_inputs.csv", index=False)
    predictions.to_csv(output / "spatial_cv_predictions.csv", index=False)
    importance.to_csv(output / "feature_importance.csv", index=False)
    save_geojson(predictions, output / "scouting_priority_points.geojson")
    (output / "validation_metrics.json").write_text(json.dumps(metrics, indent=2))
    print(f"Saved synthetic demonstration outputs to {output}")
    print({key: round(metrics[key], 3) for key in ["accuracy", "f1", "roc_auc", "brier_score"]})
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("multisensor/outputs"))
    args = parser.parse_args()
    main(args.output)
