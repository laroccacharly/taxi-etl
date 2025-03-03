import os
import requests
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from datetime import datetime
from .paths import get_data_path
from pydantic import BaseModel


class TaxiDataRequest(BaseModel):
    year: int = 2023
    month: int = 1  # Only a single month is supported.
    color: str = "yellow"
    output_dir: Path = get_data_path()  


def get_data(request: TaxiDataRequest) -> pd.DataFrame:
    """
    Download and load NYC Taxi data based on the TaxiDataRequest.
    
    Downloads and loads the parquet file corresponding to the specified year, month, and color.
    
    Args:
        request: TaxiDataRequest object containing:
            - year: Year for the data.
            - month: Month (as an integer) for the data download.
            - color: Type of taxi data ('yellow', 'green', 'fhv', or 'all').
            - output_dir: Directory to save the downloaded file.
            
    Returns:
        A pandas DataFrame containing the data from the downloaded parquet file.
    """
    # Ensure output directory exists
    output_dir = Path(request.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Validate data type
    if request.color not in ["yellow", "green", "fhv", "all"]:
        raise ValueError("color must be one of 'yellow', 'green', 'fhv', or 'all'")
    
    # Validate month
    if request.month < 1 or request.month > 12:
        raise ValueError("Month must be between 1 and 12")
    
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    
    # Build filename and URL
    filename = f"{request.color}_tripdata_{request.year}-{request.month:02d}.parquet"
    url = f"{base_url}/{filename}"
    output_file = output_dir / filename
    
    # Download the file if it does not exist
    if not output_file.exists():
        try:
            print(f"Downloading {url}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
    
            with open(output_file, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
    
            print(f"Successfully downloaded {filename}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error downloading {filename}: {e}")
    else:
        print(f"File {filename} already exists. Skipping download.")
    
    # Load data from the downloaded file
    try:
        df = pd.read_parquet(str(output_file))
    except Exception as e:
        raise ValueError(f"Error loading {output_file}: {e}")
    
    return df


def view_data():
    request = TaxiDataRequest()  # Adjust parameters as needed.
    df = get_data(request)
    print(df.head())


if __name__ == "__main__":
    view_data()