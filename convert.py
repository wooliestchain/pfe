import json


def convert_to_geojson(json_file, geojson_file):
    # Lire le fichier JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Créer la structure GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Parcourir les données et créer des fonctionnalités GeoJSON
    for item in data:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [item["longitude"], item["latitude"]]
            },
            "properties": {
                "dab_index": item["dab_index"],
                "densite_100_metter": item["densite_100_metter"],
                "secteur": item["secteur"],
                "ville": item["ville"],
                "dab_near": item["dab_near"],
                "magasin": item["magasin"]
            }
        }
        geojson["features"].append(feature)

    # Écrire le fichier GeoJSON
    with open(geojson_file, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=4)


# Chemins des fichiers
json_file = 'global.json'
geojson_file = 'output.geojson'

# Conversion
convert_to_geojson(json_file, geojson_file)
