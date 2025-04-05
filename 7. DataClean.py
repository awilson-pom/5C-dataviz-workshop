#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Set our visual style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create sample data
np.random.seed(42)
dates = [datetime(2023, 1, 1) + timedelta(days=x) for x in range(365)]
data = {
    'date': dates,
    'productid': [f'PROD{i:03d}' for i in range(1, 366)],
    'quantity': np.random.randint(1, 100, 365),
    'price': np.random.uniform(10, 1000, 365).round(2),
    'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], 365),
    'store_id': np.random.choice(['S01', 'S02', 'S03', 'S04'], 365)
}

df = pd.DataFrame(data)
print("Original clean dataset head:")
print(df.head())


# In[ ]:


# Missing Values

# Create missing values
df_missing = df.copy()
df_missing.loc[10:30, 'quantity'] = None  # Python None
df_missing.loc[40:60, 'price'] = np.nan   # NumPy NaN
df_missing.loc[70:90, 'category'] = ''    # Empty string

print("Dataset with missing values:")
print("\nMissing value counts:")
print(df_missing.isnull().sum())
print("\nSample rows with missing values:")
print(df_missing[df_missing.isnull().any(axis=1)].head())

# Visualize missing values
plt.figure(figsize=(10, 6))
sns.heatmap(df_missing.isnull(), yticklabels=False, cbar=False)
plt.title('Missing Values Pattern')
plt.show()


# In[ ]:


# Inconsistent Formats

df_inconsistent = df.copy()

# Create various date format inconsistencies
df_inconsistent['date_string'] = df_inconsistent['date'].astype(str)
df_inconsistent.loc[50:100, 'date_string'] = df_inconsistent.loc[50:100, 'date'].dt.strftime('%m/%d/%Y')
df_inconsistent.loc[101:150, 'date_string'] = df_inconsistent.loc[101:150, 'date'].dt.strftime('%Y-%m-%d')
df_inconsistent.loc[151:200, 'date_string'] = df_inconsistent.loc[151:200, 'date'].dt.strftime('%d-%b-%Y')
df_inconsistent.loc[201:250, 'date_string'] = df_inconsistent.loc[201:250, 'date'].dt.strftime('%B %d, %Y')

# Create category inconsistencies
df_inconsistent.loc[100:150, 'category'] = df_inconsistent.loc[100:150, 'category'].str.lower()  # lowercase
df_inconsistent.loc[151:200, 'category'] = df_inconsistent.loc[151:200, 'category'].str.upper()  # UPPERCASE
df_inconsistent.loc[201:250, 'category'] = df_inconsistent.loc[201:250, 'category'].str.title()  # Title Case

# Add some common misspellings and variations
category_variations = {
    'Electronics': ['electronic', 'Electronics', 'ELECTRONICS', 'electroNics', 'electron.'],
    'Clothing': ['clothing', 'CLOTHING', 'Cloths', 'clothes', 'apparels'],
    'Food': ['food', 'FOOD', 'Foods', 'F00d', 'food items'],
    'Books': ['books', 'BOOKS', 'Book', 'BOOKs', 'bks']
}

for i, (category, variations) in enumerate(category_variations.items()):
    df_inconsistent.loc[251+i*10:251+i*10+len(variations)-1, 'category'] = variations

print("Examples of inconsistent formats:\n")

print("1. Date Format Variations:")
print("-" * 50)
sample_dates = df_inconsistent['date_string'].iloc[
    [0, 60, 120, 180, 220]  # Sample indices for different formats
].reset_index(drop=True)
print(sample_dates)

print("\n2. Category Inconsistencies:")
print("-" * 50)
print("Sample of different category formats:")
print(df_inconsistent['category'].value_counts().head(12))

# Visualize category inconsistencies
plt.figure(figsize=(12, 6))
category_counts = df_inconsistent['category'].value_counts()
plt.bar(range(len(category_counts.head(12))), category_counts.head(12))
plt.xticks(range(len(category_counts.head(12))), category_counts.head(12).index, rotation=45, ha='right')
plt.title('Frequency of Category Variations')
plt.xlabel('Category')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

print("\n3. Impact of Inconsistent Formats:")
print("-" * 50)
print(f"Total unique category values (should be 4): {len(df_inconsistent['category'].unique())}")
print("\nUnique category values found:")
for idx, cat in enumerate(sorted(df_inconsistent['category'].unique()), 1):
    print(f"{idx}. '{cat}'")


# In[ ]:


# Mixed Data Types

df_mixed = df.copy()
df_mixed['mixed_quantity'] = df_mixed['quantity'].astype(str)
df_mixed.loc[200:250, 'mixed_quantity'] = 'out_of_stock'
df_mixed.loc[251:300, 'mixed_quantity'] = 'back_ordered'

print("Mixed data types example:")
print("\nUnique values in mixed_quantity:")
print(df_mixed['mixed_quantity'].value_counts().head())
print("\nData type:", df_mixed['mixed_quantity'].dtype)


# In[ ]:


# Incorrect Values

