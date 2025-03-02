import modal
from taxi_etl.modal_app import app, get_modal_function_config
import subprocess


@app.function(**get_modal_function_config()) 
@modal.web_server(8000)
def run_ui():
    cmd = f"streamlit run ui.py --server.port 8000 --server.enableCORS=false --server.enableXsrfProtection=false"
    subprocess.Popen(cmd, shell=True)