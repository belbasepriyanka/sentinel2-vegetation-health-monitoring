# Sentinel-2 Vegetation Health Monitoring

A reproducible Earth observation workflow for monitoring vegetation condition with Sentinel-2 multispectral imagery.

## Why this repository matters
This project demonstrates a complete remote-sensing workflow: satellite data access, spectral-index calculation, temporal anomaly detection, visualization, and reproducible testing.

## Skills demonstrated
- Sentinel-2 / multispectral Earth observation
- NDVI, NDRE, GNDVI and NDWI
- Time-series vegetation monitoring
- Basic stress/anomaly detection
- Python, Pandas, NumPy and Matplotlib
- Google Earth Engine
- Reproducible project structure and CI

## Run locally
```bash
pip install -r requirements.txt
python src/demo.py
pytest -q
```

## Data note
The Python demo generates synthetic time-series data so the repository is fully reproducible. The GEE script is the pathway for applying the workflow to real Sentinel-2 imagery.

## Potential applications
Crop monitoring, drought/stress screening, restoration monitoring, vegetation phenology, and environmental change assessment.

## Author
Priyanka Belbase | Remote Sensing | GIS | Earth Observation | Geospatial AI
