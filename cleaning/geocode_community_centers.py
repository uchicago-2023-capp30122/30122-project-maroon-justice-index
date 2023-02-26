# Author: Ivanna
# Date: 2/26/2023
# Purpose: save a geojson file with points for community centers to
#          be able to map them in plotly express

import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim

# read community centers filename and subset
df = pd.read_json("data/community_centers_chicago.json")

# initialize nominatim geocoder
geolocator = Nominatim(timeout=10, user_agent='myGeolocator')

# geocode address column
df['gcode'] = df['Address'].apply(geolocator.geocode)

# filter dataframe to remove NAs
df_without_none = df.dropna(subset=['gcode'])
df_without_none['lat'] = [g.latitude for g in df_without_none.gcode]
df_without_none['lon'] = [g.longitude for g in df_without_none.gcode]

# # Convert the DataFrame to a GeoDataFrame with Point geometries
# geometry = gpd.points_from_xy(data['lon'], data['lat'])
# gdf = gpd.GeoDataFrame(data, geometry=geometry)

# cannot turn to geojson for whatever reason, so i'm exporting as csv and 
# trying this later

# save to csv
df_without_none.to_csv("data/geocoded_community_centers_chicago.csv", index = False)
