import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import configuration and utilities
import config
from src.data_processing.loader import load_emissions_data, load_per_capita_data
from components.sidebar import add_year_selector, add_country_selector
from components.filters import add_source_filter

# Set page config
st.set_page_config(page_title=f"Country Analysis - {config.APP_TITLE}", 
                   page_icon=config.APP_ICON, 
                   layout="wide")

def main():
    # Page title
    st.title("Country CO2 Emissions Analysis")
    st.write("Analyze CO2 emissions by country, comparing total and per capita metrics.")
    
    # Load data
    emissions_df = load_emissions_data()
    per_capita_df = load_per_capita_data()
    
    # Add sidebar filters
    st.sidebar.header("Filters")
    selected_year = add_year_selector(emissions_df, default=config.DEFAULT_END_YEAR)
    selected_country = add_country_selector(emissions_df)
    selected_sources = add_source_filter(["Coal", "Oil", "Gas", "Cement", "Flaring", "Other"])
    
    # Filter data for selected year
    year_df = emissions_df[emissions_df['Year'] == selected_year]
    year_per_capita_df = per_capita_df[per_capita_df['Year'] == selected_year]
    
    # Top and bottom emitters
    st.header(f"Top and Bottom Emitters in {selected_year}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top total emitters
        top_emitters = year_df.sort_values('Total', ascending=False).head(config.TOP_N_COUNTRIES)
        
        fig1 = px.bar(
            top_emitters,
            y='Country',
            x='Total',
            title=f"Top {config.TOP_N_COUNTRIES} CO2 Emitters (Million Tonnes)",
            height=config.DEFAULT_CHART_HEIGHT,
            orientation='h',
            labels={"Total": "Million Tonnes CO2", "Country": ""},
            color='Total',
            color_continuous_scale=config.CHOROPLETH_COLORSCALE,
            template="plotly_white"
        )
        
        fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        # Top per capita emitters
        top_per_capita = year_per_capita_df.sort_values('Total', ascending=False).head(config.TOP_N_COUNTRIES)
        
        fig2 = px.bar(
            top_per_capita,
            y='Country',
            x='Total',
            title=f"Top {config.TOP_N_COUNTRIES} Per Capita CO2 Emitters (Tonnes per Capita)",
            height=config.DEFAULT_CHART_HEIGHT,
            orientation='h',
            labels={"Total": "Tonnes CO2 per Capita", "Country": ""},
            color='Total',
            color_continuous_scale=config.CHOROPLETH_COLORSCALE,
            template="plotly_white"
        )
        
        fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)
    
    # Country specific analysis
    st.header(f"Detailed Analysis for {selected_country}")
    
    # Filter data for selected country
    country_data = emissions_df[emissions_df['Country'] == selected_country]
    country_per_capita = per_capita_df[per_capita_df['Country'] == selected_country]
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Historical emissions trend
        fig3 = px.line(
            country_data,
            x='Year',
            y='Total',
            title=f"Historical CO2 Emissions for {selected_country}",
            height=config.DEFAULT_CHART_HEIGHT,
            labels={"Total": "Million Tonnes CO2", "Year": "Year"},
            template="plotly_white"
        )
        
        fig3.update_layout(hovermode="x unified")
        st.plotly_chart(fig3, use_container_width=True)
        
    with col4:
        # Per capita trend
        fig4 = px.line(
            country_per_capita,
            x='Year',
            y='Total',
            title=f"Per Capita CO2 Emissions for {selected_country}",
            height=config.DEFAULT_CHART_HEIGHT,
            labels={"Total": "Tonnes CO2 per Capita", "Year": "Year"},
            template="plotly_white"
        )
        
        fig4.update_layout(hovermode="x unified")
        st.plotly_chart(fig4, use_container_width=True)
    
    # Source breakdown for selected country and year
    st.header(f"Emissions Sources for {selected_country} in {selected_year}")
    
    country_year_data = country_data[country_data['Year'] == selected_year]
    
    if not country_year_data.empty:
        # Extract source columns
        source_columns = [s for s in selected_sources if s in country_data.columns]
        source_values = country_year_data[source_columns].iloc[0].tolist()
        
        # Create pie chart
        fig5 = px.pie(
            names=source_columns,
            values=source_values,
            title=f"CO2 Emissions by Source for {selected_country} ({selected_year})",
            height=config.DEFAULT_CHART_HEIGHT,
            color=source_columns,
            color_discrete_map=config.EMISSION_SOURCES_COLORS,
            template="plotly_white"
        )
        
        fig5.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig5, use_container_width=True)
        
        # Source breakdown over time
        st.header(f"Source Trends for {selected_country}")
        
        # Melt the data for stacked area chart
        country_sources = country_data[['Year'] + source_columns].copy()
        country_sources_melted = pd.melt(
            country_sources, 
            id_vars=['Year'], 
            value_vars=source_columns,
            var_name='Source', 
            value_name='Emissions'
        )
        
        # Create stacked area chart
        fig6 = px.area(
            country_sources_melted,
            x='Year',
            y='Emissions',
            color='Source',
            title=f"CO2 Emissions by Source Over Time for {selected_country}",
            height=config.DEFAULT_CHART_HEIGHT,
            labels={"Emissions": "Million Tonnes CO2", "Year": "Year"},
            color_discrete_map=config.EMISSION_SOURCES_COLORS,
            template="plotly_white"
        )
        
        fig6.update_layout(hovermode="x unified")
        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.write(f"No data available for {selected_country} in {selected_year}")

if __name__ == "__main__":
    main()