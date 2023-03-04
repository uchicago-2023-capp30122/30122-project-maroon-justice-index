'''
Author: Ivanna
Date: 2/27/2023
Purpose: add neighborhood info to census tracts based on how much of the
         census tract area lies within a neighborhood to be able to zoom in 
         on a map and then add neighborhood info to index data

Inputs: ppindex/src/boundaries_census_tracts_2010.geojson
        ppindex/data/boundaries_neighborhoods.geojson

Outputs: ppindex/data/census_tract_with_neigh_names.geojson
         ppindex/src/index_w_neigh_names.json
         ppindex/data/neigh_lat_long.csv
'''

import geopandas as gpd
import pandas as pd

# read in data
census_tracts = gpd.read_file("ppindex/src/boundaries_census_tracts_2010.geojson")
neighborhoods = gpd.read_file("ppindex/data/boundaries_neighborhoods.geojson")

# extract names in regular dataframe
neigh_names = neighborhoods[['area_numbe', 'community']]

# join
joined = census_tracts.merge(neigh_names, left_on='commarea_n', 
                            right_on='area_numbe', 
                            how='left')

joined = joined.rename(columns={'community':'neighborhood_name'})
joined['neighborhood_name'] = joined['neighborhood_name'].str.title()

# save geojson
joined.to_file('ppindex/data/census_tract_with_neigh_names.geojson', 
driver='GeoJSON')

# ------------------ add neighborhood name to index ---------------------

df = pd.read_json("ppindex/data/pp_index.json")
df['tract'] = df['tract'].astype(str)

neigh_names = joined[['tractce10', 'neighborhood_name']]

df = df.merge(neigh_names, left_on = "tract", right_on='tractce10', how='left')
df.to_json("ppindex/src/index_w_neigh_names.json")

# getting neighborhood centroids
centroids = neighborhoods.geometry.centroid
lons = centroids.x
lats = centroids.y
names = neighborhoods['community']

# Create a DataFrame with the coordinates and neighborhood names
neigh_lat_long = pd.DataFrame({'neighborhood_name': names, 'neigh_lat': lats, 
'neigh_lon': lons})
neigh_lat_long['neighborhood_name'] = neigh_lat_long['neighborhood_name'\
].str.title()

neigh_lat_long.to_csv("ppindex/data/neigh_lat_long.csv")

# now join to index dataframe
ppidx = pd.read_json("ppindex/src/index_w_neigh_names.json") 

merged = pd.merge(ppidx, neigh_lat_long, how='left', on='neighborhood_name')

merged.to_json("ppindex/src/index_w_neigh_names.json")