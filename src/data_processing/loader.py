import pandas as pd
import streamlit as st
import os
import json
import config

@st.cache
def load_emissions_data():
    """
    Load and prepare the total emissions data.
    
    Returns:
        pd.DataFrame: Prepared emissions dataframe
    """
    try:
        # Check if file exists
        if not os.path.exists(config.TOTAL_EMISSIONS_FILE):
            st.error(f"Error: Data file not found at {config.TOTAL_EMISSIONS_FILE}")
            return pd.DataFrame()
        
        # Load data
        df = pd.read_csv(config.TOTAL_EMISSIONS_FILE)
        
        # Basic validation
        required_columns = ['Country', 'ISO 3166-1 alpha-3', 'Year', 'Total']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Error: Required column '{col}' not found in data")
                return pd.DataFrame()
        
        # Convert Year to integer
        df['Year'] = df['Year'].astype(int)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading emissions data: {str(e)}")
        return pd.DataFrame()

@st.cache
def load_per_capita_data():
    """
    Load and prepare the per capita emissions data.
    
    Returns:
        pd.DataFrame: Prepared per capita emissions dataframe
    """
    try:
        # Check if file exists
        if not os.path.exists(config.PER_CAPITA_EMISSIONS_FILE):
            st.error(f"Error: Data file not found at {config.PER_CAPITA_EMISSIONS_FILE}")
            return pd.DataFrame()
        
        # Load data
        df = pd.read_csv(config.PER_CAPITA_EMISSIONS_FILE)
        
        # Basic validation
        required_columns = ['Country', 'ISO 3166-1 alpha-3', 'Year', 'Total']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Error: Required column '{col}' not found in data")
                return pd.DataFrame()
        
        # Convert Year to integer
        df['Year'] = df['Year'].astype(int)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading per capita data: {str(e)}")
        return pd.DataFrame()

@st.cache
def load_sources_data():
    """
    Load and prepare the emission sources data.
    
    Returns:
        pd.DataFrame: Prepared emission sources dataframe
    """
    try:
        # Check if file exists
        if not os.path.exists(config.SOURCES_FILE):
            st.error(f"Error: Data file not found at {config.SOURCES_FILE}")
            return pd.DataFrame()
        
        # Load data
        df = pd.read_csv(config.SOURCES_FILE)
        
        # Basic validation
        required_columns = ['Country', 'ISO 3166-1 alpha-3', 'Year']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Error: Required column '{col}' not found in data")
                return pd.DataFrame()
        
        # Convert Year to integer
        df['Year'] = df['Year'].astype(int)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading sources data: {str(e)}")
        return pd.DataFrame()

@st.cache
def load_metadata(metadata_file):
    """
    Load metadata from a JSON file.
    
    Args:
        metadata_file (str): Path to the metadata JSON file
        
    Returns:
        dict: Metadata dictionary or empty dict if file not found
    """
    try:
        # Check if file exists
        if not os.path.exists(metadata_file):
            st.warning(f"Metadata file not found at {metadata_file}")
            return {}
        
        # Load JSON metadata
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        return metadata
    
    except Exception as e:
        st.warning(f"Error loading metadata: {str(e)}")
        return {}

def get_country_codes():
    """
    Get a mapping of country names to ISO codes.
    
    Returns:
        dict: Mapping of country names to ISO codes
    """
    df = load_emissions_data()
    if df.empty:
        return {}
    
    # Create a dictionary mapping country names to ISO codes
    country_codes = dict(zip(df['Country'], df['ISO 3166-1 alpha-3']))
    return country_codes

def get_countries_by_region():
    """
    Get a mapping of countries by region based on the predefined regions in config.
    
    Returns:
        dict: Mapping of regions to lists of country names
    """
    country_codes = get_country_codes()
    if not country_codes:
        return {}
    
    # Invert the country codes dictionary
    code_to_country = {code: country for country, code in country_codes.items()}
    
    # Map regions to country names
    countries_by_region = {}
    for region, codes in config.REGIONS.items():
        countries_by_region[region] = [code_to_country.get(code, code) for code in codes if code in code_to_country]
    
    return countries_by_region