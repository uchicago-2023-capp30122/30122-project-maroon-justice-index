# Author: Ivanna
# Date: 2/27/2023
# Purpose: add neighborhood info to census tracts based on how much of the
#          census tract area lies within a neighborhood to be able to zoom in 
#          on a map

import geopandas as gpd
import pandas as pd

# read in data
census_tracts = gpd.read_file("src/boundaries_census_tracts_2010.geojson")
neighborhoods = gpd.read_file("data/boundaries_neighborhoods.geojson")

# extract names in regular dataframe
neigh_names = neighborhoods[['area_numbe', 'community']]

# join
joined = census_tracts.merge(neigh_names, left_on='commarea_n', 
                            right_on='area_numbe', 
                            how='left')

joined = joined.rename(columns={'community':'neighborhood_name'})
joined['neighborhood_name'] = joined['neighborhood_name'].str.title()

# save geojson
joined.to_file('data/census_tract_with_neigh_names.geojson', driver='GeoJSON')

# add neighborhood name to index
df = pd.read_json("src/index_draft_disposable_income_sex_age.json")
df['tract'] = df['tract'].astype(str)

neigh_names = joined[['tractce10', 'neighborhood_name']]

df = df.merge(neigh_names, left_on = "tract", right_on='tractce10', how='left')
df.to_json("src/index_w_neigh_names.json")

