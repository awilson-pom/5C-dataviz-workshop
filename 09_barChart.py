import plotly.express as px
import pandas as pd

# Sample data (resource allocation by community)
communities = ['Downtown', 'Northside', 'Eastside', 'Westside', 'Southside']
resources = [350000, 210000, 170000, 420000, 190000]
needs = [310000, 250000, 280000, 320000, 290000]

df = pd.DataFrame({
    'Community': communities,
    'Resources Allocated': resources,
    'Community Needs': needs
})

# Creating a grouped bar chart
fig = px.bar(
    df,
    x='Community',
    y=['Resources Allocated', 'Community Needs'],
    title='Resource Allocation vs. Community Needs',
    barmode='group',
    color_discrete_sequence=['#3366CC', '#DC3912']  # Custom colors
)

fig.show()