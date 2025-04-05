import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set random seed for reproducibility
np.random.seed(42)

# Create synthetic data on educational inequality
# ----------------------------------------------

# 1. School district funding data by income quintile
income_levels = ['Lowest 20%', 'Low-Mid 20%', 'Middle 20%', 'Mid-High 20%', 'Highest 20%']
funding_per_student = [8500, 9200, 10800, 12500, 16000]
teacher_salary = [45000, 48000, 52000, 58000, 65000]
class_size = [28, 26, 23, 20, 18]
resources_index = [35, 42, 58, 72, 85]

district_df = pd.DataFrame({
    'Income Level': income_levels,
    'Funding per Student ($)': funding_per_student,
    'Average Teacher Salary ($)': teacher_salary,
    'Average Class Size': class_size,
    'Resources Index': resources_index
})

# 2. Student outcome data by district resources
num_districts = 100
resources = np.random.normal(60, 20, num_districts)
resources = np.clip(resources, 20, 100)  # Keep in reasonable range

# Student outcomes are correlated with resources but with some noise
noise = np.random.normal(0, 10, num_districts)
math_scores = 40 + 0.5 * resources + noise
reading_scores = 45 + 0.45 * resources + np.random.normal(0, 8, num_districts)

# Income levels affect outcomes beyond just resources
income_effect = np.random.choice([10, 20, 30, 40, 50], num_districts)
income_label = np.random.choice(income_levels, num_districts)

# Create district dataset
outcomes_df = pd.DataFrame({
    'District ID': range(1, num_districts + 1),
    'Resources Index': resources.round(1),
    'Math Score': math_scores.round(1),
    'Reading Score': reading_scores.round(1),
    'Income Level': income_label,
    'Income Effect': income_effect
})

# 3. Performance gap trend data over time (years)
years = list(range(2000, 2023))
num_years = len(years)

# Create widening performance gap over time
high_income_trend = 75 + np.cumsum(np.random.normal(0.2, 0.1, num_years))
low_income_trend = 65 + np.cumsum(np.random.normal(0.05, 0.1, num_years))

# Create trend dataframe
trend_data = []
for i, year in enumerate(years):
    trend_data.append({'Year': year, 'Income Group': 'High Income', 'Score': high_income_trend[i]})
    trend_data.append({'Year': year, 'Income Group': 'Low Income', 'Score': low_income_trend[i]})

trend_df = pd.DataFrame(trend_data)

# 4. Intervention impact data
interventions = [
    "Nutrition\nPrograms",  # Added line breaks to intervention names
    "Extended\nLearning",
    "Technology\nAccess",
    "Teacher\nPay",
    "Reduce\nClass Size"
]

# Different interventions have different effectiveness
before_scores = [60, 64, 61, 62, 63]
after_scores = [71, 72, 67, 68, 70]
costs = [500, 1500, 800, 1200, 1800]  # Per student cost

intervention_df = pd.DataFrame({
    'Intervention': interventions,
    'Before Score': before_scores,
    'After Score': after_scores,
    'Score Improvement': [a - b for a, b in zip(after_scores, before_scores)],
    'Cost per Student ($)': costs,
    'ROI': [(a - b) / c * 100 for a, b, c in zip(after_scores, before_scores, costs)]
})

# Create the dashboard with improved layout and fixed overlapping
# ---------------------------------------------------------------
fig = make_subplots(
    rows=2, 
    cols=2,
    subplot_titles=(
        "School Funding Disparities by District Income Level",
        "Student Achievement vs. School Resources",
        "Achievement Gap Over Time",
        "Effectiveness of Interventions"
    ),
    specs=[
        [{"type": "bar"}, {"type": "scatter"}],
        [{"type": "scatter"}, {"type": "bar"}]
    ],
    vertical_spacing=0.15,  # Increased spacing to prevent overlap
    horizontal_spacing=0.08,
    row_heights=[0.5, 0.5]  # Equal height rows
)

# Panel 1: School funding disparity (top left)
fig.add_trace(
    go.Bar(
        x=district_df['Income Level'],
        y=district_df['Funding per Student ($)'],
        marker_color='#1f77b4',
        name='Funding per Student',
        width=0.6  # Slightly narrower bars
    ),
    row=1, col=1
)

# Add annotation explaining the disparity - fixed positioning
fig.add_annotation(
    text="Highest-income districts receive nearly<br>twice the funding of lowest-income districts",
    x="Mid-High 20%",  # Moved annotation to different position
    y=16500,  # Positioned above the highest bar
    showarrow=True,
    arrowhead=1,
    ax=-20,
    ay=-60,
    font=dict(size=10, color="black"),
    bgcolor="rgba(255, 255, 255, 0.9)",
    bordercolor="black",
    borderwidth=1,
    align="center",
    row=1, col=1
)

