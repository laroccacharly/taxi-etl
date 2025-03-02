import os
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple


def download_nyc_taxi_data(
    year: int = 2023,
    months: List[int] = None,
    data_type: str = "yellow",
    output_dir: str = "data",
    force_download: bool = False
) -> List[str]:
    """
    Download NYC taxi trip data as parquet files.
    
    Args:
        year: The year of data to download (default: 2023)
        months: List of months to download (1-12). If None, downloads all months (default: None)
        data_type: Type of taxi data to download - 'yellow', 'green', or 'fhv' (default: 'yellow')
        output_dir: Directory to save the downloaded files (default: 'data')
        force_download: Whether to force download even if file exists (default: False)
        
    Returns:
        List of paths to downloaded parquet files
    """
    # Validate inputs
    if data_type not in ["yellow", "green", "fhv"]:
        raise ValueError("data_type must be one of 'yellow', 'green', or 'fhv'")
    
    if months is None:
        months = list(range(1, 13))
    else:
        for month in months:
            if month < 1 or month > 12:
                raise ValueError("Months must be between 1 and 12")
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Base URL for NYC TLC trip data
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    
    downloaded_files = []
    
    for month in tqdm(months, desc=f"Downloading {data_type} taxi data for {year}"):
        # Format the filename: {data_type}_tripdata_YYYY-MM.parquet
        filename = f"{data_type}_tripdata_{year}-{month:02d}.parquet"
        url = f"{base_url}/{filename}"
        
        output_file = output_path / filename
        
        # Skip if file exists and force_download is False
        if output_file.exists() and not force_download:
            print(f"File {filename} already exists. Skipping download.")
            downloaded_files.append(str(output_file))
            continue
        
        try:
            print(f"Downloading {url}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Get total file size for progress bar
            total_size = int(response.headers.get('content-length', 0))
            
            # Download with progress bar
            with open(output_file, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            
            print(f"Successfully downloaded {filename}")
            downloaded_files.append(str(output_file))
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {filename}: {e}")
            continue
    
    return downloaded_files


def load_taxi_data(file_paths: List[str]) -> pd.DataFrame:
    """
    Load downloaded taxi data into a pandas DataFrame.
    
    Args:
        file_paths: List of paths to parquet files
        
    Returns:
        pandas DataFrame containing the combined data
    """
    dfs = []
    
    for file_path in tqdm(file_paths, desc="Loading data files"):
        try:
            df = pd.read_parquet(file_path)
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    if not dfs:
        raise ValueError("No data files were successfully loaded")
    
    return pd.concat(dfs, ignore_index=True)


if __name__ == "__main__":
    # Example usage
    files = download_nyc_taxi_data(year=2023, months=[1, 2], data_type="yellow")
    if files:
        print(f"Downloaded {len(files)} files")
        
        # Optionally load the data
        # df = load_taxi_data(files)
        # print(f"Loaded data with {len(df)} rows") 