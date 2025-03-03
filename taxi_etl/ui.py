import streamlit as st
import pandas as pd
import numpy as np
from .get_data import get_data

def run_ui(): 
    # Set page title
    st.set_page_config(page_title="NYC Taxi Data Explorer", layout="wide")

    # Main header
    st.title("NYC Taxi Data Explorer 🚕")

    # Add some description text

    # Sidebar for TaxiDataRequest parameters
    with st.sidebar:
        st.header("Data Options")
        
        # Store previous values to detect changes
        previous_options = {}
        if "previous_options" in st.session_state:
            previous_options = st.session_state.previous_options
        
        # Get current selections
        year = st.selectbox("Year", options=[2023, 2022, 2021], index=0, key="year")
        month = st.selectbox("Month", options=list(range(1, 13)), index=0, key="month")
        color = st.selectbox("Taxi Type", options=["yellow", "green", "fhv"], index=0, key="color")
        
        # Check if options have changed
        current_options = {"year": year, "month": month, "color": color}
        if "previous_options" in st.session_state and previous_options != current_options:
            # Clear the dataframe if options changed
            if "df" in st.session_state:
                del st.session_state.df
                st.session_state.data_reset = True
        
        # Store current options for next comparison
        st.session_state.previous_options = current_options
        
        #st.markdown("---")
        #st.header("About")
        #st.info("This application allows you to explore NYC taxi trip data.")

    # Main Content
    data_loaded = False
    
    # Show a notification if data was reset due to option changes
    if "data_reset" in st.session_state and st.session_state.data_reset:
        st.warning("Data options changed. Please load the data again.")
        st.session_state.data_reset = False
        
    if "df" not in st.session_state:
        if st.button("Load NYC Taxi Data"):
            with st.spinner("Loading taxi data... This might take a moment."):
                try:
                    from .get_data import TaxiDataRequest
                    # Create a TaxiDataRequest using sidebar parameters
                    request = TaxiDataRequest(year=year, month=month, color=color)

                    # Get the data
                    df = get_data(request)

                    # Store the data in session state
                    st.session_state.df = df
                    data_loaded = True
                except Exception as e:
                    st.error(f"Error loading data: {str(e)}")
                    st.info("Try downloading the data first using the sidebar options.")
    else:
        data_loaded = True

    if data_loaded:
        df = st.session_state.df

        # Display basic statistics
        st.subheader("Data Overview")
        st.write(f"Total records: {len(df):,}")
        
        
        # Add some basic visualizations
        
        # Show columns
        st.write("Available columns:")
        # Replace the comma-separated list with a table showing column names and types
        column_info = pd.DataFrame({
            'Column Name': df.columns.tolist(),
            'Data Type': [str(df[col].dtype) for col in df.columns],
            'Sample Values': [str(df[col].iloc[:3].tolist()) for col in df.columns],
            'Non-Null Count': [df[col].count() for col in df.columns],
            'Unique Values': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(column_info, use_container_width=True)
        

        st.subheader("Column Distribution Analysis")
        # Use a key to persist the selected column value in session_state
        # Set default to a datetime column if one exists in the dataset
        default_index = 0
        
        # Look for any column with "datetime" in its name
        datetime_cols = [col for col in df.columns if "datetime" in col.lower()]
        if datetime_cols:
            # Use the first datetime column found
            default_index = df.columns.tolist().index(datetime_cols[0])
        
        chosen_column = st.selectbox("Select column to analyze", df.columns.tolist(), index=default_index, key="chosen_column")

        # Create a container for the chart to minimize layout shifts
        chart_container = st.container()

        with chart_container:
            if pd.api.types.is_numeric_dtype(df[chosen_column]):
                unique_count = df[chosen_column].nunique()
                if unique_count > 20:
                    st.info("Column has many unique numeric values. Showing histogram with 20 bins.")
                    hist, bin_edges = np.histogram(df[chosen_column].dropna(), bins=20)
                    # Create a DataFrame with bin labels for proper x-axis display
                    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
                    hist_df = pd.DataFrame({
                        'count': hist,
                        'bin': [f"{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}" for i in range(len(bin_edges)-1)]
                    })
                    hist_df = hist_df.set_index('bin')
                    # Display the histogram with proper bin labels
                    st.bar_chart(hist_df)
                    
                    # Add a table with bin ranges and counts for clarity
                    with st.expander("View histogram data"):
                        st.table(hist_df)
                else:
                    st.bar_chart(df[chosen_column].value_counts().sort_index())
            elif pd.api.types.is_datetime64_any_dtype(df[chosen_column]):
                st.info("Datetime column detected, showing counts by hour if possible.")
                st.bar_chart(df[chosen_column].dt.hour.value_counts().sort_index())
            else:
                st.bar_chart(df[chosen_column].value_counts())

            # Display the dataframe
        st.subheader("Sample Data")
        st.dataframe(df.head(100))