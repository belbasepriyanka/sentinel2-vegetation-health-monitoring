// Sentinel-2 vegetation health workflow — replace the demo AOI with a real field boundary.
var aoi = ee.Geometry.Rectangle([-80.45, 25.55, -80.35, 25.65]);
function maskS2(img) {
  var scl = img.select('SCL');
  var mask = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10)).and(scl.neq(11));
  return img.updateMask(mask).divide(10000).copyProperties(img, ['system:time_start']);
}
function addIndices(img) {
  var ndvi = img.normalizedDifference(['B8','B4']).rename('NDVI');
  var ndre = img.normalizedDifference(['B8','B5']).rename('NDRE');
  var gndvi = img.normalizedDifference(['B8','B3']).rename('GNDVI');
  var ndmi = img.normalizedDifference(['B8','B11']).rename('NDMI');
  return img.addBands([ndvi, ndre, gndvi, ndmi]);
}
var collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(aoi).filterDate('2025-01-01','2025-12-31')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',35)).map(maskS2).map(addIndices);
Map.centerObject(aoi,13);
Map.addLayer(collection.median().select('NDRE'),{min:0,max:.6,palette:['brown','yellow','green']},'Median NDRE');
print(ui.Chart.image.series(collection.select(['NDVI','NDRE','NDMI']),aoi,ee.Reducer.mean(),10));
