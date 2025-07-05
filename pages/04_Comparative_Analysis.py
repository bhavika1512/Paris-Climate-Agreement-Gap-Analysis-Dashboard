import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys
import os

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import configuration and utilities
import config
from src.data_processing.loader import load_emissions_data, load_per_capita_data
from components.sidebar import add_year_selector
from components.filters import add_multi_country_selector

# Set page config
st.set_page_config(page_title=f"Comparative Analysis - {config.APP_TITLE}", 
                   page_icon=config.APP_ICON, 
                   layout="wide")

def main():
    # Page title
    st.title("Comparative CO2 Emissions Analysis")
    st.write("Compare emissions across countries and analyze relationships between different metrics.")
    
    # Load data
    emissions_df = load_emissions_data()
    per_capita_df = load_per_capita_data()
    
    # Add sidebar filters
    st.sidebar.header("Filters")
    selected_year = add_year_selector(emissions_df, default=config.DEFAULT_END_YEAR)
    selected_countries = add_multi_country_selector(emissions_df, max_selections=5)
    
    # Filter data for selected year
    year_emissions = emissions_df[emissions_df['Year'] == selected_year]
    year_per_capita = per_capita_df[per_capita_df['Year'] == selected_year]
    
    # Country comparison
    if selected_countries:
        st.header(f"Country Comparison for {selected_year}")
        
        # Filter data for selected countries
        countries_data = year_emissions[year_emissions['Country'].isin(selected_countries)]
        countries_per_capita = year_per_capita[year_per_capita['Country'].isin(selected_countries)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Total emissions comparison
            fig1 = px.bar(
                countries_data,
                x='Country',
                y='Total',
                title=f"Total Emissions Comparison ({selected_year})",
                height=config.DEFAULT_CHART_HEIGHT,
                labels={"Total": "Million Tonnes CO2", "Country": ""},
                color='Country',
                template="plotly_white"
            )
            
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Per capita comparison
            fig2 = px.bar(
                countries_per_capita,
                x='Country',
                y='Total',
                title=f"Per Capita Emissions Comparison ({selected_year})",
                height=config.DEFAULT_CHART_HEIGHT,
                labels={"Total": "Tonnes CO2 per Capita", "Country": ""},
                color='Country',
                template="plotly_white"
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        # Source breakdown comparison
        st.header(f"Source Breakdown Comparison ({selected_year})")
        
        # Select source columns
        source_columns = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other"]
        
        # Create stacked bar chart
        fig3 = px.bar(
            countries_data,
            x='Country',
            y=source_columns,
            title=f"Emissions by Source ({selected_year})",
            height=config.DEFAULT_CHART_HEIGHT,
            labels={"value": "Million Tonnes CO2", "Country": ""},
            color_discrete_map=config.EMISSION_SOURCES_COLORS,
            template="plotly_white"
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
        # Historical trend comparison
        st.header("Historical Emissions Trend Comparison")
        
        # Filter historical data for selected countries
        countries_history = emissions_df[emissions_df['Country'].isin(selected_countries)]
        
        # Create line chart
        fig4 = px.line(
            countries_history,
            x='Year',
            y='Total',
            color='Country',
            title="Historical Total Emissions Comparison",
            height=config.DEFAULT_CHART_HEIGHT,
            labels={"Total": "Million Tonnes CO2", "Year": "Year"},
            template="plotly_white"
        )
        
        fig4.update_layout(hovermode="x unified")
        st.plotly_chart(fig4, use_container_width=True)
        
        # Per capita historical trend
        countries_pc_history = per_capita_df[per_capita_df['Country'].isin(selected_countries)]
        
        # Create line chart
        fig5 = px.line(
            countries_pc_history,
            x='Year',
            y='Total',
            color='Country',
            title="Historical Per Capita Emissions Comparison",
            height=config.DEFAULT_CHART_HEIGHT,
            labels={"Total": "Tonnes CO2 per Capita", "Year": "Year"},
            template="plotly_white"
        )
        
        fig5.update_layout(hovermode="x unified")
        st.plotly_chart(fig5, use_container_width=True)
    
    # Global scatter analysis
    st.header(f"Total vs. Per Capita Emissions ({selected_year})")
    
    # Join emissions and per capita data
    merged_df = pd.merge(
        year_emissions[['Country', 'Total']],
        year_per_capita[['Country', 'Total']],
        on='Country',
        suffixes=('_total', '_per_capita')
    )
    
    # Create scatter plot
    fig6 = px.scatter(
        merged_df,
        x='Total_total',
        y='Total_per_capita',
        hover_name='Country',
        title=f"Total vs. Per Capita Emissions ({selected_year})",
        height=config.DEFAULT_CHART_HEIGHT,
        labels={
            "Total_total": "Total Emissions (Million Tonnes CO2)",
            "Total_per_capita": "Per Capita Emissions (Tonnes CO2)"
        },
        template="plotly_white",
        log_x=True  # Log scale for total emissions to better visualize distribution
    )
    
    # Highlight selected countries
    if selected_countries:
        selected_data = merged_df[merged_df['Country'].isin(selected_countries)]
        
        fig6.add_trace(
            go.Scatter(
                x=selected_data['Total_total'],
                y=selected_data['Total_per_capita'],
                mode='markers+text',
                marker=dict(size=12, color='red'),
                text=selected_data['Country'],
                textposition='top center',
                name='Selected Countries'
            )
        )
    
    st.plotly_chart(fig6, use_container_width=True)
    
    # Add explanation
    st.markdown("""
    ### Understanding the Scatter Plot
    
    This scatter plot shows the relationship between total emissions and per capita emissions:
    
    - **Upper right**: High total emissions and high per capita emissions (typically wealthy, industrialized countries)
    - **Upper left**: Low total emissions but high per capita emissions (often wealthy but small countries)
    - **Lower right**: High total emissions but lower per capita emissions (typically large developing countries)
    - **Lower left**: Low total and per capita emissions (typically less industrialized countries)
    """)
    
    # Emissions intensity by GDP
    st.header("Additional Comparative Metrics")
    st.write(
        "This dashboard could be extended with additional metrics such as emissions per GDP, "
        "which would provide insights into carbon intensity of different economies."
    )

if __name__ == "__main__":
    main()