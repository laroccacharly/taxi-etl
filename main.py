from taxi_data import download_nyc_taxi_data, load_taxi_data

def main():
    print("Hello from taxi-etl!")
    
    # Download NYC taxi data (yellow taxi data for January 2023)
    print("Downloading NYC taxi data...")
    files = download_nyc_taxi_data(year=2023, months=[1], data_type="yellow")
    
    if files:
        print(f"Successfully downloaded {len(files)} files:")
        for file in files:
            print(f"  - {file}")
        
        # Uncomment to load the data into a DataFrame
        # df = load_taxi_data(files)
        # print(f"Loaded data with {len(df)} rows")
        # print(df.head())


if __name__ == "__main__":
    main()
