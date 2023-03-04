'''
Author: Ivanna
Date: 2/26/23
Purpose: filter community centers json file webscrapped by Betty
         to be able to geocode only centers in chicago/cook county
'''

import json
import numpy as np
import pandas as pd
import geopandas as gpd

zip_codes = pd.read_csv("data/chicago_cook_county_zip_codes.csv")
zip_codes['zip'] = zip_codes['zip'].astype(str) # 2,828 obs

community_centers = pd.read_json("cleaning/cleaned_idhs.json")

# create zip code col in community centers df
community_centers['zip'] = community_centers['Address'].str[-5:]

# filter community_centers to only include zips in zip codes
community_centers = community_centers[community_centers['zip'].isin(\
zip_codes['zip'])] # 592 obs remaining

# save filtered dataset
community_centers.to_json('data/community_centers_chicago.json')
