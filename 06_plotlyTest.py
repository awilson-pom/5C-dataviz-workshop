import plotly.express as px  # Simplified API (recommended for beginners)
import plotly.graph_objects as go  # More customizable but complex

# Example data
import pandas as pd
import numpy as np

# Create sample data
data = pd.DataFrame({
    'x': range(10),
    'y': np.random.randn(10).cumsum(),
    'category': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
})