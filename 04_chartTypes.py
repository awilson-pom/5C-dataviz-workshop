import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the aesthetic style
sns.set(style="whitegrid")

# Create a figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Bar chart example for resource allocation (top left)
regions = ['Urban', 'Suburban', 'Rural']
resources = [75, 45, 30]
sns.barplot(x=regions, y=resources, ax=axes[0, 0])
axes[0, 0].set_title('Resource Allocation by Region')
axes[0, 0].set_ylabel('Funding ($ millions)')

# Line chart for environmental data (top right)
years = range(2015, 2023)
emissions = [100, 95, 93, 88, 82, 75, 68, 60]
axes[0, 1].plot(years, emissions, marker='o', linewidth=2)
axes[0, 1].set_title('Carbon Emissions Reduction')
axes[0, 1].set_xlabel('Year')
axes[0, 1].set_ylabel('Relative Emissions (%)')

# Scatter plot for education outcomes (bottom left)
investment = np.random.uniform(500, 2000, 50)
outcomes = 0.5 * investment + np.random.normal(0, 200, 50)
sns.scatterplot(x=investment, y=outcomes, ax=axes[1, 0])
axes[1, 0].set_title('Education Investment vs. Outcomes')
axes[1, 0].set_xlabel('Investment per Student ($)')
axes[1, 0].set_ylabel('Average Test Score')

# Map-style visualization placeholder (bottom right)
# In a real implementation, you might use geopandas or folium
axes[1, 1].text(0.5, 0.5, 'Geographic Visualization\n(Using geopandas or folium)',
                ha='center', va='center', fontsize=12)
axes[1, 1].set_title('Resource Distribution Map')
axes[1, 1].axis('off')

plt.tight_layout()
plt.show()