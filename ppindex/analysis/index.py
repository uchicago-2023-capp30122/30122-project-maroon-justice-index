# Author : Diamon Dunlap
# Purpose : Computes the index for risk of period poverty by census tract

import requests
import pandas as pd

#### READ IN DATA #####
# main census data
census_df = pd.read_json('data/Census_Cook_County_dta.json')

# SNAP benefits income as a proxy for public asssistance income
snap_allowable = pd.read_csv('data/snap_allowable_income.csv')
snap_allowable = snap_allowable.iloc[:,:2]

snap_benefits = pd.read_csv('data/snap_benefits.csv')

snap_benefits = snap_benefits.iloc[:, :2]

# converting tracts to zip codes
# tract_zip = pd.read_csv('data/TRACT_ZIP_122021_crosswalk.csv')

# analysis
snap_income_per_month = pd.merge(snap_benefits, snap_allowable, on=['number_of_people_in_household'])
snap_income_per_month['total_monthly_income'] = snap_income_per_month.max_gross_monthly_income +\
                                                 snap_income_per_month.max_gross_monthly_benefits
snap_income_per_month_total = snap_income_per_month[['number_of_people_in_household', 'total_monthly_income']]

benefits_with = census_df[['geo_id',
                           'census_name', 
                           'county','tract',
                           'fam_1_with_snap',
                           'fam_2_with_snap',
                           'fam_3_with_snap',
                           'fam_4_with_snap',
                           'fam_5_with_snap',
                           'fam_6_with_snap',
                           'fam_7_with_snap']]

benefits_with = pd.melt(benefits_with, id_vars=['geo_id',
                                                'census_name',
                                                'county',
                                                'tract'])
benefits_with['number_of_people_in_household'] = benefits_with.variable.str.extract(r'(\d)')
benefits_with['number_of_people_in_household'] = benefits_with.number_of_people_in_household.astype("int")

# total public assistance INCOME (dollars) at census tract level
snap_income_per_tract = pd.merge(benefits_with, snap_income_per_month_total,\
                                  on=['number_of_people_in_household'], how='left')
snap_income_per_tract.drop(axis = 1, columns=['variable'])

snap_income_per_tract['total_public_assistance_income'] = snap_income_per_tract.value *\
                                                 snap_income_per_tract.total_monthly_income

snap_income_per_tract = snap_income_per_tract.drop(axis = 1, \
                                                   columns=['variable',
                                                            'number_of_people_in_household',
                                                            'total_monthly_income'])

snap_income_per_tract = snap_income_per_tract.groupby(['geo_id', 
                                                       'census_name',
                                                       'county',
                                                       'tract']).sum()

pop = census_df[["geo_id", "census_name", "county","tract","total_pop_in_tract"]]

snap_income_per_tract = pd.merge(snap_income_per_tract, pop, on=["geo_id", 
                                                                 "census_name", 
                                                                 "county",
                                                                 "tract"], how='left')

snap_income_per_tract.total_pop_in_tract = snap_income_per_tract.total_pop_in_tract.astype("float")

# percent of income spent on rent
rent = census_df[["geo_id", 
                  "census_name", 
                  "county","tract", 
                  "rent_percent_35_more",
                  "rent_percent_30_34_9", 
                  "rent_percent_25_29_9", 
                  "rent_percent_20_24_9",
                  "rent_percent_15_19_9", 
                  "rent_percent_15_less"]]

rent['weighted_avg'] = ((rent.rent_percent_35_more*37.5) + (rent.rent_percent_30_34_9*32.45) +\
                        (rent.rent_percent_25_29_9*27.45) + (rent.rent_percent_20_24_9*22.45) +\
                        (rent.rent_percent_15_19_9*17.45) + (rent.rent_percent_15_less*12.5)) / (rent.rent_percent_35_more+\
                                                                                                rent.rent_percent_30_34_9+\
                                                                                               rent.rent_percent_25_29_9+\
                                                                                               rent.rent_percent_20_24_9+\
                                                                                               rent.rent_percent_15_19_9+\
                                                                                               rent.rent_percent_15_less)
rent = rent.drop(columns=["rent_percent_35_more",
                          "rent_percent_30_34_9",
                          "rent_percent_25_29_9",
                          "rent_percent_20_24_9",
                          "rent_percent_15_19_9", 
                          "rent_percent_15_less"])

# total population on public assistance
median_inc = census_df[['geo_id', 'census_name', 'county', 'tract','median_income']]
median_inc = median_inc[median_inc.median_income>=0]
snap_income_pop_per_tract = pd.merge(snap_income_per_tract, median_inc, on=['geo_id', 
                                                                            'census_name',
                                                                            'county', 
                                                                            'tract'], how='left')
snap_income_pop_per_tract['non_pa_pop'] = snap_income_pop_per_tract['total_pop_in_tract'] - \
                                            snap_income_pop_per_tract['value']

