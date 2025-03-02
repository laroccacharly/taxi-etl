from .get_data import download_nyc_taxi_data
from .modal_app import app, get_volume_path, get_modal_function_config

@app.function(**get_modal_function_config()) 
def get_data_modal():
    print("Hello, world!")
    volume_path = get_volume_path()
    print(volume_path)
