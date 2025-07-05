import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import config

def create_bar_comparison(df, category_col, value_col, title, **kwargs):
    """
    Create a bar chart for category comparison.
    
    Args:
        df (pd.DataFrame): The data
        category_col (str): Column for categories (x-axis)
        value_col (str): Column for values (y-axis)
        title (str): Chart title
        **kwargs: Additional arguments for px.bar
        
    Returns:
        plotly.graph_objects.Figure: The bar chart figure
    """
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {value_col: value_col.replace('_', ' ').title(), category_col: ''},
        'color': value_col,
        'color_continuous_scale': config.CHOROPLETH_COLORSCALE,
        'text_auto': '.2s'
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.bar(
        df,
        x=category_col,
        y=value_col,
        title=title,
        **kwargs
    )
    
    # Common layout adjustments
    fig.update_layout(
        xaxis={'categoryorder': 'total descending'}
    )
    
    return fig

def create_horizontal_bar_comparison(df, category_col, value_col, title, **kwargs):
    """
    Create a horizontal bar chart for category comparison.
    
    Args:
        df (pd.DataFrame): The data
        category_col (str): Column for categories (y-axis)
        value_col (str): Column for values (x-axis)
        title (str): Chart title
        **kwargs: Additional arguments for px.bar
        
    Returns:
        plotly.graph_objects.Figure: The horizontal bar chart figure
    """
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {value_col: value_col.replace('_', ' ').title(), category_col: ''},
        'color': value_col,
        'color_continuous_scale': config.CHOROPLETH_COLORSCALE,
        'text_auto': '.2s',
        'orientation': 'h'
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.bar(
        df,
        y=category_col,
        x=value_col,
        title=title,
        **kwargs
    )
    
    # Common layout adjustments
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_grouped_bar_chart(df, category_col, value_cols, title, **kwargs):
    """
    Create a grouped bar chart with multiple value columns.
    
    Args:
        df (pd.DataFrame): The data
        category_col (str): Column for categories (x-axis)
        value_cols (list): List of columns for grouped bars
        title (str): Chart title
        **kwargs: Additional arguments for px.bar
        
    Returns:
        plotly.graph_objects.Figure: The grouped bar chart figure
    """
    # Melt the dataframe for grouped bars
    melted_df = pd.melt(
        df, 
        id_vars=[category_col], 
        value_vars=value_cols,
        var_name='Metric', 
        value_name='Value'
    )
    
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {'Value': 'Value', 'Metric': 'Metric'},
        'barmode': 'group',
        'text_auto': '.2s'
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.bar(
        melted_df,
        x=category_col,
        y='Value',
        color='Metric',
        title=title,
        **kwargs
    )
    
    return fig

def create_scatter_comparison(df, x_col, y_col, title, hover_name=None, size_col=None, color_col=None, **kwargs):
    """
    Create a scatter plot for comparing two metrics.
    
    Args:
        df (pd.DataFrame): The data
        x_col (str): Column for x-axis
        y_col (str): Column for y-axis
        title (str): Chart title
        hover_name (str, optional): Column for hover text
        size_col (str, optional): Column for point size
        color_col (str, optional): Column for point color
        **kwargs: Additional arguments for px.scatter
        
    Returns:
        plotly.graph_objects.Figure: The scatter plot figure
    """
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {
            x_col: x_col.replace('_', ' ').title(), 
            y_col: y_col.replace('_', ' ').title()
        },
        'opacity': 0.7
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        hover_name=hover_name,
        size=size_col,
        color=color_col,
        title=title,
        **kwargs
    )
    
    return fig

def create_bubble_chart(df, x_col, y_col, size_col, title, hover_name=None, color_col=None, **kwargs):
    """
    Create a bubble chart.
    
    Args:
        df (pd.DataFrame): The data
        x_col (str): Column for x-axis
        y_col (str): Column for y-axis
        size_col (str): Column for bubble size
        title (str): Chart title
        hover_name (str, optional): Column for hover text
        color_col (str, optional): Column for bubble color
        **kwargs: Additional arguments for px.scatter
        
    Returns:
        plotly.graph_objects.Figure: The bubble chart figure
    """
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {
            x_col: x_col.replace('_', ' ').title(), 
            y_col: y_col.replace('_', ' ').title(),
            size_col: size_col.replace('_', ' ').title()
        },
        'opacity': 0.7,
        'size_max': 60
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        size=size_col,
        hover_name=hover_name,
        color=color_col,
        title=title,
        **kwargs
    )
    
    return fig

def create_multi_metric_radar_chart(df, category_col, value_cols, title):
    """
    Create a radar chart for comparing multiple metrics across categories.
    
    Args:
        df (pd.DataFrame): The data
        category_col (str): Column containing categories
        value_cols (list): List of columns for radar chart axes
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: The radar chart figure
    """
    # Prepare data
    categories = df[category_col].tolist()
    
    # Create figure
    fig = go.Figure()
    
    # Add each metric as a trace
    for col in value_cols:
        fig.add_trace(go.Scatterpolar(
            r=df[col].tolist(),
            theta=categories,
            fill='toself',
            name=col.replace('_', ' ').title()
        ))
    
    # Update layout
    fig.update_layout(
        title=title,
        height=config.DEFAULT_CHART_HEIGHT,
        template='plotly_white',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max([df[col].max() for col in value_cols]) * 1.1]
            )
        )
    )
    
    return fig