snap_income_pop_per_tract['total_non_public_assitance_income'] = snap_income_pop_per_tract.median_income * \
                                                                    snap_income_pop_per_tract.non_pa_pop

snap_income_pop_per_tract['total_public_assistance_income'] = snap_income_pop_per_tract.total_public_assistance_income * 12

snap_income_pop_per_tract.rename(columns={'value':'pa_pop'}, inplace=True)

snap_income_pop_per_tract.drop('median_income',axis=1)

snap_income_pop_per_tract['pa_pop_percent'] = snap_income_pop_per_tract.pa_pop/snap_income_pop_per_tract.total_pop_in_tract

snap_income_pop_per_tract['non_pa_pop_percent'] = snap_income_pop_per_tract.non_pa_pop/snap_income_pop_per_tract.total_pop_in_tract

snap_income_pop_per_tract['total_income_per_tract'] = \
                (snap_income_pop_per_tract.pa_pop_percent*snap_income_pop_per_tract.total_public_assistance_income)+\
                (snap_income_pop_per_tract.non_pa_pop_percent*snap_income_pop_per_tract.total_non_public_assitance_income)

# disposable income
disposable_income = pd.merge(snap_income_pop_per_tract, rent, on=['geo_id',
                                                                  'census_name',
                                                                  'county',
                                                                  'tract'], how='left')

disposable_income['disposable_income'] = disposable_income.total_income_per_tract * (1 - (disposable_income.weighted_avg*0.01))                                                  

disposable_income['disposable_income_per_month'] = disposable_income.disposable_income/12

# eligible female, ages 12-44

sex_age = census_df[['geo_id',
                     'census_name',
                     'tract',
                     'county',
                     'total_population',
                     'total_female',
                     'total_female_10_to_14',
                     'total_female_15_to_17',
                     'total_female_18_to_19',
                     'total_female_20',
                     'total_female_21',
                     'total_female_22_to_24',
                     'total_female_25_to_29',
                     'total_female_30_to_34',
                     'total_female_35_to_39',
                     'total_female_40_to_44']]

sex_age['percent_female_pop'] = sex_age.total_female / sex_age.total_population
sex_age['total_eligible_women'] = sex_age.total_female_10_to_14 +\
                                  sex_age.total_female_15_to_17 +\
                                  sex_age.total_female_18_to_19 +\
                                  sex_age.total_female_20 +\
                                  sex_age.total_female_21 +\
                                  sex_age.total_female_22_to_24 +\
                                  sex_age.total_female_25_to_29 +\
                                  sex_age.total_female_30_to_34 +\
                                  sex_age.total_female_35_to_39 +\
                                  sex_age.total_female_40_to_44

sex_age_eligible = sex_age[['geo_id',
                            'census_name',
                            'county',
                            'tract',
                            'percent_female_pop',
                            'total_eligible_women']]

disposable_income_sex_age = pd.merge(disposable_income, sex_age_eligible, \
                                        on=['geo_id',
                                            'census_name',
                                            'county',
                                            'tract'], how='left')

disposable_income_sex_age['pp_index_raw'] = ((20 * disposable_income_sex_age.total_eligible_women)/\
                                                (disposable_income_sex_age.disposable_income_per_month * \
                                                        disposable_income_sex_age.percent_female_pop)) * 1000

disposable_income_sex_age['county_name'] = disposable_income_sex_age.census_name.str.extract(r'(\sCook\s)')
disposable_income_sex_age = disposable_income_sex_age.dropna()

# join to community center counts
comm_counts = pd.read_json('data/Tract_center_counts.json')

disposable_income_sex_age = pd.merge(disposable_income_sex_age, comm_counts, on=['tract'], how='left')
disposable_income_sex_age['number_of_centers'] = disposable_income_sex_age['number_of_centers'].fillna(0)

def down_weighting(x):
    if x >= 15:
        return 0.5
    elif x >= 10 and x <=14:
        return (1 - 0.35)
    elif x >= 5 and x <=9:
        return (1 - 0.20)
    elif x >= 1 and x <=4:
        return (1 - 0.05)
    else:
        return 1

disposable_income_sex_age['down_weight'] = disposable_income_sex_age['number_of_centers'].apply(lambda x: down_weighting(x))
disposable_income_sex_age['pp_index'] = disposable_income_sex_age.pp_index_raw * disposable_income_sex_age.down_weight

# normalize the data
disposable_income_sex_age['pp_index'] = (disposable_income_sex_age.pp_index - disposable_income_sex_age.pp_index.min())/ \
                (disposable_income_sex_age.pp_index.max() - disposable_income_sex_age.pp_index.min())


# disposable_income_sex_age['pp_index'] = (disposable_income_sex_age.pp_index - disposable_income_sex_age.pp_index.mean())/ \
#                                                 disposable_income_sex_age.pp_index.std()


# export to json
# MAP 1
disposable_income_sex_age.to_json(path_or_buf='data/pp_index.json')