# Panel 2: Student achievement vs resources (top right)
colorscale = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

for i, income in enumerate(income_levels):
    subset = outcomes_df[outcomes_df['Income Level'] == income]
    fig.add_trace(
        go.Scatter(
            x=subset['Resources Index'],
            y=subset['Math Score'],
            mode='markers',
            name=income,
            marker=dict(
                size=10,
                opacity=0.7,
                color=colorscale[i]
            )
        ),
        row=1, col=2
    )

# Add trendline for overall relationship
all_resources = outcomes_df['Resources Index']
all_scores = outcomes_df['Math Score']
z = np.polyfit(all_resources, all_scores, 1)
p = np.poly1d(z)
x_line = np.array([min(all_resources), max(all_resources)])
y_line = p(x_line)

fig.add_trace(
    go.Scatter(
        x=x_line,
        y=y_line,
        mode='lines',
        line=dict(color='black', dash='dash', width=2),
        name='Trend Line',
        showlegend=False
    ),
    row=1, col=2
)

# Add annotation explaining the correlation - fixed positioning
fig.add_annotation(
    text="Students in well-resourced schools<br>consistently perform better,<br>regardless of income level",
    x=30,  # Moved to left side of chart
    y=75,  # Moved to top area with fewer data points
    showarrow=True,
    arrowhead=1,
    ax=40,
    ay=20,
    font=dict(size=10, color="black"),
    bgcolor="rgba(255, 255, 255, 0.9)",
    bordercolor="black",
    borderwidth=1,
    align="center",
    row=1, col=2
)

# Panel 3: Achievement gap over time (bottom left)
fig.add_trace(
    go.Scatter(
        x=trend_df[trend_df['Income Group'] == 'High Income']['Year'],
        y=trend_df[trend_df['Income Group'] == 'High Income']['Score'],
        mode='lines',
        name='High Income',
        line=dict(width=3, color='#1f77b4')
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=trend_df[trend_df['Income Group'] == 'Low Income']['Year'],
        y=trend_df[trend_df['Income Group'] == 'Low Income']['Score'],
        mode='lines',
        name='Low Income',
        line=dict(width=3, color='#ff7f0e')
    ),
    row=2, col=1
)

# Calculate the gap at the beginning and end
start_gap = (
    trend_df[(trend_df['Income Group'] == 'High Income') & (trend_df['Year'] == 2000)]['Score'].values[0] -
    trend_df[(trend_df['Income Group'] == 'Low Income') & (trend_df['Year'] == 2000)]['Score'].values[0]
)

end_gap = (
    trend_df[(trend_df['Income Group'] == 'High Income') & (trend_df['Year'] == 2022)]['Score'].values[0] -
    trend_df[(trend_df['Income Group'] == 'Low Income') & (trend_df['Year'] == 2022)]['Score'].values[0]
)

# Add area to highlight the gap
high_years = trend_df[trend_df['Income Group'] == 'High Income']['Year']
high_scores = trend_df[trend_df['Income Group'] == 'High Income']['Score']
low_years = trend_df[trend_df['Income Group'] == 'Low Income']['Year']
low_scores = trend_df[trend_df['Income Group'] == 'Low Income']['Score']

fig.add_trace(
    go.Scatter(
        x=pd.concat([high_years, low_years[::-1]]),
        y=pd.concat([high_scores, low_scores[::-1]]),
        fill='toself',
        fillcolor='rgba(200, 200, 200, 0.3)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        hoverinfo='skip'
    ),
    row=2, col=1
)

# Add annotation explaining the widening gap - fixed positioning
fig.add_annotation(
    text="Gap widened from {:.1f} to {:.1f} points<br>({:.1f}% increase)".format(
        start_gap, end_gap, ((end_gap-start_gap)/start_gap*100)),
    x=2000,  # Moved to left side
    y=78,    # Positioned at top of chart
    showarrow=True,
    arrowhead=1,
    ax=30,
    ay=15,
    font=dict(size=10, color="black"),
    bgcolor="rgba(255, 255, 255, 0.9)",
    bordercolor="black",
    borderwidth=1,
    align="center",
    row=2, col=1
)

# Add vertical reference line at 2010
fig.add_vline(
    x=2010, 
    line_width=1.5,
    line_dash="dot", 
    line_color="gray",
    row=2,
    col=1
)

fig.add_annotation(
    text="2010 policy change<br>did not reduce gap",
    x=2012,  # Adjusted position
    y=62,    # Moved to bottom area
    showarrow=False,
    font=dict(size=9, color="gray"),
    align="center",
    bgcolor="rgba(255, 255, 255, 0.8)",
    row=2, col=1
)

# Panel 4: Intervention effectiveness (bottom right)
intervention_df_sorted = intervention_df.sort_values('ROI', ascending=False)

