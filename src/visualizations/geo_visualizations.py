import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import numpy as np
import config

def create_choropleth_map(df, iso_col, color_col, title, **kwargs):
    """
    Create a choropleth map of countries.
    
    Args:
        df (pd.DataFrame): The data
        iso_col (str): Column containing ISO country codes
        color_col (str): Column for color encoding
        title (str): Map title
        **kwargs: Additional arguments for px.choropleth
        
    Returns:
        plotly.graph_objects.Figure: The choropleth map figure
    """
    default_kwargs = {
        'height': config.DEFAULT_MAP_HEIGHT,
        'color_continuous_scale': config.CHOROPLETH_COLORSCALE,
        'labels': {color_col: color_col.replace('_', ' ').title()},
        'template': 'plotly_white',
        'projection': 'natural earth'
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.choropleth(
        df,
        locations=iso_col,
        color=color_col,
        title=title,
        **kwargs
    )
    
    # Common layout adjustments
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="aliceblue",
            showlakes=True,
            lakecolor="aliceblue",
            showrivers=True,
            rivercolor="aliceblue"
        )
    )
    
    return fig

def create_bubble_map(df, lat_col, lon_col, size_col, hover_name_col, title, color_col=None, **kwargs):
    """
    Create a bubble map with points sized by a metric.
    
    Args:
        df (pd.DataFrame): The data
        lat_col (str): Column containing latitude
        lon_col (str): Column containing longitude
        size_col (str): Column for bubble size
        hover_name_col (str): Column for hover text
        title (str): Map title
        color_col (str, optional): Column for color encoding
        **kwargs: Additional arguments for px.scatter_geo
        
    Returns:
        plotly.graph_objects.Figure: The bubble map figure
    """
    default_kwargs = {
        'height': config.DEFAULT_MAP_HEIGHT,
        'template': 'plotly_white',
        'labels': {size_col: size_col.replace('_', ' ').title()},
        'projection': 'natural earth'
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    if color_col:
        fig = px.scatter_geo(
            df,
            lat=lat_col,
            lon=lon_col,
            size=size_col,
            hover_name=hover_name_col,
            color=color_col,
            title=title,
            **kwargs
        )
    else:
        fig = px.scatter_geo(
            df,
            lat=lat_col,
            lon=lon_col,
            size=size_col,
            hover_name=hover_name_col,
            title=title,
            **kwargs
        )
    
    # Common layout adjustments
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="aliceblue",
            showlakes=True,
            lakecolor="aliceblue",
            showrivers=True,
            rivercolor="aliceblue"
        )
    )
    
    return fig

def create_regional_choropleth(df, region_col, color_col, title, **kwargs):
    """
    Create a choropleth map of regions rather than countries.
    
    Args:
        df (pd.DataFrame): The data
        region_col (str): Column containing region names
        color_col (str): Column for color encoding
        title (str): Map title
        **kwargs: Additional arguments for px.choropleth
        
    Returns:
        plotly.graph_objects.Figure: The regional choropleth map figure
    """
    default_kwargs = {
        'height': config.DEFAULT_MAP_HEIGHT,
        'color_continuous_scale': config.CHOROPLETH_COLORSCALE,
        'labels': {color_col: color_col.replace('_', ' ').title()},
        'template': 'plotly_white',
        'projection': 'natural earth',
        'scope': 'world'  # can be 'world', 'usa', 'europe', 'asia', 'africa', etc.
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    # Create a dummy variable for regions if not present in geojson
    # (This is a placeholder - actual implementation would depend on having region GeoJSON)
    fig = px.choropleth(
        df,
        locations=region_col,
        locationmode="country names",  # Change as needed based on your region definitions
        color=color_col,
        title=title,
        **kwargs
    )
    
    # Common layout adjustments
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="aliceblue",
            showlakes=True,
            lakecolor="aliceblue",
            showrivers=True,
            rivercolor="aliceblue"
        )
    )
    
    return fig

def animate_choropleth_by_year(df, iso_col, color_col, year_col, title, **kwargs):
    """
    Create an animated choropleth map changing over years.
    
    Args:
        df (pd.DataFrame): The data
        iso_col (str): Column containing ISO country codes
        color_col (str): Column for color encoding
        year_col (str): Column containing years for animation
        title (str): Map title
        **kwargs: Additional arguments for px.choropleth
        
    Returns:
        plotly.graph_objects.Figure: The animated choropleth map figure
    """
    default_kwargs = {
        'height': config.DEFAULT_MAP_HEIGHT,
        'color_continuous_scale': config.CHOROPLETH_COLORSCALE,
        'labels': {color_col: color_col.replace('_', ' ').title()},
        'template': 'plotly_white',
        'projection': 'natural earth',
        'animation_frame': year_col,
        'range_color': [df[color_col].min(), df[color_col].max()]
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.choropleth(
        df,
        locations=iso_col,
        color=color_col,
        title=title,
        **kwargs
    )
    
    # Common layout adjustments
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="aliceblue",
            showlakes=True,
            lakecolor="aliceblue",
            showrivers=True,
            rivercolor="aliceblue"
        )
    )
    
    # Animation settings
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 800
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300
    
    return fig