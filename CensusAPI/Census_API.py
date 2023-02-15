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
        cols = ['B01001_026E','B01001_029E','B01001_030E',\
        "B01001_031E", "B01001_032E", "B01001_033E", \
        "B01001_034E", "B01001_035E", "B01001_036E", \
        "B01001_037E", "B01001_038E", 'S1701_C03_001E']

        #identify columns that are found in the subject tables
        subject_columns, macro_columns = self.classify_columns(cols)
        print(macro_columns)

        full_url_macro = f'{self.base_url_macro_table}?get={macro_columns}&for={geo}&in=state:{state}&key={self.census_key}'
        data_response_macro = requests.get(full_url_macro)
        full_json = data_response_macro.json()
        df = pd.DataFrame(full_json[1:], columns=full_json[0]).rename(
            columns={
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
            "B01001_038E": "total_female_40_to_44"
            }
        )
        df = df.astype(
            dtype={
            "total_female": 'int64', 
            "total_female_10_to_14": 'int64'
            }
        )
        # df = df.assign(
        #     internet_rate = 100 * (df.tot_hhld_int / df.tot_hhld),
        #     emp_rate_25_64 = 100 - df.unemp_rate_25_64,
        #     above_pov_rate = 100 - df.pov_rate
        # )
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
            print(column)
            if column.startswith("S"):
                subject_columns.append(column)
            elif column.startswith("B"):
                macro_columns.append(column)

        
        return (",".join(subject_columns), ",".join(macro_columns))

cols = 'B01001_026E,B01001_029E'
geo = 'tract:*'
state = '17'

api = CensusAPI("7527e32c66997745264cf65a96efac91e01e1b5b")
df = api.get_data(cols, geo, state)