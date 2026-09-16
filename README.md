# GeoAI Multi-Sensor Crop Stress Intelligence

**Python • scikit-learn • Sentinel-2 • spectral features • environmental data • spatial validation • decision support**

A recruiter-facing portfolio implementation of a multi-sensor crop-stress workflow designed to move from raw Earth-observation and field indicators to **repeatable machine-learning analysis, uncertainty-aware interpretation, and scouting-priority outputs**.

> **Portfolio note:** GitHub commit dates reflect when public code and documentation were published or maintained. They are not intended to represent the start date of the underlying research or analytical work.

## What this project demonstrates

| Capability | Implementation |
|---|---|
| Multi-source geospatial integration | Sentinel-2 vegetation indices, spectral indicators, soil/tissue variables, weather and moisture features |
| Feature engineering | NDVI, NDRE, NDMI, GNDVI, red-edge slope, NIR/SWIR and environmental predictors |
| Machine learning | Random Forest classification/regression and Isolation Forest anomaly detection |
| Model evaluation | reproducible train/evaluate workflow, feature importance and risk interpretation |
| Operational output | 0–100 scouting score and Normal / Monitor / Inspect prioritization |
| Reproducibility | scripts, notebook, tests, figures, results and version-controlled workflow |
| Production thinking | separation of ingestion, feature construction, modeling, scoring and dashboard delivery |

## Research architecture

The broader research workflow motivating this repository combines **Sentinel-2 imagery, UAV canopy information, hyperspectral red-edge/NIR/water-sensitive features, soil moisture, field observations, rainfall and temperature**. Because unpublished field and spectral measurements are not distributed publicly, this repository separates:

1. a **real public Sentinel-2 workflow**, and
2. a **synthetic demonstration dataset** used to show the machine-learning and decision-support architecture.

This keeps the software reproducible without presenting demonstration values as measured research data.

## Real Sentinel-2 workflow

The repository includes a real **Sentinel-2 Level-2A South Florida vegetation-monitoring workflow** using `COPERNICUS/S2_SR_HARMONIZED` in Google Earth Engine.

- [`gee/south_florida_real_case.js`](gee/south_florida_real_case.js)
- [`docs/real_sentinel2_case_study.md`](docs/real_sentinel2_case_study.md)
- SCL-based cloud, cloud-shadow and cirrus masking
- NDVI, NDRE, NDMI and GNDVI
- seasonal median products
- vegetation-index time series
- export-ready rasters for downstream GIS/Python/ML workflows

The public AOI is a demonstration region. Field-specific agronomic interpretation requires a verified field boundary and corresponding ground observations.

## Machine-learning workflow

```mermaid
flowchart LR
 A[Satellite / spectral indicators] --> E[Feature table]
 B[Soil + tissue variables] --> E
 C[Weather + moisture] --> E
 D[Field observations] --> E
 E --> F[QA + feature engineering]
 F --> G[Random Forest]
 F --> H[Isolation Forest]
 G --> I[Stress probability / regression]
 H --> J[Anomaly score]
 I --> K[Risk integration]
 J --> K
 K --> L[Scouting priority map / dashboard]
```

## Technical highlights

- integrates soil N/P/K, tissue N/P/K, weather, canopy moisture and spectral predictors
- Random Forest stress classification
- tissue-N regression from nutrient + spectral variables
- Isolation Forest spectral anomaly scoring
- feature-importance analysis
- uncertainty-aware risk interpretation
- 0–100 scouting-priority score
- Sentinel-2 preprocessing in Google Earth Engine
- Streamlit decision-support dashboard
- reproducible scripts, notebook, figures, results and tests

## Visual outputs

| Nutrient–spectral relationship | Stress classification |
|---|---|
| ![relationship](figures/nutrient_spectral_relationship.svg) | ![matrix](figures/confusion_matrix.svg) |

![Scouting priority](figures/scouting_priority.svg)

## Repository structure

```text
sentinel2-vegetation-health-monitoring/
├── dashboard/      # Streamlit decision-support interface
├── data/           # public demonstration data
├── docs/           # methodology and real-data case study
├── figures/        # model and decision-support visuals
├── gee/            # real Sentinel-2 Earth Engine workflow
├── notebooks/      # exploratory/reproducible analysis
├── results/        # machine-readable outputs
├── scripts/        # runnable workflow entry points
├── src/            # reusable analysis components
└── tests/          # workflow validation
```

## Run locally

```bash
pip install -r requirements.txt
python scripts/run_demo.py
python -m pytest -q
streamlit run dashboard/app.py
```

For the real satellite-data workflow, open [`gee/south_florida_real_case.js`](gee/south_florida_real_case.js) in Google Earth Engine.

## Production relevance

This project is structured around the same steps required in operational geospatial ML: **data ingestion → QA/QC → feature engineering → model training → validation → inference → uncertainty/risk interpretation → user-facing output**. The architecture is designed to be extendable to larger field collections, additional sensors and production-scale batch inference.

## Scientific boundary

Public CSV values, risk scores and model metrics in the demonstration pathway are synthetic. They are not unpublished research measurements, crop diagnoses or fertilizer recommendations. Operational deployment requires field-specific ground truth, independent validation and appropriate agronomic calibration.

## Author

**Priyanka Belbase**  
Geospatial Data Science | Remote Sensing | GeoAI | Machine Learning
