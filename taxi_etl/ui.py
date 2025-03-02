import streamlit as st
from .get_data import view_data, get_data

def run_ui(): 
    # Set page title
    st.set_page_config(page_title="NYC Taxi Data Explorer", layout="wide")

    # Main header
    st.title("NYC Taxi Data Explorer 🚕")

    # Add some description text
    st.write("Explore NYC taxi trip data with this interactive application.")

    # NYC Taxi Data section
    st.subheader("NYC Taxi Data")
    
    # Add a button to load the data
    if st.button("Load NYC Taxi Data"):
        with st.spinner("Loading taxi data... This might take a moment."):
            try:
                # Get the data
                df = get_data()
                
                # Display basic statistics
                st.subheader("Data Overview")
                st.write(f"Total records: {len(df):,}")
                
                # Display the dataframe
                st.subheader("Sample Data")
                st.dataframe(df.head(100))
                
                # Add some basic visualizations
                st.subheader("Data Visualization")
                
                # Show columns
                st.write("Available columns:")
                st.write(", ".join(df.columns.tolist()))
                
                # If there's a datetime column, show trips by hour
                if 'tpep_pickup_datetime' in df.columns:
                    st.subheader("Trips by Hour")
                    df['hour'] = df['tpep_pickup_datetime'].dt.hour
                    hourly_counts = df['hour'].value_counts().sort_index()
                    st.bar_chart(hourly_counts)
                
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
                st.info("Try downloading the data first using the sidebar options.")

    # Add a sidebar
    with st.sidebar:
        st.header("Data Options")
        
        # Add data download options
        st.subheader("Download Data")
        
        year = st.selectbox("Year", options=[2023, 2022, 2021], index=0)
        months = st.multiselect("Months", options=list(range(1, 13)), default=[1])
        data_type = st.selectbox("Data Type", options=["yellow", "green", "fhv"], index=0)
        
        if st.button("Download Selected Data"):
            st.info("This will download the selected data. It may take some time depending on the selection.")
            # This would trigger the download but we'll implement it in a future update
            
        st.markdown("---")
        
        st.header("About")
        st.info("This application allows you to explore NYC taxi trip data.")
        
        # Add a selectbox to the sidebar
        option = st.selectbox(
            'What aspect of the data interests you most?',
            ['Trip duration', 'Fare amounts', 'Pickup/dropoff locations', 'Time patterns', 'Other']
        )
        st.write(f'You selected: {option}')
