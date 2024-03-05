"""
File: JSON_FuelPrices.py
Author: EC
Created: 2024-03-05

Description: 
Script fetches fuel price data from multiple URLs, combines it into a DataFrame and exports as  CSV.

Data source:
https://www.gov.uk/guidance/access-fuel-price-data

"""

import requests
import json
import pandas as pd
from datetime import datetime

# List of URLs to fetch JSON data from
urls = [
    'https://applegreenstores.com/fuel-prices/data.json',
    'https://fuelprices.asconagroup.co.uk/newfuel.json',
    'https://storelocator.asda.com/fuel_prices_data.json',
    'https://www.bp.com/en_gb/united-kingdom/home/fuelprices/fuel_prices_data.json',
    'https://fuelprices.esso.co.uk/latestdata.json',
    'https://www.morrisons.com/fuel-prices/fuel.json',
    'https://moto-way.com/fuel-price/fuel_prices.json',
    'https://fuel.motorfuelgroup.com/fuel_prices_data.json',
    'https://www.rontec-servicestations.co.uk/fuel-prices/data/fuel_prices_data.json',
    'https://api.sainsburys.co.uk/v1/exports/latest/fuel_prices_data.json',
    'https://www.sgnretail.uk/files/data/SGN_daily_fuel_prices.json',
    'https://www.shell.co.uk/fuel-prices-data.html'

]

# Get todays date
now = datetime.now()

# Format date as string
date_string = now.strftime("%Y%m%d")

# Create empty DataFrame
combined_df = pd.DataFrame()

# Load data from each URL and append to DataFrame
for url in urls:
    response = requests.get(url)
    data = json.loads(response.text)
    df = pd.DataFrame(data['stations'])
    df['Data_Source_URL'] = url  # Add a new column for the URL
    df['Last_Updated'] = pd.to_datetime(data['last_updated'], format='%d/%m/%Y %H:%M:%S') 
    combined_df = combined_df.append(df, ignore_index=True)

# Extract latitude and longitude into separate columns
combined_df['latitude'] = combined_df['location'].apply(lambda loc: loc['latitude'])
combined_df['longitude'] = combined_df['location'].apply(lambda loc: loc['longitude'])

# Extract petrol prices into separate columns
combined_df['B7_price'] = combined_df['prices'].apply(lambda p: p.get('B7'))
combined_df['E5_price'] = combined_df['prices'].apply(lambda p: p.get('E5'))
combined_df['E10_price'] = combined_df['prices'].apply(lambda p: p.get('E10'))

# Drop the original 'location' and 'prices' columns
combined_df.drop(columns=['location', 'prices'], inplace=True)

# Construct filename of file to be exported
filename = 'Fuel_Prices' + '_' + date_string + '.csv'

print(filename)

# Write the combined data to a CSV file
combined_df.to_csv(filename, index=False, encoding='utf-8')

print(f"Data exported, please see file named {filename}")
