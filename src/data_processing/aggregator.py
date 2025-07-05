import pandas as pd
import numpy as np
import streamlit as st
import config
from src.data_processing.loader import get_country_codes

@st.cache_data
def aggregate_by_year(df, column='Total'):
    """
    Aggregate emissions data by year.
    
    Args:
        df (pd.DataFrame): Emissions dataframe
        column (str): Column to aggregate (default: 'Total')
        
    Returns:
        pd.DataFrame: Aggregated dataframe with columns ['Year', column]
    """
    if df.empty or column not in df.columns:
        return pd.DataFrame()
    
    # Group by year and sum the specified column
    aggregated = df.groupby('Year')[column].sum().reset_index()
    return aggregated

@st.cache_data
def aggregate_by_region(df, column='Total', year=None):
    """
    Aggregate emissions data by region for a specific year.
    
    Args:
        df (pd.DataFrame): Emissions dataframe
        column (str): Column to aggregate (default: 'Total')
        year (int, optional): Specific year to filter for
        
    Returns:
        pd.DataFrame: Aggregated dataframe with columns ['Region', column]
    """
    if df.empty or column not in df.columns:
        return pd.DataFrame()
    
    # Filter by year if specified
    if year is not None:
        df = df[df['Year'] == year]
    
    # Create a region mapping
    region_map = {}
    for region, countries in config.REGIONS.items():
        for country_code in countries:
            region_map[country_code] = region
    
    # Add a Region column
    df_with_region = df.copy()
    df_with_region['Region'] = df_with_region['ISO 3166-1 alpha-3'].map(region_map)
    
    # Remove rows without a region
    df_with_region = df_with_region.dropna(subset=['Region'])
    
    # Group by region and sum the specified column
    aggregated = df_with_region.groupby('Region')[column].sum().reset_index()
    return aggregated

@st.cache_data
def aggregate_by_source(df, year=None, country=None):
    """
    Aggregate emissions data by source.
    
    Args:
        df (pd.DataFrame): Emissions dataframe
        year (int, optional): Specific year to filter for
        country (str, optional): Specific country to filter for
        
    Returns:
        pd.DataFrame: Aggregated dataframe with emissions by source
    """
    if df.empty:
        return pd.DataFrame()
    
    # Source columns
    source_columns = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other"]
    
    # Check if source columns exist
    source_columns = [col for col in source_columns if col in df.columns]
    if not source_columns:
        return pd.DataFrame()
    
    # Filter dataframe
    filtered_df = df.copy()
    if year is not None:
        filtered_df = filtered_df[filtered_df['Year'] == year]
    if country is not None:
        filtered_df = filtered_df[filtered_df['Country'] == country]
    
    # Aggregate by source
    if country is not None:
        # For a specific country, just return the row(s)
        result = filtered_df[['Year'] + source_columns]
    else:
        # Sum by source
        result = pd.DataFrame({
            'Source': source_columns,
            'Emissions': [filtered_df[col].sum() for col in source_columns]
        })
    
    return result

@st.cache_data
def calculate_per_source_percentages(df, year=None):
    """
    Calculate the percentage contribution of each emission source.
    
    Args:
        df (pd.DataFrame): Emissions dataframe
        year (int, optional): Specific year to filter for
        
    Returns:
        pd.DataFrame: Dataframe with source percentages by year
    """
    if df.empty:
        return pd.DataFrame()
    
    # Source columns
    source_columns = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other"]
    
    # Check if source columns exist
    source_columns = [col for col in source_columns if col in df.columns]
    if not source_columns:
        return pd.DataFrame()
    
    # Filter by year if specified
    if year is not None:
        df = df[df['Year'] == year]
    
    # Group by year and sum source columns
    sources_by_year = df.groupby('Year')[source_columns].sum().reset_index()
    
    # Calculate percentages
    for source in source_columns:
        sources_by_year[f"{source}_pct"] = (sources_by_year[source] / sources_by_year[source_columns].sum(axis=1)) * 100
    
    return sources_by_year

@st.cache_data
def get_top_emitters(df, column='Total', year=None, n=10):
    """
    Get the top n emitters for a specific year.
    
    Args:
        df (pd.DataFrame): Emissions dataframe
        column (str): Column to sort by (default: 'Total')
        year (int, optional): Specific year to filter for
        n (int): Number of top emitters to return
        
    Returns:
        pd.DataFrame: Top n emitters sorted by the specified column
    """
    if df.empty or column not in df.columns:
        return pd.DataFrame()
    
    # Filter by year if specified
    if year is not None:
        df = df[df['Year'] == year]
    
    # Sort and get top n
    top_n = df.sort_values(column, ascending=False).head(n)
    return top_n

@st.cache_data
def calculate_growth_rates(df, column='Total', periods=[5, 10, 20]):
    """
    Calculate growth rates over different periods.
    
    Args:
        df (pd.DataFrame): Emissions dataframe
        column (str): Column to calculate growth for (default: 'Total')
        periods (list): List of periods (years) to calculate growth rates for
        
    Returns:
        pd.DataFrame: Dataframe with growth rates for different periods
    """
    if df.empty or column not in df.columns:
        return pd.DataFrame()
    
    # Get the latest year in the data
    latest_year = df['Year'].max()
    
    # Initialize result dataframe
    result = pd.DataFrame({'Country': df['Country'].unique()})
    
    # Calculate growth rates for each period
    for period in periods:
        # Get data for current and past year
        current_year_data = df[df['Year'] == latest_year][['Country', column]].set_index('Country')
        past_year_data = df[df['Year'] == (latest_year - period)][['Country', column]].set_index('Country')
        
        # Calculate growth rate
        growth = pd.DataFrame({
            'Country': current_year_data.index,
            f'{period}yr_growth': ((current_year_data[column] / past_year_data[column]) - 1) * 100
        }).set_index('Country')
        
        # Merge with result
        result = result.set_index('Country').join(growth, how='left').reset_index()
    
    return result