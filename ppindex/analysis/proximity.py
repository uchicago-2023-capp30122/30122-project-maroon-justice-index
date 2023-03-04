'''
Author: Betty
Date: 2/28/23
'''

import json
import pandas as pd
import geopandas as gpd

def proximity_analysis(lat=41.854, lon=-87.71):
    """
    Takes a pair of latitude & longitude coordinates and returns the number of
    IDHS offices/service providers within an approx 1 mile (1609 meters) radius 
    """

    # create dataframe for centroid with latitude and longitude as attributes
    centroid_df = pd.DataFrame({'Latitude': [lat], 'Longitude': [lon]})

    # generate geometry of shapely Point geometries from x, y(, z) coordinates
    gdf = gpd.GeoDataFrame(
        centroid_df, geometry=gpd.points_from_xy(centroid_df.Longitude,
                                                     centroid_df.Latitude), 
        crs = "EPSG:4326")

    # convert crs to UTM zone 16T to create buffer
    # ref: https://www.latlong.net/lat-long-utm.html and https://epsg.io/32616
    gdf = gdf.to_crs("EPSG:32616")  

    # create buffer geometry and convert 1 mile into meters (~1609 meters)
    gdf['buffergeometry1mile'] = gdf['geometry'].buffer(1609) 
    gdf.set_geometry('buffergeometry1mile',inplace=True)

    # convert crs back to EPSG:4326 to match community centers crs
    gdf = gdf.to_crs("EPSG:4326")

    comm_centers = gpd.read_file("src/comm_centers_neighborhoods.geojson")
    comm_centers = comm_centers.to_crs("EPSG:4326")

    # create intersection dataframe of community centers within 1 mile radius
    # of centroid coordinates
    intersect_df = gpd.overlay(gdf, comm_centers, how='intersection', keep_geom_type=False)

    # to view comm_centers plot: comm_centers.plot()
    # to view gdf plot: gdf.plot()
    # to view intersect_df: intersect_df.plot()

    return len(intersect_df)