fig.add_trace(
    go.Bar(
        x=intervention_df_sorted['Intervention'],
        y=intervention_df_sorted['ROI'],
        marker_color='#2ca02c',
        name='Return on Investment',
        width=0.5  # Narrower bars to prevent label overlap
    ),
    row=2, col=2
)

# Add cost labels with cleaner positioning
for i, intervention in enumerate(intervention_df_sorted['Intervention']):
    cost = intervention_df_sorted.iloc[i]['Cost per Student ($)']
    improvement = intervention_df_sorted.iloc[i]['Score Improvement']
    
    # Position costs above the bars, better spaced
    fig.add_annotation(
        text="${}<br>+{} pts".format(cost, improvement),
        x=intervention,
        y=intervention_df_sorted.iloc[i]['ROI'] + 1.2,  # More space above bars
        showarrow=False,
        font=dict(size=9),
        bgcolor="rgba(255, 255, 255, 0.8)",
        align="center",
        row=2, col=2
    )

# Add annotation explaining the interventions - fixed positioning
fig.add_annotation(
    text="Targeted interventions show promising<br>returns, especially nutrition programs",
    x=intervention_df_sorted['Intervention'].iloc[0],
    y=10,  # Positioned in middle of chart
    showarrow=True,
    arrowhead=1,
    ax=0,
    ay=-30,
    font=dict(size=10, color="black"),
    bgcolor="rgba(255, 255, 255, 0.9)",
    bordercolor="black",
    borderwidth=1,
    align="center",
    row=2, col=2
)

# Update layout with better spacing and sizing
fig.update_layout(
    title={
        'text': "Educational Inequality: Causes, Trends, and Solutions",
        'y':0.98,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24)
    },
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(size=11)
    ),
    height=900,  # Increased height
    width=1200,
    template="plotly_white",
    margin=dict(t=120, l=80, r=40, b=150),  # Increased top and bottom margins
    plot_bgcolor='rgba(250,250,250,0.9)'
)

# Subtitle with more space below title
fig.add_annotation(
    text="This dashboard examines disparities in school funding and their impacts on student outcomes",
    xref="paper",
    yref="paper",
    x=0.5,
    y=0.995,  # Positioned closer to title
    showarrow=False,
    font=dict(size=14),
    opacity=0.8,
    align="center"
)

# Update subplot titles with numbers but avoid overlap with plots
for i, annotation in enumerate(fig['layout']['annotations'][:4]):  # First 4 annotations are subplot titles
    annotation['text'] = "<b>{}.</b> {}".format(i+1, annotation['text'])
    annotation['font'] = dict(size=13)
    annotation['y'] = annotation['y'] - 0.02  # Move titles up slightly

# Add big arrows to show the narrative flow - improved positioning
arrow_specs = [
    # From panel 1 to panel 2
    dict(x=0.49, y=0.73, ax=30, ay=0),
    # From panel 2 to panel 3
    dict(x=0.75, y=0.52, ax=0, ay=-30),
    # From panel 3 to panel 4
    dict(x=0.49, y=0.27, ax=-30, ay=0)
]

for spec in arrow_specs:
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=spec['x'],
        y=spec['y'],
        text="",
        showarrow=True,
        axref="pixel",
        ayref="pixel",
        ax=spec['ax'],
        ay=spec['ay'],
        arrowhead=3,
        arrowsize=1.8,
        arrowwidth=2.5,
        arrowcolor="#e377c2"
    )

# Update axes labels with better positioning
fig.update_xaxes(title_text="District Income Level", title_font=dict(size=12), row=1, col=1)
fig.update_xaxes(title_text="School Resources Index", title_font=dict(size=12), row=1, col=2)
fig.update_xaxes(title_text="Year", title_font=dict(size=12), row=2, col=1)
fig.update_xaxes(title_text="Intervention Type", title_font=dict(size=12), row=2, col=2)
fig.update_xaxes(tickangle=0, row=2, col=2)  # Keep intervention labels horizontal

fig.update_yaxes(title_text="Funding per Student ($)", title_font=dict(size=12), row=1, col=1)
fig.update_yaxes(title_text="Math Achievement Score", title_font=dict(size=12), row=1, col=2)
fig.update_yaxes(title_text="Average Test Score", title_font=dict(size=12), row=2, col=1)
fig.update_yaxes(title_text="Return on Investment (%)", title_font=dict(size=12), row=2, col=2)

# Set ranges to prevent overcrowding
fig.update_yaxes(range=[8000, 18000], row=1, col=1)
fig.update_xaxes(range=[20, 105], row=1, col=2)
fig.update_yaxes(range=[35, 85], row=1, col=2)
fig.update_yaxes(range=[60, 85], row=2, col=1)
fig.update_yaxes(range=[0, 23], row=2, col=2)

# Show the figure
fig.show()

# To save as an HTML file:
# fig.write_html("educational_inequality_dashboard.html")