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
from components.sidebar import add_year_range_selector, add_year_selector
from components.filters import add_region_filter

# Set page config
st.set_page_config(page_title=f"Emission Sources - {config.APP_TITLE}", 
                   page_icon=config.APP_ICON, 
                   layout="wide")

def main():
    # Page title
    st.title("CO2 Emission Sources Analysis")
    st.write("Analyze the contribution of different emission sources and how they've changed over time.")
    
    # Load data
    df = load_emissions_data()
    
    # Add sidebar filters
    st.sidebar.header("Filters")
    start_year, end_year = add_year_range_selector(df)
    selected_year = add_year_selector(df, default=config.DEFAULT_END_YEAR, label="Focus Year")
    selected_regions = add_region_filter()
    
    # Filter data based on year range
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    
    # Filter data for selected year
    year_df = df[df['Year'] == selected_year]
    
    # Global source breakdown for selected year
    st.header(f"Global Emission Sources in {selected_year}")
    
    # Calculate global totals by source for selected year
    source_columns = ["Coal", "Oil", "Gas", "Cement", "Flaring", "Other"]
    global_sources = year_df[source_columns].sum()
    
    # Create pie chart
    fig1 = px.pie(
        names=global_sources.index,
        values=global_sources.values,
        title=f"Global CO2 Emissions by Source ({selected_year})",
        height=config.DEFAULT_CHART_HEIGHT,
        color=global_sources.index,
        color_discrete_map=config.EMISSION_SOURCES_COLORS,
        template="plotly_white"
    )
    
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)
    
    # Source contribution over time
    st.header("Evolution of Emission Sources")
    
    # Calculate global totals by year and source
    source_by_year = filtered_df.groupby('Year')[source_columns].sum().reset_index()
    
    # Calculate percentage contribution
    for source in source_columns:
        source_by_year[f"{source}_pct"] = (source_by_year[source] / source_by_year[source_columns].sum(axis=1)) * 100
    
    # Melt the data for area chart of percentages
    pct_columns = [f"{source}_pct" for source in source_columns]
    source_pct_melted = pd.melt(
        source_by_year, 
        id_vars=['Year'], 
        value_vars=pct_columns,
        var_name='Source', 
        value_name='Percentage'
    )
    
    # Clean source names for display
    source_pct_melted['Source'] = source_pct_melted['Source'].str.replace('_pct', '')
    
    # Create stacked area chart for percentages
    fig2 = px.area(
        source_pct_melted,
        x='Year',
        y='Percentage',
        color='Source',
        title="Relative Contribution of Emission Sources Over Time (%)",
        height=config.DEFAULT_CHART_HEIGHT,
        labels={"Percentage": "Contribution (%)", "Year": "Year"},
        color_discrete_map=config.EMISSION_SOURCES_COLORS,
        template="plotly_white"
    )
    
    fig2.update_layout(
        xaxis=dict(tickmode='linear', dtick=5),
        hovermode="x unified",
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Source emissions over time (absolute values)
    st.header("Absolute Emissions by Source")
    
    # Melt the data for line chart
    source_melted = pd.melt(
        source_by_year, 
        id_vars=['Year'], 
        value_vars=source_columns,
        var_name='Source', 
        value_name='Emissions'
    )
    
    # Create line chart
    fig3 = px.line(
        source_melted,
        x='Year',
        y='Emissions',
        color='Source',
        title="Global CO2 Emissions by Source Over Time",
        height=config.DEFAULT_CHART_HEIGHT,
        labels={"Emissions": "Million Tonnes CO2", "Year": "Year"},
        color_discrete_map=config.EMISSION_SOURCES_COLORS,
        template="plotly_white"
    )
    
    fig3.update_layout(
        xaxis=dict(tickmode='linear', dtick=5),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Regional source analysis
    if selected_regions:
        st.header(f"Source Analysis by Region ({selected_year})")
        
        # Filter countries by selected regions
        region_countries = []
        for region in selected_regions:
            if region in config.REGIONS:
                region_countries.extend(config.REGIONS[region])
        
        # Filter data for selected regions and year
        region_df = year_df[year_df['ISO 3166-1 alpha-3'].isin(region_countries)]
        
        if not region_df.empty:
            # Group by region
            region_map = {}
            for region in selected_regions:
                for country_code in config.REGIONS[region]:
                    region_map[country_code] = region
            
            region_df['Region'] = region_df['ISO 3166-1 alpha-3'].map(region_map)
            region_sources = region_df.groupby('Region')[source_columns].sum().reset_index()
            
            # Create grouped bar chart
            region_sources_melted = pd.melt(
                region_sources, 
                id_vars=['Region'], 
                value_vars=source_columns,
                var_name='Source', 
                value_name='Emissions'
            )
            
            fig4 = px.bar(
                region_sources_melted,
                x='Region',
                y='Emissions',
                color='Source',
                title=f"CO2 Emissions by Source and Region ({selected_year})",
                height=config.DEFAULT_CHART_HEIGHT,
                labels={"Emissions": "Million Tonnes CO2", "Region": ""},
                color_discrete_map=config.EMISSION_SOURCES_COLORS,
                template="plotly_white",
                barmode='group'
            )
            
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.write("No data available for selected regions in the chosen year.")
    
    # Source intensity analysis
    st.header("Source Intensity Analysis")
    st.write(
        "This section analyzes which countries have the highest intensity of specific emission sources "
        "relative to their total emissions."
    )
    
    # Calculate source intensity (% of total emissions)
    source_intensity = year_df.copy()
    for source in source_columns:
        source_intensity[f"{source}_intensity"] = (source_intensity[source] / source_intensity['Total']) * 100
    
    # Allow user to select a source for intensity analysis
    selected_source = st.selectbox(
        "Select emission source for intensity analysis:",
        options=source_columns,
        index=0
    )
    
    # Filter out countries with very small total emissions to avoid outliers
    min_emissions = 10  # Minimum emissions threshold in million tonnes
    significant_countries = source_intensity[source_intensity['Total'] >= min_emissions]
    
    # Get top countries by source intensity
    intensity_column = f"{selected_source}_intensity"
    top_by_intensity = significant_countries.sort_values(intensity_column, ascending=False).head(config.TOP_N_COUNTRIES)
    
    # Create horizontal bar chart
    fig5 = px.bar(
        top_by_intensity,
        y='Country',
        x=intensity_column,
        title=f"Top {config.TOP_N_COUNTRIES} Countries by {selected_source} Intensity ({selected_year})",
        height=config.DEFAULT_CHART_HEIGHT,
        orientation='h',
        labels={intensity_column: f"% of Total Emissions", "Country": ""},
        color=intensity_column,
        color_continuous_scale="Viridis",
        template="plotly_white"
    )
    
    fig5.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig5, use_container_width=True)

if __name__ == "__main__":
    main()