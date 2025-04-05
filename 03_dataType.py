import pandas as pd
import numpy as np

# Sample DataFrame representing renewable energy adoption
data = {
    'Region': ['North', 'South', 'East', 'West', 'Central'],
    'Solar_Capacity_MW': [150, 320, 110, 280, 90],
    'Wind_Capacity_MW': [420, 100, 350, 270, 150],
    'Year': pd.date_range(start='2020-01-01', periods=5, freq='Y')
}

df = pd.DataFrame(data)
print(df)

# Add a calculated column
df['Total_Capacity_MW'] = df['Solar_Capacity_MW'] + df['Wind_Capacity_MW']
print(df)