'''
CAPP 122: Project Maroon Justice Index
Jimena Salinas
Code for merging our index data set with the
geojson file, so our visualizations can show
neighborhood name in the hover function.
'''

import pandas as pd
import geopandas as gpd

def prep_viz_data():

    # Data prep
    pp_dta = pd.read_json("ppindex/data/pp_index.json")

    census_geo0 = gpd.read_file('ppindex/src/census_tract_with_neigh_names.geojson')

    #covert geopandas data frame to a regular dataframe for merging
    census_geo = pd.DataFrame(census_geo0)
    census_geo

    # # # add per capita disposable monthly income
    pp_dta["avg_disposable_income_per_month"] = pp_dta["disposable_income_per_month"] / pp_dta['total_pop_in_tract']

    # Rename the "tractce10" column to "tract" for consistency with the pp_dta file
    census_geo['tractce10'] = census_geo['tractce10'].astype(str)
    pp_dta['tract'] = pp_dta['tract'].astype(str)
    census_geo.rename(columns={'tractce10': 'tract'}, inplace=True)
    census_geo = census_geo.loc[:, ['tract', 'neighborhood_name']]

    # # # Merge the two dataframes using the "tract" column
    pp_dta = pd.merge(left=pp_dta, right=census_geo, on='tract', how='left')
    pp_dta

    pp_dta.columns
    pp_dta = pp_dta.loc[:, ['tract', 'neighborhood_name', 'pp_index', 'disposable_income_per_month', 
                            'avg_disposable_income_per_month', 'total_eligible_women', 'total_pop_in_tract',
                            'number_of_centers']]

    pp_dta.to_json("ppindex/data/index_data_for_scatter.json", orient='records')



prep_viz_data()