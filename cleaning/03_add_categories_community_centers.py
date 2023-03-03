'''
Author: Ivanna
Date: 3/2/2023
Purpose: condense community center categories
'''

import pandas as pd
import geopandas as gpd

ccs = gpd.read_file("src/comm_centers_neighborhoods.geojson")
crosswalk = pd.read_csv("data/community_centers_crosswalk.csv")

joined = ccs.merge(crosswalk, left_on='Type', 
                            right_on='Type', 
                            how='left')

joined['Category'] = joined['Category'].str.strip()

# joined.drop(joined[joined['Filter'] == " drop"].index, inplace = True) # 218

joined.to_file("src/comm_centers_neighborhoods.geojson", driver='GeoJSON')