#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed for reproducibility
np.random.seed(42)
n_samples = 1000

# Generate data with intentional missing values
data = {
    'numeric_uniform': np.random.uniform(0, 100, n_samples),
    'numeric_normal': np.random.normal(50, 15, n_samples),
    'categorical': np.random.choice(['A', 'B', 'C', 'D'], n_samples),
    'dates': pd.date_range(start='2023-01-01', periods=n_samples, freq='D')
}

df = pd.DataFrame(data)

# Introduce missing values with different patterns
df.loc[10:50, 'numeric_uniform'] = np.nan  # Consecutive missing
df.loc[np.random.choice(n_samples, 100), 'numeric_normal'] = np.nan  # Random missing
df.loc[500:600, 'categorical'] = np.nan  # Block missing
df.loc[np.random.choice(n_samples, 50), 'dates'] = pd.NaT  # Time missing

print("Dataset with missing values:")
print(df.head(10))
print("\nMissing value summary:")
print(df.isnull().sum())

# Visualize missing values pattern
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), yticklabels=False, cbar=False)
plt.title('Missing Values Pattern')
plt.show()


# In[ ]:


# Removing Missing Values
# =============================
"""
Demonstrate different ways to remove missing values from the dataset.
"""

print("Original shape:", df.shape)

# Method 1: Remove all rows with any missing values
df_dropped_all = df.dropna()
print("\nShape after dropping all rows with any missing values:", df_dropped_all.shape)

# Method 2: Remove rows with missing values in specific columns
df_dropped_subset = df.dropna(subset=['numeric_normal'])
print("Shape after dropping rows with missing numeric_normal:", df_dropped_subset.shape)

# Method 3: Keep rows with at least n non-null values
df_dropped_thresh = df.dropna(thresh=3)
print("Shape after keeping rows with at least 3 non-null values:", df_dropped_thresh.shape)

# Visualize results
methods = ['Original', 'Drop All', 'Drop Subset', 'Drop Threshold']
counts = [len(df), len(df_dropped_all), len(df_dropped_subset), len(df_dropped_thresh)]

plt.figure(figsize=(10, 6))
plt.bar(methods, counts)
plt.title('Impact of Different Dropping Methods')
plt.ylabel('Number of Rows')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[ ]:


# Simple Imputation Methods
# ==============================
"""
Demonstrate simple imputation methods using basic statistics.
"""

# Create copies for different imputation methods
df_mean = df.copy()
df_median = df.copy()
df_mode = df.copy()
df_constant = df.copy()

# Mean imputation
df_mean['numeric_normal'] = df['numeric_normal'].fillna(df['numeric_normal'].mean())

# Median imputation
df_median['numeric_normal'] = df['numeric_normal'].fillna(df['numeric_normal'].median())

# Mode imputation for categorical
df_mode['categorical'] = df['categorical'].fillna(df['categorical'].mode()[0])

# Constant imputation
df_constant['numeric_normal'] = df['numeric_normal'].fillna(0)

# Visualize numeric imputation results
plt.figure(figsize=(12, 6))
plt.hist(df['numeric_normal'].dropna(), bins=30, alpha=0.5, label='Original (non-missing)')
plt.hist(df_mean['numeric_normal'], bins=30, alpha=0.5, label='Mean Imputation')
plt.hist(df_median['numeric_normal'], bins=30, alpha=0.5, label='Median Imputation')
plt.hist(df_constant['numeric_normal'], bins=30, alpha=0.5, label='Zero Imputation')
plt.title('Distribution of Different Imputation Methods')
plt.legend()
plt.tight_layout()
plt.show()


# In[ ]:


# Sequential Imputation Methods
# =================================
"""
Demonstrate forward fill and backward fill methods.
"""

# Create copy for sequential imputation
df_seq = df.copy()

# Forward fill
df_seq['forward_fill'] = df_seq['numeric_normal'].copy()
df_seq['forward_fill'] = df_seq['forward_fill'].ffill()

# Backward fill
df_seq['backward_fill'] = df_seq['numeric_normal'].copy()
df_seq['backward_fill'] = df_seq['backward_fill'].bfill()

# Combine both methods
df_seq['both_fill'] = df_seq['numeric_normal'].copy()
df_seq['both_fill'] = df_seq['both_fill'].ffill().bfill()

# Visualize sequential imputation
plt.figure(figsize=(15, 6))
sample_range = slice(20, 70)  # Select a range with missing values

plt.plot(df_seq.index[sample_range], 
         df_seq['numeric_normal'].iloc[sample_range], 
         'o-', label='Original', alpha=0.5)
plt.plot(df_seq.index[sample_range], 
         df_seq['forward_fill'].iloc[sample_range], 
         's-', label='Forward Fill')
plt.plot(df_seq.index[sample_range], 
         df_seq['backward_fill'].iloc[sample_range], 
         '^-', label='Backward Fill')
plt.plot(df_seq.index[sample_range], 
         df_seq['both_fill'].iloc[sample_range], 
         'D-', label='Both Fill')

plt.title('Comparison of Sequential Imputation Methods')
plt.legend()
plt.grid(True)
plt.show()


# In[ ]:


# Interpolation Methods
# ==========================
"""
Demonstrate different interpolation methods for handling missing values.
"""

# Create copy for interpolation
df_interp = df.copy()

# Linear interpolation
df_interp['linear'] = df_interp['numeric_normal'].interpolate(method='linear')

# Polynomial interpolation
df_interp['polynomial'] = df_interp['numeric_normal'].interpolate(method='polynomial', order=2)

# Nearest interpolation
df_interp['nearest'] = df_interp['numeric_normal'].interpolate(method='nearest')

# Visualize interpolation methods
plt.figure(figsize=(15, 6))
sample_range = slice(20, 70)  # Select a range with missing values

plt.plot(df_interp.index[sample_range], 
         df_interp['numeric_normal'].iloc[sample_range], 
         'o-', label='Original', alpha=0.5)
plt.plot(df_interp.index[sample_range], 
         df_interp['linear'].iloc[sample_range], 
         's-', label='Linear')
plt.plot(df_interp.index[sample_range], 
         df_interp['polynomial'].iloc[sample_range], 
         '^-', label='Polynomial')
plt.plot(df_interp.index[sample_range], 
         df_interp['nearest'].iloc[sample_range], 
         'D-', label='Nearest')

plt.title('Comparison of Interpolation Methods')
plt.legend()
plt.grid(True)
plt.show()


# In[ ]:


# Statistical Comparison
# ==========================
"""
Compare statistical properties of different imputation methods.
"""

stats_df = pd.DataFrame({
    'Original': df['numeric_normal'].dropna().describe(),
    'Mean': df_mean['numeric_normal'].describe(),
    'Median': df_median['numeric_normal'].describe(),
    'Forward Fill': df_seq['forward_fill'].describe(),
    'Linear Interp': df_interp['linear'].describe()
})

print("Statistical Comparison of Different Methods:")
print(stats_df)

# Visualize distributions
plt.figure(figsize=(12, 6))
methods = ['Original', 'Mean', 'Median', 'Forward Fill', 'Linear Interp']
data = [df['numeric_normal'].dropna(),
        df_mean['numeric_normal'],
        df_median['numeric_normal'],
        df_seq['forward_fill'],
        df_interp['linear']]

plt.boxplot(data, tick_labels=methods)
plt.title('Distribution Comparison of Different Imputation Methods')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[ ]:




