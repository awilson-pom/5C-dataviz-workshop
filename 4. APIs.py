#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
import time
from datetime import datetime
import json

# Set up API base URL
BASE_URL = "https://api.github.com"


# In[ ]:


def basic_request():
    """Basic GET request to GitHub's public API"""
    print("=== Basic Request Demo ===\n")
    
    # Request pandas repository issues
    url = f"{BASE_URL}/repos/pandas-dev/pandas/issues"
    response = requests.get(url)
    
    # Print response details
    print(f"Status Code: {response.status_code}")
    print(f"Response Type: {type(response.json())}")
    print(f"Number of items: {len(response.json())}")
    
    # Show first issue details
    first_issue = response.json()[0]
    print("\nFirst Issue Details:")
    print(f"Title: {first_issue['title']}")
    print(f"State: {first_issue['state']}")
    print(f"Number: {first_issue['number']}")
    
    return response.json()

# Run basic request
issues = basic_request()


# In[ ]:


def error_handling_demo():
    """Demonstrate proper API error handling"""
    print("=== Error Handling Demo ===\n")
    
    def make_request(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Error connecting: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error: {timeout_err}")
        except requests.exceptions.RequestException as err:
            print(f"Other error occurred: {err}")
        return None
    
    # Test with valid URL
    print("Testing valid URL:")
    result = make_request(f"{BASE_URL}/repos/pandas-dev/pandas")
    print(f"Success: {result is not None}\n")
    
    # Test with invalid URL
    print("Testing invalid URL:")
    result = make_request(f"{BASE_URL}/nonexistent-endpoint")
    print(f"Success: {result is not None}")

# Run error handling demo
error_handling_demo()


# In[ ]:


def pagination_demo():
    """Demonstrate handling paginated responses"""
    print("=== Pagination Demo ===\n")
    
    all_issues = []
    page = 1
    per_page = 10  # Small number for demonstration
    
    while True:
        # Make request with pagination parameters
        params = {'page': page, 'per_page': per_page}
        url = f"{BASE_URL}/repos/pandas-dev/pandas/issues"
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error: Status code {response.status_code}")
            break
        
        page_data = response.json()
        if not page_data:
            break
            
        all_issues.extend(page_data)
        print(f"Fetched page {page}, got {len(page_data)} items")
        
        # Stop after 3 pages for demonstration
        if page >= 3:
            break
            
        page += 1
        time.sleep(1)  # Be nice to the API
    
    print(f"\nTotal issues fetched: {len(all_issues)}")
    return pd.DataFrame(all_issues)

# Run pagination demo
df_issues = pagination_demo()


# In[ ]:


def rate_limit_demo():
    """Check and display API rate limits"""
    print("=== Rate Limit Demo ===\n")
    
    response = requests.get(f"{BASE_URL}/rate_limit")
    limits = response.json()
    
    if response.status_code == 200:
        core_limits = limits['resources']['core']
        reset_time = datetime.fromtimestamp(core_limits['reset'])
        
        print("Rate Limit Information:")
        print(f"Limit: {core_limits['limit']}")
        print(f"Remaining: {core_limits['remaining']}")
        print(f"Reset Time: {reset_time}")
    else:
        print("Failed to fetch rate limits")

# Run rate limit demo
rate_limit_demo()


# In[ ]:


def analyze_issues(df):
    """Analyze the fetched issues data"""
    print("=== Data Analysis Demo ===\n")
    
    if df is not None and not df.empty:
        print("Basic Statistics:")
        print(f"Total issues: {len(df)}")
        
        # State distribution
        print("\nIssue States:")
        print(df['state'].value_counts())
        
        # Comments analysis
        print("\nComments Statistics:")
        print(df['comments'].describe())
        
        # Convert and analyze dates
        df['created_at'] = pd.to_datetime(df['created_at'])
        print("\nDate Range:")
        print(f"Earliest issue: {df['created_at'].min()}")
        print(f"Latest issue: {df['created_at'].max()}")
    else:
        print("No data available for analysis")

# Run analysis if we have data
if 'df_issues' in globals():
    analyze_issues(df_issues)


# In[ ]:


def visualize_issues(df):
    """Create visualizations of the issues data"""
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        
        # Only proceed if we have data
        if df is not None and not df.empty:
            # Time series of issues
            daily_issues = df.groupby(df['created_at'].dt.date).size().reset_index()
            daily_issues.columns = ['date', 'count']
            
            # Create line chart
            fig1 = px.line(daily_issues, x='date', y='count',
                          title='GitHub Issues Over Time')
            fig1.show()
            
            # Issue states distribution
            state_counts = df['state'].value_counts()
            fig2 = px.bar(x=state_counts.index, y=state_counts.values,
                         title='Issue States Distribution')
            fig2.show()
    except ImportError:
        print("Plotly is required for visualizations. Install with: pip install plotly")

# Run visualization if we have data
if 'df_issues' in globals():
    visualize_issues(df_issues)

