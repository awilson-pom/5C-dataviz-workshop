#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from datetime import datetime

# First, let's create a messy CSV file to work with
def create_sample_csv():
    """Create a CSV file with common issues for demonstration"""
    
    # Create some messy data
    data = {
        'ID': ['001', '002', 'N/A', '004', '005'],
        'Date': ['2024-01-15', '1/16/24', 'unknown', '2024-01-17', '18-01-2024'],
        'Temperature': ['22.5', 'NA', '25.3', '-999', '24.1'],
        'Category': ['A', 'B', 'missing', 'D', 'E'],
        'Notes': ['Good', 'Check,this', 'NA', 'Test"quote"', 'Fine'],
        'Value': ['1,234.56', '2,345.67', 'unknown', '3,456.78', '4,567.89']
    }
    
    # Write to CSV with some intentional quirks
    df = pd.DataFrame(data)
    df.to_csv('messy_data.csv', index=False)
    
    # Also create a CSV with different encoding and separator
    df.to_csv('messy_data_semicolon.csv', index=False, sep=';', encoding='latin1')

# Create our sample files
create_sample_csv()


# In[ ]:


def demonstrate_basic_loading():
    """Demonstrate basic CSV loading and common issues"""
    
    print("\n=== Basic CSV Loading ===")
    
    # Basic loading - might have issues
    print("\n1. Basic loading:")
    df = pd.read_csv('messy_data.csv')
    print(df.head())
    print("\nData Types:")
    print(df.dtypes)
    
    # Check for missing values
    print("\nMissing Values:")
    print(df.isnull().sum())
    
demonstrate_basic_loading()


# In[ ]:


def demonstrate_advanced_loading():
    """Demonstrate advanced CSV loading with custom parameters"""
    
    print("\n=== Advanced CSV Loading ===")
    
    # Advanced loading with custom parameters
    df = pd.read_csv('messy_data.csv',
                     na_values=['NA', 'N/A', 'unknown', '-999', 'missing'],  # Custom NA values
                     dtype={
                         'ID': str,  # Force ID to be string
                         'Category': 'category'  # Use category type for categorical data
                     },
                     parse_dates=['Date'])  # Parse dates automatically
    
    print("\n1. Advanced loading results:")
    print(df.head())
    print("\nData Types:")
    print(df.dtypes)
    
    # Show how missing values are handled
    print("\nMissing Values After Custom NA Handling:")
    print(df.isnull().sum())

demonstrate_advanced_loading()


# In[ ]:


def demonstrate_date_parsing():
    """Demonstrate different ways to handle date parsing"""
    
    print("\n=== Date Parsing ===")
    
    # Custom date parsing
    df = pd.read_csv('messy_data.csv',
                     parse_dates=['Date'],
                     date_parser=lambda x: pd.to_datetime(x, errors='coerce', 
                                                        format='%Y-%m-%d', 
                                                        infer_datetime_format=True))
    
    print("\nDates after parsing:")
    print(df['Date'])
    
    # Alternative: Parse dates after loading
    df['Date_Alternative'] = pd.to_datetime(df['Date'], errors='coerce')
    print("\nDates using alternative method:")
    print(df['Date_Alternative'])

demonstrate_date_parsing()


# In[ ]:


def demonstrate_numeric_handling():
    """Demonstrate handling numeric data with different formats"""
    
    print("\n=== Numeric Data Handling ===")
    
    # Handle numbers with thousands separators
    df = pd.read_csv('messy_data.csv',
                     thousands=',')  # Handle thousand separators
    
    print("\nNumeric values after handling thousands separator:")
    print(df['Value'])
    
    # Convert specific columns to numeric
    df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
    print("\nTemperature after conversion:")
    print(df['Temperature'])

demonstrate_numeric_handling()


# In[ ]:


def demonstrate_different_encodings():
    """Demonstrate handling different file encodings"""
    
    print("\n=== Handling Different Encodings ===")
    
    # Try different encodings
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            df = pd.read_csv('messy_data_semicolon.csv', 
                            encoding=encoding,
                            sep=';')
            print(f"\nSuccessfully read with {encoding} encoding")
            break
        except UnicodeDecodeError:
            print(f"Failed with {encoding} encoding")
    
demonstrate_different_encodings()


# In[ ]:


def demonstrate_chunking():
    """Demonstrate reading large CSV files in chunks"""
    
    print("\n=== Reading Large Files in Chunks ===")
    
    # Read in chunks
    chunk_size = 2
    chunks = []
    
    for chunk in pd.read_csv('messy_data.csv', chunksize=chunk_size):
        # Process each chunk (example: calculate mean of numeric columns)
        print("\nProcessing chunk:")
        print(chunk)
        chunks.append(chunk)
    
    # Combine all chunks
    df_final = pd.concat(chunks)
    print("\nFinal combined dataframe:")
    print(df_final)

demonstrate_chunking()

