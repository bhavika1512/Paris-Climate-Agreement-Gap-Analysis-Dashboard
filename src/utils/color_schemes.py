"""
Color scheme definitions for the CO2 emissions dashboard visualizations.
"""

import plotly.express as px
import config

# Source colors - defined in config.py
EMISSION_SOURCES_COLORS = config.EMISSION_SOURCES_COLORS

# Categorical color scales
def get_categorical_colors(n_colors=10):
    """
    Get a categorical color palette with the specified number of colors.
    
    Args:
        n_colors (int): Number of colors needed
        
    Returns:
        list: List of color hex codes
    """
    # Use px.colors.qualitative for categorical data
    if n_colors <= 10:
        return px.colors.qualitative.Plotly[:n_colors]
    elif n_colors <= 12:
        return px.colors.qualitative.Set3[:n_colors]
    else:
        # For more colors, cycle through existing palette
        base_colors = px.colors.qualitative.Plotly
        return [base_colors[i % len(base_colors)] for i in range(n_colors)]

# Sequential color scales for continuous data
def get_sequential_colorscale(colorscale_name=None):
    """
    Get a sequential color scale.
    
    Args:
        colorscale_name (str, optional): Name of the colorscale from Plotly
        
    Returns:
        list or str: Color scale for use in visualizations
    """
    # If no name specified, use the default from config
    if colorscale_name is None:
        return config.CHOROPLETH_COLORSCALE
    
    # Return named colorscale if it exists
    if hasattr(px.colors.sequential, colorscale_name):
        return getattr(px.colors.sequential, colorscale_name)
    else:
        return config.CHOROPLETH_COLORSCALE

# Diverging color scales for data centered around a midpoint
def get_diverging_colorscale(colorscale_name=None):
    """
    Get a diverging color scale for values that diverge from a midpoint.
    
    Args:
        colorscale_name (str, optional): Name of the colorscale from Plotly
        
    Returns:
        list or str: Color scale for use in visualizations
    """
    # Default to RdBu_r (red to blue, reversed) if none specified
    if colorscale_name is None:
        return "RdBu_r"
    
    # Return named colorscale if it exists
    if hasattr(px.colors.diverging, colorscale_name):
        return getattr(px.colors.diverging, colorscale_name)
    else:
        return "RdBu_r"

# Color scale for percent changes (green for positive, red for negative)
def get_change_colorscale():
    """
    Get a colorscale for percent changes (green for positive, red for negative).
    
    Returns:
        list: Custom colorscale
    """
    return [
        [0, "rgb(165, 0, 38)"],      # Strong negative
        [0.25, "rgb(215, 48, 39)"],  # Negative
        [0.45, "rgb(244, 109, 67)"], # Slight negative
        [0.5, "rgb(255, 255, 255)"], # Neutral
        [0.55, "rgb(116, 173, 209)"],# Slight positive
        [0.75, "rgb(69, 117, 180)"], # Positive
        [1, "rgb(49, 54, 149)"]      # Strong positive
    ]

# Functions to get specific color palettes
def get_region_colors():
    """
    Get a color palette for regions.
    
    Returns:
        dict: Mapping of regions to colors
    """
    regions = list(config.REGIONS.keys())
    colors = get_categorical_colors(len(regions))
    
    return dict(zip(regions, colors))

def color_by_value(value, min_val, max_val, colorscale_name=None):
    """
    Get a color from a sequential colorscale based on value.
    
    Args:
        value (float): The value to map to a color
        min_val (float): Minimum value in the range
        max_val (float): Maximum value in the range
        colorscale_name (str, optional): Name of the colorscale
        
    Returns:
        str: Hex color code
    """
    import plotly.colors as pc
    
    # Get colorscale
    colorscale = get_sequential_colorscale(colorscale_name)
    
    # Normalize value to 0-1 range
    if max_val == min_val:
        normalized = 0.5  # Handle case where all values are the same
    else:
        normalized = (value - min_val) / (max_val - min_val)
    
    # Clamp to 0-1 range
    normalized = max(0, min(1, normalized))
    
    # Map to color
    return pc.sample_colorscale(colorscale, normalized)[0]