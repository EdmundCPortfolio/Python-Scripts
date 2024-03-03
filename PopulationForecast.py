"""
File: PopulationForecast.py
Author: EC
Created: 2024-03-03

Description: 
The estimated population of England and Wales during 2023

Data source:
https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates
2011 to 2022
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Read the CSV file
file_path = r'E:\WNationalData\Data\MYEB2 (2023 Geography).csv'
df = pd.read_csv(file_path, sep=',', engine='python', encoding='unicode_escape', header=None, skiprows=1)

# Use the second row as the column names
column_names = df.iloc[0]
df.columns = column_names

# Remove the first row which isnt part of the dataset
df = df[1:]

# List of the columns containing the yearly populations 
year_columns_population = ['population_2011', 'population_2012', 'population_2013', 'population_2014',
                          'population_2015', 'population_2016', 'population_2017', 'population_2018',
                          'population_2019', 'population_2020', 'population_2021', 'population_2022']

# Convert population columns to numeric data types
for col in year_columns_population:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Unpivot the data
population_df = pd.melt(df, id_vars=['laname23', 'ladcode23'], value_vars=year_columns_population,
                        var_name='year', value_name='population')

# Convert the year column to a numeric value, removing the leading string
population_df['year'] = population_df['year'].str.extract(r'(\d+)').astype(int)

# Sum the total population for each year
yearly_population_totals = population_df.groupby(['year'])['population'].sum()

# Linear regression on the historical population data to estimate the population for the year 2023
X = yearly_population_totals.index.values.reshape(-1, 1)
y = yearly_population_totals.values
regressor = LinearRegression()
regressor.fit(X, y)
estimated_population_2023 = regressor.predict([[2023]])

# Scatter plot for total population
plt.figure(figsize=(8, 6))
plt.scatter(yearly_population_totals.index, yearly_population_totals.values, color='b', label='Year Population')
plt.scatter(2023, estimated_population_2023, color='r', label='Estimated Population (2023)')
plt.xlabel('Year')
plt.ylabel('Total Population (Millions)')
plt.title('England and Wales Population Trend (2011-2022) with 2023 Estimate')
plt.grid(True)
plt.legend()

# Add data labels for historic years
for year, population in zip(yearly_population_totals.index, yearly_population_totals.values):
    if year != 2023:
        plt.text(year, population, f'{population/1000000:.2f}M', color='black', ha='center', va='bottom')

# Add data label for 2023
plt.text(2023, estimated_population_2023[0], f'{estimated_population_2023[0]/1000000:.2f}M', color='black', ha='center', va='bottom')

plt.show()

print(f"Estimated population for 2023: {estimated_population_2023[0]:,.0f} million")
