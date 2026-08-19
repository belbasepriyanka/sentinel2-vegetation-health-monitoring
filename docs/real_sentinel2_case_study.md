# Real Public-Data Extension — South Florida Sentinel-2

This extension uses the official **COPERNICUS/S2_SR_HARMONIZED** Level-2A surface-reflectance collection in Google Earth Engine to demonstrate a real-data vegetation-monitoring workflow.

## Workflow

1. Define a South Florida analysis area or replace it with a verified farm/field boundary.
2. Filter Sentinel-2 Level-2A imagery by date and cloud percentage.
3. Mask cloud shadow, cloud, cirrus, and snow/ice using the Scene Classification Layer (SCL).
4. Scale surface reflectance.
5. Calculate NDVI, NDRE, NDMI, and GNDVI.
6. Create seasonal median layers and vegetation-index time series.
7. Export analysis-ready index rasters for GIS, Python, or ML analysis.

Run [`../gee/south_florida_real_case.js`](../gee/south_florida_real_case.js) in the Earth Engine Code Editor.

## Data provenance

Earth Engine dataset: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED

Producer: European Union / ESA / Copernicus.

## Scientific boundary

The public script uses real Sentinel-2 imagery but a demonstration AOI. A field-specific agronomic result requires a verified field boundary, field observations or laboratory ground truth, appropriate sampling dates, and independent validation.
