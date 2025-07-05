import streamlit as st
import pandas as pd
import config

def add_year_range_selector(df, default_start=config.DEFAULT_START_YEAR, default_end=config.DEFAULT_END_YEAR):
    """
    Add a year range selector to the sidebar.
    
    Args:
        df (pd.DataFrame): The dataframe containing the 'Year' column
        default_start (int): Default start year
        default_end (int): Default end year
        
    Returns:
        tuple: Selected start and end years
    """
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    
    # Ensure defaults are within valid range
    default_start = max(min_year, default_start)
    default_end = min(max_year, default_end)
    
    start_year = st.sidebar.slider(
        "Start Year",
        min_value=min_year,
        max_value=max_year,
        value=default_start,
        step=1
    )
    
    # Ensure end_year is at least start_year
    end_year = st.sidebar.slider(
        "End Year",
        min_value=start_year,
        max_value=max_year,
        value=min(default_end, max_year),
        step=1
    )
    
    return start_year, end_year

def add_year_selector(df, default=None, label="Select Year"):
    """
    Add a single year selector to the sidebar.
    
    Args:
        df (pd.DataFrame): The dataframe containing the 'Year' column
        default (int, optional): Default selected year
        label (str): Label for the selector
        
    Returns:
        int: Selected year
    """
    years = sorted(df['Year'].unique())
    
    if default is None:
        default = years[-1]  # Latest year
    elif default not in years:
        default = min(filter(lambda y: y >= default, years), default=years[-1])
    
    selected_year = st.sidebar.selectbox(
        label,
        options=years,
        index=years.index(default) if default in years else len(years) - 1
    )
    
    return selected_year

def add_country_selector(df, default="China"):
    """
    Add a country selector to the sidebar.
    
    Args:
        df (pd.DataFrame): The dataframe containing the 'Country' column
        default (str): Default selected country
        
    Returns:
        str: Selected country
    """
    countries = sorted(df['Country'].unique())
    
    if default not in countries:
        default = countries[0]
    
    selected_country = st.sidebar.selectbox(
        "Select Country",
        options=countries,
        index=countries.index(default) if default in countries else 0
    )
    
    return selected_country

def add_top_n_selector(default=10, max_value=50):
    """
    Add a selector for the number of top items to display.
    
    Args:
        default (int): Default number of items
        max_value (int): Maximum number of items
        
    Returns:
        int: Selected number of items
    """
    top_n = st.sidebar.slider(
        "Number of items to display",
        min_value=5,
        max_value=max_value,
        value=default,
        step=5
    )
    
    return top_n