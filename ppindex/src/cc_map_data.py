import pandas as pd
import geopandas as gpd
from .geocode_pp_partners_chicago import gdf

joined = gpd.read_file("ppindex/src/comm_centers_neighborhoods.geojson")
joined = joined[["Community Center", "Type", "Category", "Neighborhood", 
                 "Address", "Contact", "Note", "gcode", "lat", "lon",
                 "geometry"]]

gdf = gdf.rename(columns={"Name":"Community Center"})

joined = joined.append(gdf, ignore_index = True)