"""
Custom metrics calculations for the CO2 emissions dashboard.
"""

import pandas as pd
import numpy as np
import streamlit as st

def calculate_percent_change(df, column, year1, year2):
    """
    Calculate the percent change in a metric between two years.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data
        column (str): Column to calculate change for
        year1 (int): Starting year
        year2 (int): Ending year
        
    Returns:
        float: Percent change
    """
    # Filter data for the specified years
    value1 = df[df['Year'] == year1][column].sum()
    value2 = df[df['Year'] == year2][column].sum()
    
    # Calculate percent change
    if value1 == 0:
        return np.inf if value2 > 0 else -np.inf if value2 < 0 else 0
    
    return ((value2 - value1) / value1) * 100

@st.cache_data
def calculate_cagr(df, column, start_year, end_year):
    """
    Calculate Compound Annual Growth Rate (CAGR) for a metric.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data
        column (str): Column to calculate CAGR for
        start_year (int): Starting year
        end_year (int): Ending year
        
    Returns:
        float: CAGR as a percentage
    """
    # Filter data for the specified years
    start_value = df[df['Year'] == start_year][column].sum()
    end_value = df[df['Year'] == end_year][column].sum()
    
    # Calculate number of years
    n_years = end_year - start_year
    
    # Handle edge cases
    if start_value <= 0 or n_years <= 0:
        return 0
    
    # Calculate CAGR
    cagr = (((end_value / start_value) ** (1 / n_years)) - 1) * 100
    
    return cagr

@st.cache_data
def calculate_moving_average(df, column, window=5):
    """
    Calculate moving average for a time series.
    
    Args:
        df (pd.DataFrame): DataFrame containing time series data
        column (str): Column to calculate moving average for
        window (int): Window size for moving average
        
    Returns:
        pd.Series: Moving average series
    """
    # Ensure data is sorted by year
    df = df.sort_values('Year')
    
    # Calculate moving average
    return df[column].rolling(window=window, min_periods=1).mean()

@st.cache_data
def calculate_emission_intensity(df, source_col, total_col):
    """
    Calculate emission intensity (source as percent of total).
    
    Args:
        df (pd.DataFrame): DataFrame containing the data
        source_col (str): Column with source emissions
        total_col (str): Column with total emissions
        
    Returns:
        pd.Series: Emission intensity as percentage
    """
    # Calculate intensity
    intensity = (df[source_col] / df[total_col]) * 100
    
    # Replace infinities and NaN with 0
    intensity = intensity.replace([np.inf, -np.inf, np.nan], 0)
    
    return intensity

@st.cache_data
def calculate_top_contributors(df, column, year, n=10, min_value=None):
    """
    Calculate top contributing countries/entities for a specific metric.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data
        column (str): Column to rank by
        year (int): Year to filter for
        n (int): Number of top contributors to return
        min_value (float, optional): Minimum value threshold
        
    Returns:
        pd.DataFrame: DataFrame with top contributors
    """
    # Filter data for the specified year
    year_df = df[df['Year'] == year].copy()
    
    # Apply minimum value filter if specified
    if min_value is not None:
        year_df = year_df[year_df[column] >= min_value]
    
    # Sort and get top n
    top_n = year_df.sort_values(column, ascending=False).head(n)
    
    # Calculate percentage of total
    total = year_df[column].sum()
    if total > 0:
        top_n['Percentage'] = (top_n[column] / total) * 100
    else:
        top_n['Percentage'] = 0
    
    return top_n

@st.cache_data
def calculate_reduction_needed(df, column, current_year, target_year, target_reduction_pct):
    """
    Calculate emissions reduction needed to meet a target.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data
        column (str): Column with emissions data
        current_year (int): Current year
        target_year (int): Target year
        target_reduction_pct (float): Target percentage reduction
        
    Returns:
        dict: Dictionary with reduction metrics
    """
    # Get current emissions
    current_emissions = df[df['Year'] == current_year][column].sum()
    
    # Calculate target emissions
    target_emissions = current_emissions * (1 - (target_reduction_pct / 100))
    
    # Calculate absolute reduction needed
    absolute_reduction = current_emissions - target_emissions
    
    # Calculate annual reduction needed
    years_remaining = target_year - current_year
    if years_remaining <= 0:
        annual_reduction = absolute_reduction
        annual_reduction_pct = target_reduction_pct
    else:
        annual_reduction = absolute_reduction / years_remaining
        annual_reduction_pct = (1 - ((1 - (target_reduction_pct / 100)) ** (1 / years_remaining))) * 100
    
    return {
        'current_emissions': current_emissions,
        'target_emissions': target_emissions,
        'absolute_reduction': absolute_reduction,
        'annual_reduction': annual_reduction,
        'annual_reduction_pct': annual_reduction_pct
    }