import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create some test data
data = pd.DataFrame({
    'x': np.random.normal(0, 1, 100),
    'y': np.random.normal(0, 1, 100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})

# Create a simple plot
plt.figure(figsize=(8, 6))
sns.scatterplot(data=data, x='x', y='y', hue='category')
plt.title('Test Plot')
plt.show()

print("If you see a plot above, your setup is complete!")