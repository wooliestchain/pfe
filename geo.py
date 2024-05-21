import json
import pandas as pd


df = pd.read_json('global.json')

longitude = df['longitude']
latitude = df['latitude']

# Créer une liste de dictionnaires avec longitude et latitude
coord_list = df[['longitude', 'latitude']].to_dict(orient='records')

# Afficher la liste des coordonnées
for coord in coord_list:
    print(coord)


# # Extraire les colonnes longitude et latitude
# longitude = df['longitude'].tolist()
# latitude = df['latitude'].tolist()
#
# # Afficher les listes de longitude et latitude
# print("Longitudes:", longitude)
# print("Latitudes:", latitude)