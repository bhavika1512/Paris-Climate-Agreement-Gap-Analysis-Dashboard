import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add the project directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import configuration
import config

# Set page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main function to run the Streamlit app"""
    
    # Display header
    st.title(config.APP_TITLE)
    st.markdown(config.APP_DESCRIPTION)
    
    # Sidebar
    st.sidebar.title("Navigation")
    st.sidebar.info(
        "This dashboard visualizes CO2 emissions data from the Global Carbon Budget 2022."
    )
    
    st.sidebar.title("About")
    st.sidebar.info(
        "This dashboard is created using Streamlit and Python to visualize "
        "carbon emissions data from the Global Carbon Project."
    )
    
    # Main content
    st.header("Global CO2 Emissions Dashboard")
    st.write("Welcome to the CO2 Emissions Dashboard. Use the navigation to explore different visualizations.")
    
    # Example visualization placeholder (will be replaced with actual data later)
    st.subheader("Sample Visualization")
    
    # Placeholder for visualization
    data = {
        'Year': [2010, 2011, 2012, 2013, 2014, 2015],
        'Emissions': [30, 32, 34, 36, 35, 37]
    }
    df = pd.DataFrame(data)
    
    fig = px.line(df, x='Year', y='Emissions', title='Sample CO2 Emissions Trend')
    st.plotly_chart(fig, use_container_width=True)
    
    # Information about the data
    st.markdown("## Data Source")
    st.write(
        "The data used in this dashboard comes from the Global Carbon Budget 2022 "
        "published by the Global Carbon Project."
    )
    
    # Dataset description
    st.markdown("## Available Datasets")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Total Emissions")
        st.write("Total CO2 emissions in millions of tonnes")
        
    with col2:
        st.markdown("### Per Capita Emissions")
        st.write("CO2 emissions in tonnes per capita")

if __name__ == "__main__":
    main()