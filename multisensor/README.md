# Multi-sensor crop-stress extension

**Status:** Runnable synthetic demonstration. The real Sentinel-2 Earth Engine script in the parent repository is a separate public-data pathway. This extension does not claim that real UAV, hyperspectral, soil, weather, or field observations have been jointly calibrated or field-validated.

## What is demonstrated

The extension builds a fictional 18 × 18 geospatial sampling grid with nine spatial blocks. It simulates Sentinel-2-style NDVI, NDRE, EVI and NDWI, UAV canopy height and texture, hyperspectral red-edge/NIR/water features, soil moisture and nitrogen, temperature, and seven-day rainfall. A Random Forest predicts a synthetic stress label using five-fold **GroupKFold** validation by non-overlapping spatial block.

### Outputs

- **synthetic_multisensor_inputs.csv**: feature table with labels, fictional coordinates and group IDs.
- **spatial_cv_predictions.csv**: held-out stress probabilities, risk classes and scouting priorities.
- **scouting_priority_points.geojson**: GIS-ready synthetic point features, not a mapped real field.
- **feature_importance.csv**: exploratory feature importance from an all-sample fitted model.
- **validation_metrics.json**: held-out metrics, group membership per fold and caveats.

The forest's tree-to-tree probability standard deviation is an **uncertainty proxy**, not a calibrated predictive interval. Feature importance does not establish causation or a nutrient diagnosis. Priority 1, 2 and 3 indicate high, moderate and low modeled risk using illustrative thresholds of 0.7 and 0.3.

### Run from repository root

    pip install -r requirements.txt
    python multisensor/run_demo.py
    python -m pytest multisensor/tests -q

Review the real public-data satellite extension in [the Earth Engine script](../gee/south_florida_real_case.js) and its [data notes](../docs/real_sentinel2_case_study.md).

## Ingestion contract for future real-data use

| Input | Intended fields | Validation needed |
|---|---|---|
| Sentinel-2 L2A | observation date, geometry/field ID, reflectance, NDVI, NDRE, EVI, moisture index | cloud mask, spatial and temporal co-registration |
| UAV | footprint, acquisition time, canopy height, canopy texture | georeferencing, ground control, resolution/coverage |
| Hyperspectral | calibrated spectral features, acquisition time, sampling unit | dark/white reference, band and acquisition consistency |
| Soil and field | location, depth, soil moisture, lab results, crop observations | units, sampling protocol, laboratory QA |
| Weather | station/grid ID, timestamp, rainfall and temperature | temporal alignment and missingness checks |

Merge real inputs using vetted sample/field IDs and aligned observation windows. Split by spatially disjoint groups before model selection. Confirm intended transfer conditions with independent fields, seasons and ground-truth observations. Replace illustrative risk thresholds with field-calibrated decision rules. None of these production-validation steps is implied by demonstration scores.
