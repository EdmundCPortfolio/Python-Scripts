import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


# Interest rates data source
url = 'https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp'

page = requests.get(url)

# Check for response 200
print(page)

# Webpage parse tree 
web_tree = BeautifulSoup(page.text, 'html.parser')

# Select the table of index rates
table = web_tree.find_all('table')[0]

# Grab column titles
col_titles = table.find_all('th')

# Remove leading whitespace from the column titles
col_titles_cleaned = [title.text.strip() for title in col_titles]

# Create an empty DataFrame with col_titles_cleaned as column names
df = pd.DataFrame(columns=col_titles_cleaned)

# Extract the rows from the table
rows = table.find_all('tr')

# Iterate over each row
for row in rows:
    # Get the columns in each row
    cols = row.find_all('td')
    # Get the text from each column
    cols = [col.text.strip() for col in cols]
    # Check if cols is not empty
    if cols:
        # Create a dictionary with the data in cols and the column titles
        data_dict = dict(zip(col_titles_cleaned, cols))
        # Add the data to the DataFrame
        df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)

print(df)

#filename = 'rates.csv'
# Write the combined data to a CSV file
#df.to_csv(filename, index=False, encoding='utf-8')

# Convert Date column to datetime
df['Date Changed'] = pd.to_datetime(df['Date Changed'])

# Sort by date
df = df.sort_values('Date Changed')

# Convert Rate column to numeric
df['Rate'] = pd.to_numeric(df['Rate'])

# Create a step plot
plt.figure(figsize=(10, 6))
plt.step(df['Date Changed'], df['Rate'], where='post')

# Set the title and labels
plt.title ('Bank of England\'s Bank Rate over time')
plt.xlabel('Date Changed')
plt.ylabel('Bank Rate')

# Display the plot
plt.show()