df_incorrect = df.copy()
df_incorrect.loc[300:320, 'quantity'] = -100  # Impossible negative quantities
df_incorrect.loc[321:340, 'price'] = 0        # Zero prices
df_incorrect.loc[341:360, 'store_id'] = 'UNKNOWN'  # Invalid store ID

print("Examples of incorrect values:")
print("\nNegative quantities:")
print(df_incorrect[df_incorrect['quantity'] < 0].head())
print("\nZero prices:")
print(df_incorrect[df_incorrect['price'] == 0].head())
print("\nInvalid store IDs:")
print(df_incorrect[df_incorrect['store_id'] == 'UNKNOWN'].head())


# In[ ]:


# Outliers

df_outliers = df.copy()

# Create different types of outliers
# 1. Extreme high values (possibly data entry errors)
df_outliers.loc[150:155, 'price'] = 999999.99  # Unrealistic prices
df_outliers.loc[156:160, 'quantity'] = 99999   # Impossible quantities

# 2. Moderate outliers (possibly real but unusual)
df_outliers.loc[161:170, 'price'] = 5000  # Expensive but possible items
df_outliers.loc[171:180, 'quantity'] = 500 # Large but possible orders

# 3. Low-end outliers
df_outliers.loc[181:185, 'price'] = 0.01  # Extremely low prices
df_outliers.loc[186:190, 'quantity'] = 1   # Minimal quantities

# Create visualizations to understand outliers
plt.figure(figsize=(15, 10))

# 1. Box plots to show outlier distribution
plt.subplot(2, 2, 1)
sns.boxplot(y=df_outliers['price'])
plt.title('Price Distribution with Outliers')
plt.ylabel('Price ($)')

plt.subplot(2, 2, 2)
sns.boxplot(y=df_outliers['quantity'])
plt.title('Quantity Distribution with Outliers')
plt.ylabel('Quantity')

# 2. Histograms to show frequency distribution
plt.subplot(2, 2, 3)
sns.histplot(data=df_outliers, x='price', bins=50)
plt.title('Price Histogram')
plt.xlabel('Price ($)')
plt.ylabel('Frequency')

plt.subplot(2, 2, 4)
sns.histplot(data=df_outliers, x='quantity', bins=50)
plt.title('Quantity Histogram')
plt.xlabel('Quantity')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# Calculate and show statistical measures for outlier detection
def analyze_outliers(series, column_name):
    """Analyze outliers using different statistical methods"""
    # Calculate basic statistics
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Calculate z-scores
    z_scores = (series - series.mean()) / series.std()
    
    print(f"\nOutlier Analysis for {column_name}:")
    print("-" * 50)
    print(f"Basic Statistics:")
    print(f"Mean: {series.mean():.2f}")
    print(f"Median: {series.median():.2f}")
    print(f"Standard Deviation: {series.std():.2f}")
    print(f"\nIQR Method Boundaries:")
    print(f"Q1 (25th percentile): {Q1:.2f}")
    print(f"Q3 (75th percentile): {Q3:.2f}")
    print(f"IQR: {IQR:.2f}")
    print(f"Lower bound: {lower_bound:.2f}")
    print(f"Upper bound: {upper_bound:.2f}")
    
    # Count outliers
    iqr_outliers = series[(series < lower_bound) | (series > upper_bound)]
    z_score_outliers = series[abs(z_scores) > 3]
    
    print(f"\nOutlier Detection:")
    print(f"Number of outliers (IQR method): {len(iqr_outliers)}")
    print(f"Number of outliers (Z-score method): {len(z_score_outliers)}")
    
    if len(iqr_outliers) > 0:
        print(f"\nExample outlier values ({column_name}):")
        print(iqr_outliers.head().to_string())

# Analyze outliers in both columns
analyze_outliers(df_outliers['price'], 'Price')
analyze_outliers(df_outliers['quantity'], 'Quantity')

# Show impact of outliers on summary statistics
print("\nImpact of Outliers on Summary Statistics:")
print("-" * 50)
print("\nWith Outliers:")
print(df_outliers[['price', 'quantity']].describe())

# Remove outliers for comparison
df_no_outliers = df_outliers.copy()
for column in ['price', 'quantity']:
    Q1 = df_no_outliers[column].quantile(0.25)
    Q3 = df_no_outliers[column].quantile(0.75)
    IQR = Q3 - Q1
    df_no_outliers = df_no_outliers[
        (df_no_outliers[column] >= Q1 - 1.5 * IQR) & 
        (df_no_outliers[column] <= Q3 + 1.5 * IQR)
    ]

print("\nWithout Outliers:")
print(df_no_outliers[['price', 'quantity']].describe())


# In[ ]:


# Cleaning

