"""Programme to read in the original data files from the Penn World Table 7.1
and prepare the data for the use across different modules.

"""

import pandas as pd
import pickle

import csv

from bld.project_paths import project_paths_join as ppj

# Read in the csv file.
data_pwt = pd.read_csv(ppj('IN_DATA', 'pwt71_wo_country_names_wo_g_vars.csv'))
data = data_pwt[['isocode', 'year', 'rgdpwok', 'POP']]

# Exclude official Chinese statistics from data set as corrected data is
# included as 'CH2'
data_pwt = data_pwt[data_pwt['isocode'] != 'CHN']
data = data[data['isocode'] != 'CHN']

# Restrict data to some specified years.
# years = list(range(1970, 2011))
years = [1970, 1980, 1990, 2000, 2010]
data = data[data['year'].isin(years)].dropna()

# Check which countries have entries for specified the years.
country_duplicates = {}
for country in data['isocode'].unique():
    country_duplicates[country] = (
        list(data['isocode']).count(country) == len(years)
    )

# Create list of the countries with entries for all specified years
countries = []
for country in sorted(country_duplicates.keys()):
    if country_duplicates[country] is True:
        countries.append(country)
    else:
        pass

print(
    'Number of countries with entries for all specified years:', len(countries)
)
# Restrict data to countries for which data is available for the specified
# years.
data = data[(data['isocode'].isin(countries) == True)]

# Calculate percentage of world population which is about 7.4 billion people
# and total number of countries in the world which is 195.
pop_incl = sum(data[(data['year'] == 2010)]['POP'])
print('Share of total number of countries:', len(countries) / 195)
print('Percentage of world population:', pop_incl / 7400000)

# Save the results in pickle object.
with open(ppj('OUT_DATA', 'data_pwt71.pickle'), 'wb') as f_results:
    pickle.dump(data, f_results)

with open(ppj('OUT_DATA', 'years_pwt.pickle'), 'wb') as f_years:
    pickle.dump(years, f_years)

with open(ppj('OUT_DATA', 'countries.csv'), 'w') as f_countries:
    wr = csv.writer(f_countries, quoting=csv.QUOTE_ALL)
    for country in sorted(countries):
        wr.writerow([country])
