import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import config

def create_line_chart(df, x_col, y_col, title, color_col=None, **kwargs):
    """
    Create a line chart.
    
    Args:
        df (pd.DataFrame): The data
        x_col (str): Column for x-axis
        y_col (str): Column for y-axis
        title (str): Chart title
        color_col (str, optional): Column for color encoding
        **kwargs: Additional arguments for px.line
        
    Returns:
        plotly.graph_objects.Figure: The line chart figure
    """
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {y_col: y_col.replace('_', ' ').title(), x_col: x_col.replace('_', ' ').title()},
        'hover_data': None
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    if color_col:
        fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title, **kwargs)
    else:
        fig = px.line(df, x=x_col, y=y_col, title=title, **kwargs)
    
    # Common layout adjustments
    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(tickmode='linear', dtick=5) if x_col == 'Year' else None
    )
    
    return fig

def create_multi_line_chart(df, x_col, y_cols, title, **kwargs):
    """
    Create a multi-line chart with multiple y columns.
    
    Args:
        df (pd.DataFrame): The data
        x_col (str): Column for x-axis
        y_cols (list): List of columns for multiple lines
        title (str): Chart title
        **kwargs: Additional arguments for px.line
        
    Returns:
        plotly.graph_objects.Figure: The multi-line chart figure
    """
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {col: col.replace('_', ' ').title() for col in y_cols},
        'hover_data': None
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    # Create figure
    fig = go.Figure()
    
    # Add each line
    for col in y_cols:
        fig.add_trace(
            go.Scatter(
                x=df[x_col], 
                y=df[col], 
                name=col,
                mode='lines'
            )
        )
    
    # Update layout
    fig.update_layout(
        title=title,
        height=kwargs['height'],
        template=kwargs['template'],
        hovermode="x unified",
        xaxis=dict(tickmode='linear', dtick=5) if x_col == 'Year' else None,
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_cols[0].replace('_', ' ').title()  # Use first y column for axis title
    )
    
    return fig

def create_area_chart(df, x_col, y_col, title, color_col=None, **kwargs):
    """
    Create an area chart.
    
    Args:
        df (pd.DataFrame): The data
        x_col (str): Column for x-axis
        y_col (str): Column for y-axis
        title (str): Chart title
        color_col (str, optional): Column for color encoding
        **kwargs: Additional arguments for px.area
        
    Returns:
        plotly.graph_objects.Figure: The area chart figure
    """
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {y_col: y_col.replace('_', ' ').title(), x_col: x_col.replace('_', ' ').title()},
        'hover_data': None
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    if color_col:
        fig = px.area(df, x=x_col, y=y_col, color=color_col, title=title, **kwargs)
    else:
        fig = px.area(df, x=x_col, y=y_col, title=title, **kwargs)
    
    # Common layout adjustments
    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(tickmode='linear', dtick=5) if x_col == 'Year' else None
    )
    
    return fig

def create_stacked_area_chart(df, x_col, y_cols, title, **kwargs):
    """
    Create a stacked area chart with multiple y columns.
    
    Args:
        df (pd.DataFrame): The data
        x_col (str): Column for x-axis
        y_cols (list): List of columns to stack
        title (str): Chart title
        **kwargs: Additional arguments for px.area
        
    Returns:
        plotly.graph_objects.Figure: The stacked area chart figure
    """
    # Melt the dataframe for stacked area
    melted_df = pd.melt(
        df, 
        id_vars=[x_col], 
        value_vars=y_cols,
        var_name='Category', 
        value_name='Value'
    )
    
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {'Value': 'Value', 'Category': 'Category'},
        'color_discrete_map': config.EMISSION_SOURCES_COLORS if set(y_cols).issubset(config.EMISSION_SOURCES_COLORS.keys()) else None
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    fig = px.area(
        melted_df, 
        x=x_col, 
        y='Value', 
        color='Category', 
        title=title,
        **kwargs
    )
    
    # Common layout adjustments
    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(tickmode='linear', dtick=5) if x_col == 'Year' else None
    )
    
    return fig

def create_bar_chart_with_average_line(df, x_col, y_col, title, avg_label="Average", **kwargs):
    """
    Create a bar chart with an average line.
    
    Args:
        df (pd.DataFrame): The data
        x_col (str): Column for x-axis
        y_col (str): Column for y-axis
        title (str): Chart title
        avg_label (str): Label for the average line
        **kwargs: Additional arguments for px.bar
        
    Returns:
        plotly.graph_objects.Figure: The bar chart figure with average line
    """
    default_kwargs = {
        'height': config.DEFAULT_CHART_HEIGHT,
        'template': 'plotly_white',
        'labels': {y_col: y_col.replace('_', ' ').title(), x_col: x_col.replace('_', ' ').title()},
        'hover_data': None
    }
    
    # Update defaults with provided kwargs
    kwargs = {**default_kwargs, **kwargs}
    
    # Calculate average
    avg = df[y_col].mean()
    
    # Create bar chart
    fig = px.bar(df, x=x_col, y=y_col, title=title, **kwargs)
    
    # Add average line
    fig.add_trace(
        go.Scatter(
            x=df[x_col],
            y=[avg] * len(df),
            mode='lines',
            name=avg_label,
            line=dict(color='red', width=2, dash='dash')
        )
    )
    
    # Common layout adjustments
    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(tickmode='linear', dtick=5) if x_col == 'Year' else None
    )
    
    return fig

def highlight_years_of_interest(fig, years_dict):
    """
    Add vertical lines to highlight years of interest on a time series chart.
    
    Args:
        fig (plotly.graph_objects.Figure): The figure to add lines to
        years_dict (dict): Dictionary mapping years to event descriptions
        
    Returns:
        plotly.graph_objects.Figure: The updated figure
    """
    for year, event in years_dict.items():
        fig.add_vline(
            x=year,
            line_dash="dash",
            line_color="rgba(0, 0, 0, 0.5)",
            annotation_text=event,
            annotation_position="top right"
        )
    
    return fig