def clean_data(df):
    print("Starting data cleaning process...")
    df_clean = df.copy()
    
    # 1. Handle missing values
    print("\n1. Handling missing values...")
    missing_before = df_clean.isnull().sum()
    df_clean['quantity'] = df_clean['quantity'].fillna(df_clean['quantity'].median())
    df_clean['price'] = df_clean['price'].fillna(df_clean['price'].median())
    df_clean['category'] = df_clean['category'].fillna('Unknown')
    missing_after = df_clean.isnull().sum()
    
    print("Missing values before:")
    print(missing_before)
    print("\nMissing values after:")
    print(missing_after)
    
    # 2. Standardize formats
    print("\n2. Standardizing formats...")
    print("Sample of categories before standardization:")
    print(df_clean['category'].value_counts().head())
    
    df_clean['date_parsed'] = pd.to_datetime(df_clean['date_string'], format='mixed')
    df_clean['category'] = df_clean['category'].str.title()
    
    print("\nSample of categories after standardization:")
    print(df_clean['category'].value_counts().head())
    
    # 3. Fix incorrect values
    print("\n3. Fixing incorrect values...")
    incorrect_counts_before = {
        'negative_quantities': len(df_clean[df_clean['quantity'] < 0]),
        'zero_prices': len(df_clean[df_clean['price'] == 0]),
        'unknown_stores': len(df_clean[df_clean['store_id'] == 'UNKNOWN'])
    }
    
    df_clean.loc[df_clean['quantity'] < 0, 'quantity'] = 0
    df_clean.loc[df_clean['price'] == 0, 'price'] = df_clean['price'].median()
    df_clean.loc[df_clean['store_id'] == 'UNKNOWN', 'store_id'] = 'S01'
    
    incorrect_counts_after = {
        'negative_quantities': len(df_clean[df_clean['quantity'] < 0]),
        'zero_prices': len(df_clean[df_clean['price'] == 0]),
        'unknown_stores': len(df_clean[df_clean['store_id'] == 'UNKNOWN'])
    }
    
    print("Incorrect values before cleaning:")
    print(incorrect_counts_before)
    print("\nIncorrect values after cleaning:")
    print(incorrect_counts_after)
    
    # 4. Handle outliers using IQR method
    print("\n4. Handling outliers...")
    def remove_outliers(series):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return series.clip(lower=lower_bound, upper=upper_bound)
    
    print("Before outlier removal:")
    print(df_clean[['price', 'quantity']].describe())
    
    df_clean['price'] = remove_outliers(df_clean['price'])
    df_clean['quantity'] = remove_outliers(df_clean['quantity'])
    
    print("\nAfter outlier removal:")
    print(df_clean[['price', 'quantity']].describe())
    
    return df_clean


# In[ ]:


# Results

# Combine all issues into one dataset
df_problems = df.copy()  # Start with fresh copy

# 1. Add missing values
df_problems.loc[10:30, 'quantity'] = None
df_problems.loc[40:60, 'price'] = np.nan
df_problems.loc[70:90, 'category'] = ''

# 2. Add inconsistent formats
df_problems['date_string'] = df_problems['date'].astype(str)
df_problems.loc[50:100, 'date_string'] = df_problems.loc[50:100, 'date'].dt.strftime('%m/%d/%Y')
df_problems.loc[101:150, 'date_string'] = df_problems.loc[101:150, 'date'].dt.strftime('%Y-%m-%d')
df_problems.loc[100:200, 'category'] = df_problems.loc[100:200, 'category'].str.lower()

# 3. Add incorrect values
df_problems.loc[300:320, 'quantity'] = -100
df_problems.loc[321:340, 'price'] = 0
df_problems.loc[341:360, 'store_id'] = 'UNKNOWN'

# 4. Add outliers
df_problems.loc[150:155, 'price'] = 999999.99
df_problems.loc[156:160, 'quantity'] = 99999

# Clean the data
print("Starting data cleaning demonstration...")
df_cleaned = clean_data(df_problems)

# Visualize the results
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# Price distribution before and after
sns.boxplot(y=df_problems['price'], ax=ax1)
ax1.set_title('Original Price Distribution')
ax1.set_ylabel('Price ($)')

sns.boxplot(y=df_cleaned['price'], ax=ax2)
ax2.set_title('Cleaned Price Distribution')
ax2.set_ylabel('Price ($)')

# Quantity distribution before and after
sns.boxplot(y=df_problems['quantity'], ax=ax3)
ax3.set_title('Original Quantity Distribution')
ax3.set_ylabel('Quantity')

sns.boxplot(y=df_cleaned['quantity'], ax=ax4)
ax4.set_title('Cleaned Quantity Distribution')
ax4.set_ylabel('Quantity')

plt.tight_layout()
plt.show()

# Compare summary statistics
print("\nSummary Statistics Comparison:")
print("\nOriginal Data Summary:")
print(df_problems[['price', 'quantity']].describe())
print("\nCleaned Data Summary:")
print(df_cleaned[['price', 'quantity']].describe())

# Show the impact of cleaning on the dataset size
print(f"\nOriginal dataset size: {len(df_problems)}")
print(f"Cleaned dataset size: {len(df_cleaned)}")

# Show the number of unique categories before and after cleaning
print(f"\nUnique categories before cleaning: {df_problems['category'].nunique()}")
print(f"Unique categories after cleaning: {df_cleaned['category'].nunique()}")

