// Sentinel-2 vegetation monitoring starter workflow for Google Earth Engine.
// Replace roi with your own geometry before running.
var roi = ee.Geometry.Rectangle([-80.6, 25.3, -80.1, 25.8]);

function maskS2(image) {
  var scl = image.select('SCL');
  var mask = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10));
  return image.updateMask(mask).divide(10000).copyProperties(image, ['system:time_start']);
}

function addIndices(image) {
  var ndvi = image.normalizedDifference(['B8','B4']).rename('NDVI');
  var ndre = image.normalizedDifference(['B8','B5']).rename('NDRE');
  var gndvi = image.normalizedDifference(['B8','B3']).rename('GNDVI');
  return image.addBands([ndvi, ndre, gndvi]);
}

var collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(roi)
  .filterDate('2025-01-01', '2026-01-01')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
  .map(maskS2)
  .map(addIndices);

Map.centerObject(roi, 10);
Map.addLayer(collection.median().select('NDVI'), {min:0, max:0.9}, 'Median NDVI');
print('Images:', collection.size());
