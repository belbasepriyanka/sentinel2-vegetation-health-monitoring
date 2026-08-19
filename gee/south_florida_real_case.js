// Real public-data case study: South Florida vegetation monitoring
// Data: COPERNICUS/S2_SR_HARMONIZED
// Replace the demonstration AOI with a verified field boundary for applied use.

var aoi = ee.Geometry.Rectangle([-80.65, 25.35, -80.25, 25.75]);
var start = '2025-01-01';
var end = '2025-06-30';

function maskS2(img) {
  var scl = img.select('SCL');
  var good = scl.neq(3) // cloud shadow
    .and(scl.neq(8))    // medium cloud
    .and(scl.neq(9))    // high cloud
    .and(scl.neq(10))   // cirrus
    .and(scl.neq(11));  // snow/ice
  return img.updateMask(good).divide(10000)
    .copyProperties(img, ['system:time_start']);
}

function addIndices(img) {
  var ndvi = img.normalizedDifference(['B8','B4']).rename('NDVI');
  var ndre = img.normalizedDifference(['B8','B5']).rename('NDRE');
  var ndmi = img.normalizedDifference(['B8','B11']).rename('NDMI');
  var gndvi = img.normalizedDifference(['B8','B3']).rename('GNDVI');
  return img.addBands([ndvi, ndre, ndmi, gndvi]);
}

var collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(aoi)
  .filterDate(start, end)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 60))
  .map(maskS2)
  .map(addIndices);

print('Usable Sentinel-2 scenes', collection.size());

var median = collection.median().clip(aoi);
Map.centerObject(aoi, 10);
Map.addLayer(median, {bands:['B4','B3','B2'], min:0.02, max:0.30}, 'True color');
Map.addLayer(median.select('NDVI'), {min:0,max:0.9,palette:['8c510a','f6e8c3','01665e']}, 'Median NDVI');
Map.addLayer(median.select('NDRE'), {min:-0.1,max:0.6,palette:['ffffcc','41b6c4','0c2c84']}, 'Median NDRE');
Map.addLayer(median.select('NDMI'), {min:-0.5,max:0.7,palette:['a6611a','f5f5f5','018571']}, 'Median NDMI');

var chart = ui.Chart.image.series({
  imageCollection: collection.select(['NDVI','NDRE','NDMI']),
  region: aoi,
  reducer: ee.Reducer.mean(),
  scale: 20
}).setOptions({title:'South Florida Sentinel-2 vegetation-index time series'});
print(chart);

Export.image.toDrive({
  image: median.select(['NDVI','NDRE','NDMI','GNDVI']),
  description: 'South_Florida_Sentinel2_Vegetation_Indices',
  folder: 'GEE_Agriculture_Portfolio',
  region: aoi,
  scale: 10,
  maxPixels: 1e10
});
