'''
Author: Betty
Date: 03/05/2022
Purpose: Geocode period poverty alleviation partner organizations locations
'''

import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim

df = pd.read_json("ppindex/data/pp_partners_chicago.json")

geolocator = Nominatim(timeout=10, user_agent='myGeolocator')

df['gcode'] = df['Address'].apply(geolocator.geocode)

df['lat'] = [g.latitude for g in df.gcode]
df['lon'] = [g.longitude for g in df.gcode]

geometry = gpd.points_from_xy(df['lon'], df['lat'])

gdf = gpd.GeoDataFrame(df, geometry=geometry, crs = 'EPSG:4326')