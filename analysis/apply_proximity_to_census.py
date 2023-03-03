'''
CAPP 122: Project Maroon Justice Index
Jimena Salinas
Code for applying the proximity_anlysis function
to all the Census tracts and resourcer centers, and
updating the master analysis file
'''

from analysis.proximity import proximity_analysis
import geopandas as gpd
import pandas as pd
import geopandas as gpd


class CensusTractCentroids:
    """
    This class finds the centroids for each Census tract
    and applies the proximity analysis function to estimate
    proximity to resource centers.
    """

    def __init__(self):
        """
        Initializes the class by reading a GeoJSON file with data for 
        all the Census tracts in Illinois.
        """
        self.tracts_geo = gpd.read_file(
            "src/boundaries_census_tracts_2010.geojson")

    def get_centroids(self):
        """
        This function uses the built-in GeoPandas 'centroid', 'x', and 'y
        attributes to obtain the centroids for each tract in the 
        GeoDataFrame

        Returns:
            - Dictionary of coordinates by tract: (dict) a dictionary mapping
            each Illinois Census tract to a tuple with the latitude and 
            longitude of the tract's centroid .
        """
        centroids = {}
        for row in self.tracts_geo.itertuples():
            centroid = row.geometry.centroid
            tract = row.tractce10
            lat = centroid.y
            lon = centroid.x
            centroids[tract] = (lat, lon)
        return centroids

    def apply_prox_to_census(self):
        """

        """
        centroids_census = self.get_centroids()
        number_of_centers = {}
        for tract, coordinates in centroids_census.items():
            lat, long = coordinates
            centers_count = proximity_analysis(lat, long)
            number_of_centers[tract] = centers_count
        return number_of_centers

    def merge_dict_to_dataframe(self):
        """

        """
        tract_centers_df = pd.DataFrame.from_dict(
            self.apply_prox_to_census(), orient='index', columns=['number_of_centers'])
        tract_centers_df = tract_centers_df.reset_index().rename(columns={
            'index': 'tract'})
        return tract_centers_df


        # TO DO: run Betty's function
centroids = CensusTractCentroids().get_centroids()
centroids
centers = CensusTractCentroids()
centers.merge_dict_to_dataframe()