'''
CAPP 122: Project Maroon Justice Index
Jimena Salinas
Code for applying the proximity_anlysis function
to all the Census tracts and resource centers, and
updating the master analysis file
'''

from ppindex.analysis.proximity import proximity_analysis
import geopandas as gpd
import pandas as pd
import geopandas as gpd


class CensusTractCentroids:
    """
    This class finds the centroids for each Census tract
    and applies the proximity analysis function to estimate
    proximity to resource centers.
    """
    DIRECTORY = "ppindex/data"

    def __init__(self):
        """
        Initializes the class by reading a GeoJSON file with data for 
        all the Census tracts in Illinois.
        """
        self.tracts_geo = gpd.read_file(
            "ppindex/src/boundaries_census_tracts_2010.geojson")

    def get_centroids(self):
        """
        This function uses the built-in GeoPandas 'centroid', 'x', and 'y
        attributes to obtain the centroids for each tract in the 
        GeoDataFrame
        Inputs:
            - None
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
        This function calls the get_centroids method
        to find the total number of resource centers
        from each Census tract.
        Inputs:
            - None
        Returns:
            - A dictionary mapping each Census tract
              to the total number of resource centers 
              at a walking distance.
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
        This function calls the apply_prox_to_census method
        and merges a dictionary containing census tracts mapped
        to number of resources to the master analysis Pandas dataframe.
        Inputs:
            - None
        Returns:
            - A new Pandas dataframe with an additional column 
            containing the number of resource centers per tract.
        """
        tract_centers_df = pd.DataFrame.from_dict(
            self.apply_prox_to_census(), orient='index', columns=['number_of_centers'])
        tract_centers_df = tract_centers_df.reset_index().rename(columns={
            'index': 'tract'})
        return tract_centers_df

    def export_dataframe_to_json(self):
        """
        This function exports the Pandas dataframe with center
        access information at the tract level to a JSON file.
        Inputs:
            None
        Returns:
            None
        """
        # Construct the full path to the file
        export_as = self.DIRECTORY + "/Tract_center_counts.json"
        dataframe = self.merge_dict_to_dataframe()
        dataframe.to_json(export_as, orient='records')
        return dataframe


# Call class and export center access information for index computation
centers = CensusTractCentroids()
centers.export_dataframe_to_json()
