import requests
import pandas as pd


class CensusAPI:
    """
    This class extracts US Census Data
    """
    def __init__(self, census_key):
        self.census_key = census_key
        self.base_url_subject_tables = 'https://api.census.gov/data/2021/acs/acs5/subject'
        self.base_url_macro_table = 'https://api.census.gov/data/2021/acs/acs5'
        
    def get_data(self, cols, geo, state):
        cols = ["B01001_001E",'B01001_026E','B01001_029E','B01001_030E',\
        "B01001_031E", "B01001_032E", "B01001_033E", \
        "B01001_034E", "B01001_035E", "B01001_036E", \
        "B01001_037E", "B01001_038E", "B18135_023E", \
        "B18135_022E", "B19001_002E", "B19001_003E",\
        "B19001_004E", "B19001_005E", "B19001_006E",\
        "B19001_007E", "B19001_008E", "B19001_009E"]
        # "B19001_0010E", "B19001_0011E",'S1701_C03_001E']

        #identify columns that are found in the subject tables
        subject_columns, macro_columns = self.classify_columns(cols)

        full_url_macro = f'{self.base_url_macro_table}?get={macro_columns}&for={geo}&in=state:{state}&key={self.census_key}'
        data_response_macro = requests.get(full_url_macro)
        full_json = data_response_macro.json()
        df = pd.DataFrame(full_json[1:], columns=full_json[0]).rename(
            columns={
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
            "B19001_009E": "total_with_income_level6"
            # "B19001_0010E": "total_with_income_level7",
            # "B19001_0011E": "total_with_income_level8"
            }
        )
        df = df.astype(
            dtype={
            "total_population" :'int64',
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
            # "total_with_income_level7": 'int64',
            # "total_with_income_level8": 'int64'
            }
        )
        df['total_female_mentrual_age'] = df[['total_female_10_to_14', \
                         'total_female_15_to_17', 'total_female_18_to_19',
                         'total_female_20', 'total_female_21', 'total_female_22_to_24',
                         'total_female_25_to_29', 'total_female_30_to_34', \
                         'total_female_35_to_39',
                         'total_female_40_to_44']].apply(sum, axis=1)

        df = df.assign(
            percentage_female_menstrual_age = (df.total_female_mentrual_age/ df.total_female)
        )
        return df
    
    def classify_columns(self, column_lst):
        """
        This function takes a list of column names from the US Census,
        and classifies the columns in those belonging to the Subject tables
        of the general Census macro table.
        Inputs: 
            - A list of column names (lst)
        Returns:
            - A a tuple with a list of subject column and macro columns
            (tuple)
        """
        subject_columns = []
        macro_columns = []

        for column in column_lst:
            if column.startswith("S"):
                subject_columns.append(column)
            elif column.startswith("B"):
                macro_columns.append(column)

        
        return (",".join(subject_columns), ",".join(macro_columns))


# Produce Data sets and save as JSON
cols = 'B01001_026E,B01001_029E'
geo = 'tract:*'
state = '17'

api = CensusAPI("7527e32c66997745264cf65a96efac91e01e1b5b")
df = api.get_data(cols, geo, state)