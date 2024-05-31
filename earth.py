import ee
import geemap
import folium

# Authentification et initialisation de l'API Earth Engine
try:
    ee.Initialize()
except ee.EEException as e:
    print("Authentication error: ", e)
    print("Please authenticate using the command line by running: earthengine authenticate")
    raise

# Définir la géométrie de la ville (vous devez définir cityGeometry)
cityGeometry = ee.Geometry.Polygon(
    [[[10.190136329449802, 36.85932073032182],
      [10.19142180000206, 36.84693253206098],
      [10.210523647852378, 36.83226772164917],
      [10.191806488345284, 36.847172226146355]]]
)

# Charger la collection d'images pour la densité de population
populationDataset = ee.ImageCollection('CIESIN/GPWv411/GPW_UNWPP-Adjusted_Population_Density') \
    .filterBounds(cityGeometry) \
    .first()

# Sélectionner la bande de densité de population ajustée
populationRaster = populationDataset.select('unwpp-adjusted_population_density')

# Créer une carte Folium
mapobj = folium.Map(location=[36.934418779239266, 10.093014639942036], zoom_start=10)

# Ajouter la couche raster de densité de population à la carte
vis_params = {
    'min': 0,
    'max': 1000,
    'palette': ['blue', 'green', 'yellow', 'red']
}
population_layer = geemap.ee_tile_layer(populationRaster, vis_params, 'Population Density')
mapobj.add_child(population_layer)

# Ajouter des contrôles de couches
folium.LayerControl().add_to(mapobj)

# Sauvegarder la carte
mapobj.save('output.html')
