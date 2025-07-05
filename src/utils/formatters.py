"""
Formatting utilities for the CO2 emissions dashboard.
"""

import pandas as pd
import numpy as np
import streamlit as st

def format_number(value, precision=1, suffix=''):
    """
    Format a number with thousands separator and fixed precision.
    
    Args:
        value (float): Number to format
        precision (int): Decimal precision
        suffix (str): Optional suffix to append
        
    Returns:
        str: Formatted number string
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    # Format with thousands separator and fixed precision
    formatted = f"{value:,.{precision}f}"
    
    # Add suffix if provided
    if suffix:
        formatted += f" {suffix}"
    
    return formatted

def format_with_units(value, unit='Mt CO2'):
    """
    Format a number with appropriate units.
    
    Args:
        value (float): Number to format
        unit (str): Base unit
        
    Returns:
        str: Formatted number with units
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    # Format based on magnitude
    if abs(value) >= 1e9:
        return f"{value/1e9:.1f} G{unit}"
    elif abs(value) >= 1e6:
        return f"{value/1e6:.1f} M{unit}"
    elif abs(value) >= 1e3:
        return f"{value/1e3:.1f} k{unit}"
    else:
        return f"{value:.1f} {unit}"

def format_percent(value, precision=1, include_sign=False):
    """
    Format a value as a percentage.
    
    Args:
        value (float): Value to format as percentage
        precision (int): Decimal precision
        include_sign (bool): Whether to include + sign for positive values
        
    Returns:
        str: Formatted percentage string
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    # Format with precision
    if include_sign and value > 0:
        return f"+{value:.{precision}f}%"
    else:
        return f"{value:.{precision}f}%"

def format_year_range(start_year, end_year):
    """
    Format a year range.
    
    Args:
        start_year (int): Start year
        end_year (int): End year
        
    Returns:
        str: Formatted year range
    """
    return f"{start_year}–{end_year}"

def format_country_name(country_code):
    """
    Format a country code to a readable name.
    
    Args:
        country_code (str): ISO 3166-1 alpha-3 country code
        
    Returns:
        str: Formatted country name
    """
    # This is a minimal mapping of common codes to full names
    # In a real application, you would use a more complete mapping
    country_mapping = {
        'USA': 'United States',
        'CHN': 'China',
        'IND': 'India',
        'RUS': 'Russia',
        'JPN': 'Japan',
        'DEU': 'Germany',
        'GBR': 'United Kingdom',
        'FRA': 'France',
        'ITA': 'Italy',
        'CAN': 'Canada',
        'BRA': 'Brazil',
        'AUS': 'Australia'
    }
    
    return country_mapping.get(country_code, country_code)

def format_metric_for_display(metric, value, show_units=True):
    """
    Format a metric value appropriately based on its type.
    
    Args:
        metric (str): Metric name
        value (float): Value to format
        show_units (bool): Whether to include units
        
    Returns:
        str: Formatted value
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    # Format based on metric type
    if 'percent' in metric.lower() or metric.endswith('_pct'):
        return format_percent(value)
    elif any(term in metric.lower() for term in ['total', 'emissions', 'coal', 'oil', 'gas', 'cement']):
        return format_with_units(value, unit='Mt CO2' if show_units else '')
    elif 'per_capita' in metric.lower():
        return format_with_units(value, unit='t CO2/capita' if show_units else '')
    else:
        return format_number(value)

def create_delta_indicator(current, previous, is_good_if_down=True):
    """
    Create a delta indicator for metrics display.
    
    Args:
        current (float): Current value
        previous (float): Previous value
        is_good_if_down (bool): Whether a decrease is considered positive
        
    Returns:
        tuple: (delta_value, is_positive)
    """
    if pd.isna(current) or pd.isna(previous) or previous == 0:
        return None, None
    
    delta = ((current - previous) / previous) * 100
    
    # Determine if the change is positive based on direction and context
    if delta < 0:
        is_positive = is_good_if_down
    elif delta > 0:
        is_positive = not is_good_if_down
    else:
        is_positive = None
    
    return delta, is_positive

def abbreviate_large_number(num):
    """
    Abbreviate large numbers for display.
    
    Args:
        num (float): Number to abbreviate
        
    Returns:
        str: Abbreviated number
    """
    if pd.isna(num) or num is None:
        return "N/A"
    
    magnitude = 0
    abbreviations = ['', 'K', 'M', 'B', 'T']
    while abs(num) >= 1000 and magnitude < len(abbreviations) - 1:
        magnitude += 1
        num /= 1000.0
    
    # Format with 1 decimal place for numbers with magnitude
    if magnitude > 0:
        return f"{num:.1f}{abbreviations[magnitude]}"
    else:
        return f"{num:.0f}"