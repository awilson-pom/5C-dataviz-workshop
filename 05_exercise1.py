# Download a sample climate dataset
import pandas as pd

# This dataset contains climate change indicators
url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
climate_df = pd.read_csv(url)

# Filter to recent years and a few countries
countries = ['United States', 'China', 'India', 'Germany', 'Brazil']
recent_climate = climate_df[
    (climate_df['country'].isin(countries)) & 
    (climate_df['year'] >= 2000)
].copy()

# Take a look at the data
print(recent_climate[['country', 'year', 'co2', 'co2_per_capita']].head())

# EXERCISE:
# 1. Create a line chart showing CO2 emissions over time by country
# 2. Create a bar chart comparing per-capita emissions for the most recent year
# 3. Create a scatter plot relating GDP per capita to emissions per capita

# Sample solution for #1:
# plt.figure(figsize=(10, 6))
# for country in countries:
#     data = recent_climate[recent_climate['country'] == country]
#     plt.plot(data['year'], data['co2'], marker='o', label=country)
    
# plt.title('CO2 Emissions by Country')
# plt.xlabel('Year')
# plt.ylabel('CO2 Emissions (million tonnes)')
# plt.legend()
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()

# Now try #2 and #3 on your own!