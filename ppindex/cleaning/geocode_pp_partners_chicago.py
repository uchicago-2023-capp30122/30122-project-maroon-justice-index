import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim

df = pd.read_json("ppindex/data/pp_partners_chicago.json")

geolocator = Nominatim(timeout=10, user_agent='myGeolocator')

df['gcode'] = df['Address'].apply(geolocator.geocode)

df_without_none = df.dropna(subset=['gcode'])
df_without_none['lat'] = [g.latitude for g in df_without_none.gcode]
df_without_none['lon'] = [g.longitude for g in df_without_none.gcode]

geometry = gpd.points_from_xy(df_without_none['lon'], df_without_none['lat'])
gdf = gpd.GeoDataFrame(df_without_none, geometry=geometry)

mask = df['gcode'].isnull()

new_df = df[mask].copy()

new_df.at[4, 'lat'] = 41.91703338166604
new_df.at[4, 'lon'] = -87.69738259997727

new_df.at[5, 'lat'] = 41.9170949145771
new_df.at[5, 'lon'] = -87.69742551532273

geometry = gpd.points_from_xy(new_df['lon'], new_df['lat'])

new_gdf = gpd.GeoDataFrame(new_df, geometry=geometry)

gdf = gdf.append(new_gdf, ignore_index = True)

gdf.to_file('ppindex/src/pp_partners_chicago.geojson', driver='GeoJSON')