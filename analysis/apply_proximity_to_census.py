'''
CAPP 122: Project Maroon Justice Index
Jimena Salinas
Code for applying the proximity_anlysis function
to all the Census tracts and resourcer centers, and
updating the master analysis file
'''

from analysis.proximity import proximity_analysis
import geopandas as gpd


class CensusTractCentroids:
    """
    This class finds the centroids for each Census tract
    and applied the proximity analysis function to estimate
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
        GeoDaraFrame

        Returns:
            - List of tuples: (list) a list of tuples with 
            the latitude and longitude of a tract centroid.
        """
        centroids = []
        for row in self.tracts_geo.itertuples():
            centroid = row.geometry.centroid
            lat = centroid.y
            lon = centroid.x
            centroids.append((lat, lon))
        return centroids


# TO DO: run Betty's function
centroids = CensusTractCentroids().get_centroids()
centroids
