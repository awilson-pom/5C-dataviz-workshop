import plotly.express as px

# Load sample dataset (built into plotly)
df = px.data.gapminder().query("year==2007")

# Create scatter plot with multiple dimensions
fig = px.scatter(
    df,
    x='gdpPercap',           # X-axis: GDP per capita
    y='lifeExp',             # Y-axis: Life expectancy
    size='pop',              # Point size: Population
    color='continent',       # Point color: Continent
    hover_name='country',    # Main tooltip label
    log_x=True,              # Log scale for x-axis
    title='Global Development in 2007'
)

fig.show()