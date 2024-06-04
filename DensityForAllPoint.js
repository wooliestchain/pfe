// Liste des coordonnées des points à évaluer
var points = [
[10.822141846068686, 35.77025508588869],
[10.832086281300468, 35.77355421964674]

  // Ajoutez les autres coordonnées de points ici...
];


var cityGeometry = ee.Geometry.Point([10.1797, 36.8065]).buffer(5000);


var populationDataset = ee.ImageCollection('CIESIN/GPWv411/GPW_UNWPP-Adjusted_Population_Density')
  .filterBounds(cityGeometry)
  .first();

var populationRaster = populationDataset.select('unwpp-adjusted_population_density');

// Fonction pour calculer la densité de population pour un point donné
var calculerDensitePopulation = function(point) {
  var pointGeom = ee.Geometry.Point(point);
  var valeurPopulation = populationRaster.reduceRegion({
    reducer: ee.Reducer.first(),
    geometry: pointGeom,
    scale: 100,
    bestEffort: true
  });
  return valeurPopulation.get('unwpp-adjusted_population_density');
};

// Boucle à travers les points pour calculer et afficher la densité de population
for (var i = 0; i < points.length; i++) {
  var densite = calculerDensitePopulation(points[i]);
  print('Densité de population au point ' + (i+1) + ':', densite);
}
