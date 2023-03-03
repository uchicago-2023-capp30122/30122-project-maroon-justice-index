'''
CAPP 122: Project Maroon Justice Index
Jimena Salinas
Code for calling the US Census API and constructing 
a JSON data file
'''

import requests
import pandas as pd


class CensusAPI:
    """
    This class extracts US Census Data.
    """
    DIRECTORY = "30122-project-maroon-justice-index/data"

    def __init__(self, census_key):
        """
        This function initializes a new instance of the CensusAPI class.

        Inputs:
            - census_key : (str) A string representing the 
        API key needed to access the US Census Bureau API. A key
        can be obtained from the US Census webpage. For more info visit:
        https://www.census.gov/data/developers/guidance/api-user-guide.html
        """
        self.census_key = census_key
        self.base_url_macro_table = 'https://api.census.gov/data/2019/acs/acs5'
        self.base_url_profile_table = 'https://api.census.gov/data/2019/acs/acs5/profile'

    def get_data(self, geo, state):
        """
        This method extracts data from the US Census Bureau API 
        for the specified geographic location and state.

        Inputs:
            - geo : (str) A string representing the
              geographic location to retrieve data for.
            - state : (str) A string representing the 
            state to retrieve data for.

        Returns:
            - dataframe: (Pandas dataframe) A DataFrame containing 
            the data retrieved from the US Census Bureau API.
        """
        cols = ["GEO_ID",
                "NAME",
                "B01001_001E",
                'B01001_026E',
                'B01001_029E',
                'B01001_030E',
                "B01001_031E",
                "B01001_032E",
                "B01001_033E",
                "B01001_034E",
                "B01001_035E",
                "B01001_036E",
                "B01001_037E",
                "B01001_038E",
                "B18135_023E",
                "B18135_022E",
                "B19001_002E",
                "B19001_003E",
                "B19001_004E",
                "B19001_005E",
                "B19001_006E",
                "B19001_007E",
                "B19001_008E",
                "B19001_009E",
                "B19001_010E",
                "B19001_011E",
                "B19058_002E",
                "B19058_003E",
                "B09010_001E",
                "B01003_001E",
                "B09010_002E",
                "B19013_001E",
                "B19123_001E",
                "B19123_002E",
                "B19123_005E",
                "B19123_008E",
                "B19123_011E",
                "B19123_014E",
                "B19123_017E",
                "B19123_020E",
                "DP04_0142PE",
                "DP04_0141PE",
                "DP04_0140PE",
                "DP04_0139PE",
                "DP04_0138PE",
                "DP04_0137PE"
                ]

        # identify columns that are found in the profile tables
        profile_columns, macro_columns = self.classify_columns(cols)

        # macro data
        full_url_macro = f'{self.base_url_macro_table}?get={macro_columns}&for={geo}&in=state:{state}&key={self.census_key}'
        data_response_macro = requests.get(full_url_macro)

        # profile data
        full_url_profile = f'{self.base_url_profile_table}?get={profile_columns}&for={geo}&in=state:{state}&key={self.census_key}'
        data_response_profile = requests.get(full_url_profile)

        full_json = data_response_macro.json()
        profile_json = data_response_profile.json()

        # Convert JSON data to Pandas dataframes
        full_df = pd.DataFrame(full_json[1:], columns=full_json[0])
        profile_df = pd.DataFrame(profile_json[1:], columns=profile_json[0])

        # Merge dataframes on county and tract
        merged_df = pd.merge(full_df, profile_df, on=['county', 'tract'])

        merged_df = merged_df.rename(
            columns={
                "GEO_ID": "geo_id",
                "NAME": "census_name",
                "B01001_001E": "total_population",
                "B01001_026E": "total_female",
                "B01001_029E": "total_female_10_to_14",
                "B01001_030E": "total_female_15_to_17",
                "B01001_031E": "total_female_18_to_19",
                "B01001_032E": "total_female_20",
                "B01001_033E": "total_female_21",
                "B01001_034E": "total_female_22_to_24",
                "B01001_035E": "total_female_25_to_29",
                "B01001_036E": "total_female_30_to_34",
                "B01001_037E": "total_female_35_to_39",
                "B01001_038E": "total_female_40_to_44",
                "B18135_023E": "total_19_to_64_no_health_insurance",
                "B18135_022E": "total_19_to_64_public_health_insurance",
                "B19001_002E": "total_no_income",
                "B19001_003E": "total_with_income",
                "B19001_004E": "total_with_income_level1",
                "B19001_005E": "total_with_income_level2",
                "B19001_006E": "total_with_income_level3",
                "B19001_007E": "total_with_income_level4",
                "B19001_008E": "total_with_income_level5",
                "B19001_009E": "total_with_income_level6",
                "B19001_010E": "total_with_income_level7",
                "B19001_011E": "total_with_income_level8",
                "B19058_002E": "total_receives_stamps_snap",
                "B19058_003E": "no_stamps_snap",
                "B09010_001E": "receipt_stamps_snap",
                "B09010_002E": "receipt_stamps_snap_household",
                "B19123_001E": "total_assistance",
                "B19013_001E": "median_income",
                "B01003_001E": "total_pop_in_tract",
                "B19123_002E": "fam_1_with_snap",
                "B19123_005E": "fam_2_with_snap",
                "B19123_008E": "fam_3_with_snap",
                "B19123_011E": "fam_4_with_snap",
                "B19123_014E": "fam_5_with_snap",
                "B19123_017E": "fam_6_with_snap",
                "B19123_020E": "fam_7_with_snap",
                "DP04_0142PE": "rent_percent_35_more",
                "DP04_0141PE": "rent_percent_30_34_9",
                "DP04_0140PE": "rent_percent_25_29_9",
                "DP04_0139PE": "rent_percent_20_24_9",
                "DP04_0138PE": "rent_percent_15_19_9",
                "DP04_0137PE": "rent_percent_15_less"})

        merged_df = merged_df.astype(
            dtype={
                "total_population": 'int64',
                "total_female": 'int64',
                "total_female_10_to_14": 'int64',
                "total_female_15_to_17": 'int64',
                "total_female_18_to_19": 'int64',
                "total_female_20": 'int64',
                "total_female_21": 'int64',
                "total_female_22_to_24": 'int64',
                "total_female_25_to_29": 'int64',
                "total_female_30_to_34": 'int64',
                "total_female_35_to_39": 'int64',
                "total_female_40_to_44": 'int64',
                "total_19_to_64_no_health_insurance": 'int64',
                "total_19_to_64_public_health_insurance": 'int64',
                "total_no_income": 'int64',
                "total_with_income": 'int64',
                "total_with_income_level1": 'int64',
                "total_with_income_level2": 'int64',
                "total_with_income_level3": 'int64',
                "total_with_income_level4": 'int64',
                "total_with_income_level5": 'int64',
                "total_with_income_level6": 'int64',
                "total_with_income_level7": 'int64',
                "total_with_income_level8": 'int64',
                "total_receives_stamps_snap": 'int64',
                "no_stamps_snap": 'int64',
                "receipt_stamps_snap": 'int64',
                "receipt_stamps_snap_household": 'int64',
                "total_assistance": 'int64',
                "median_income": 'int64',
                "fam_1_with_snap": 'int64',
                "fam_2_with_snap": 'int64',
                "fam_3_with_snap": 'int64',
                "fam_4_with_snap": 'int64',
                "fam_5_with_snap": 'int64',
                "fam_6_with_snap": 'int64',
                "fam_7_with_snap": 'int64',
                "total_pop_in_tract": 'int64'
            }
        )
        merged_df['total_female_mentrual_age'] = merged_df[['total_female_10_to_14',
                                                            'total_female_15_to_17', 'total_female_18_to_19',
                                                            'total_female_20', 'total_female_21', 'total_female_22_to_24',
                                                            'total_female_25_to_29', 'total_female_30_to_34',
                                                            'total_female_35_to_39',
                                                            'total_female_40_to_44']].apply(sum, axis=1)

        merged_df = merged_df.assign(
            percentage_female_menstrual_age=(
                merged_df.total_female_mentrual_age / merged_df.total_female)
        )
        return self.move_key_columns_to_front(merged_df)

    def classify_columns(self, column_lst):
        """
        This function takes a list of column names from the US Census,
        and classifies the columns in those belonging to the profile tables
        of the general Census macro table.
        Inputs: 
            - A list of column names (lst)
        Returns:
            - A a tuple with a list of profile column and macro columns
            (tuple)
        """
        profile_columns = []
        macro_columns = []

        for column in column_lst:
            if column.startswith("DP"):
                profile_columns.append(column)
            else:
                macro_columns.append(column)

        return (",".join(profile_columns), ",".join(macro_columns))

    def move_key_columns_to_front(self, dataframe):
        """
        This function moves the geo columns to the front of the table
        to improve readability
        Inputs:
            - dataframe (Pandas dataframe)
        Returns:
            - a dataframe with re-ordered columns
        """
        cols_to_move = ['tract', 'county']
        dataframe = dataframe[cols_to_move +
                              [col for col in dataframe.columns if col not in cols_to_move]]
        return dataframe

    def export_dataframe_to_json(self, dataframe):
        """
        This function exports a Pandas dataframe to a JSON file.

        Inputs:
            dataframe (pandas.DataFrame): The dataframe to export.
            filename (str): The name of the file to save the JSON data to.

        Returns:
            None
        """
        # Construct the full path to the file
        export_as = self.DIRECTORY + "/Census_Cook_County_dta.json"
        print(export_as)
        dataframe.to_json(export_as, orient='records')


# Produce Data sets and save as JSON
geo = 'tract:*'
state = '17'

api = CensusAPI("7527e32c66997745264cf65a96efac91e01e1b5b")
merged_df = api.get_data(geo, state)

# export dataframe
api.export_dataframe_to_json(merged_df)