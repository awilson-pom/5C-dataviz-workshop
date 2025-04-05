import plotly.express as px
import pandas as pd

# Sample data (could be climate data, student outcomes, etc.)
df = pd.DataFrame({
    'Year': range(2010, 2023),
    'Temperature': [14.4, 14.5, 14.8, 14.9, 15.2, 15.5, 
                   15.8, 15.9, 16.1, 16.3, 16.5, 16.7, 16.9],
    'Region': ['Global']*13
})

# Create an interactive line chart
fig = px.line(
    df, 
    x='Year', 
    y='Temperature', 
    title='Global Temperature Trend',
    markers=True  # Show markers on the line
)

# Display the figure
fig.show()