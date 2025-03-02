import os
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple
from .paths import get_data_path


def download_nyc_taxi_data(
    year: int = 2023,
    months: List[int] = [1],
    data_type: str = "yellow",
    output_dir: Path = None,
    force_download: bool = False
) -> List[str]:
    """
    Download NYC Taxi data for specified year and months.
    
    Args:
        year: The year to download data for
        months: List of months to download (1-12). If None, downloads all months.
        data_type: Type of data to download ('yellow', 'green', or 'fhv')
        output_dir: Directory to save files to. If None, uses get_volume_path() / 'data'
        force_download: If True, download even if file exists
        
    Returns:
        List of paths to downloaded files
    """
    if months is None:
        months = list(range(1, 13))
    
    if output_dir is None:
        output_dir = get_data_path()
    
    # Convert to Path object if it's a string
    output_dir = Path(output_dir)
    
    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Validate inputs
    if data_type not in ["yellow", "green", "fhv"]:
        raise ValueError("data_type must be one of 'yellow', 'green', or 'fhv'")
    
    for month in months:
        if month < 1 or month > 12:
            raise ValueError("Months must be between 1 and 12")
    
    # Base URL for NYC TLC trip data
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    
    downloaded_files = []
    
    for month in tqdm(months, desc=f"Downloading {data_type} taxi data for {year}"):
        # Format the filename: {data_type}_tripdata_YYYY-MM.parquet
        filename = f"{data_type}_tripdata_{year}-{month:02d}.parquet"
        url = f"{base_url}/{filename}"
        
        output_file = output_dir / filename
        
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
    Load NYC Taxi data from parquet files.
    
    Args:
        file_paths: List of paths to parquet files (can be str or Path objects)
        
    Returns:
        DataFrame with combined data
    """
    dfs = []
    
    for file_path in tqdm(file_paths, desc="Loading data files"):
        try:
            # Convert to string in case it's a Path object
            df = pd.read_parquet(str(file_path))
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    if not dfs:
        raise ValueError("No data files were successfully loaded")
    
    return pd.concat(dfs, ignore_index=True)


def get_data() -> pd.DataFrame:
    files = download_nyc_taxi_data(year=2023, months=[1], data_type="yellow")
    if files:
        return load_taxi_data(files)
    else:
        raise ValueError("No data files were successfully loaded")
    

def view_data():
    df = get_data()
    print(df.head())

if __name__ == "__main__":
    view_data()