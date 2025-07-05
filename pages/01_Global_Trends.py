import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import configuration and utilities
import config
from src.data_processing.loader import load_emissions_data
from components.sidebar import add_year_range_selector
from components.filters import add_source_filter

# Set page config
st.set_page_config(page_title=f"Global Trends - {config.APP_TITLE}", 
                   page_icon=config.APP_ICON, 
                   layout="wide")

def main():
    # Page title
    st.title("Global CO2 Emission Trends")
    st.write("Analyze global emissions trends over time and by source.")
    
    # Load data
    df = load_emissions_data()
    
    # Add sidebar filters
    st.sidebar.header("Filters")
    start_year, end_year = add_year_range_selector(df)
    selected_sources = add_source_filter(["Coal", "Oil", "Gas", "Cement", "Flaring", "Other"])
    
    # Filter data based on year range
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    
    # Global trends over time
    st.header("Global Emissions Over Time")
    
    # Calculate global totals by year
    global_by_year = filtered_df.groupby('Year').agg({'Total': 'sum'}).reset_index()
    
    # Create time series chart
    fig1 = px.line(
        global_by_year, 
        x='Year', 
        y='Total',
        title="Total Global CO2 Emissions (Million Tonnes)",
        height=config.DEFAULT_CHART_HEIGHT,
        labels={"Total": "Million Tonnes CO2", "Year": "Year"},
        template="plotly_white"
    )
    
    fig1.update_layout(
        xaxis=dict(tickmode='linear', dtick=5),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Source breakdown over time
    st.header("Emissions by Source Over Time")
    
    # Calculate global totals by year and source
    source_columns = [s for s in selected_sources if s in filtered_df.columns]
    if source_columns:
        global_by_source = filtered_df.groupby('Year')[source_columns].sum().reset_index()
        global_by_source_melted = pd.melt(
            global_by_source, 
            id_vars=['Year'], 
            value_vars=source_columns,
            var_name='Source', 
            value_name='Emissions'
        )
        
        # Create stacked area chart
        fig2 = px.area(
            global_by_source_melted, 
            x='Year', 
            y='Emissions',
            color='Source',
            title="Global CO2 Emissions by Source (Million Tonnes)",
            height=config.DEFAULT_CHART_HEIGHT,
            labels={"Emissions": "Million Tonnes CO2", "Year": "Year"},
            color_discrete_map=config.EMISSION_SOURCES_COLORS,
            template="plotly_white"
        )
        
        fig2.update_layout(
            xaxis=dict(tickmode='linear', dtick=5),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Year-over-year changes
    st.header("Annual Change in Global Emissions")
    
    # Calculate year-over-year percent changes
    global_by_year['YoY_Change'] = global_by_year['Total'].pct_change() * 100
    
    # Remove the first row which has NaN for YoY change
    yoy_df = global_by_year.dropna(subset=['YoY_Change'])
    
    # Create bar chart for YoY changes
    fig3 = px.bar(
        yoy_df,
        x='Year',
        y='YoY_Change',
        title="Year-over-Year Change in Global CO2 Emissions (%)",
        height=config.DEFAULT_CHART_HEIGHT,
        labels={"YoY_Change": "% Change", "Year": "Year"},
        template="plotly_white",
        color='YoY_Change',
        color_continuous_scale=['red', 'white', 'green'],
        range_color=[-max(abs(yoy_df['YoY_Change'])), max(abs(yoy_df['YoY_Change']))]
    )
    
    fig3.update_layout(
        xaxis=dict(tickmode='linear', dtick=5),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Additional context
    st.markdown("### About the Data")
    st.write(
        "This visualization shows global CO2 emissions trends based on data from the Global Carbon Budget 2022. "
        "The data includes emissions from various sources including coal, oil, gas, cement production, and flaring."
    )
    
    # Notable events in emissions history
    st.markdown("### Notable Events")
    events = [
        {"year": 1973, "event": "Oil Crisis", "description": "Global oil shortages led to temporary emissions reductions."},
        {"year": 1991, "event": "Dissolution of Soviet Union", "description": "Economic contraction in former Soviet states reduced industrial emissions."},
        {"year": 2008, "event": "Global Financial Crisis", "description": "Economic downturn reduced global emissions temporarily."},
        {"year": 2020, "event": "COVID-19 Pandemic", "description": "Lockdowns and economic slowdown caused a significant drop in emissions."}
    ]
    
    events_df = pd.DataFrame(events)
    st.dataframe(events_df)

if __name__ == "__main__":
    main()