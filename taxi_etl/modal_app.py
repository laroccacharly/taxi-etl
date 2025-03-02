import modal 
import os
from pathlib import Path

image = (modal.Image.debian_slim(python_version="3.12")
    .pip_install("uv")
    .add_local_file("pyproject.toml", "/root/pyproject.toml", copy=True)
    .run_commands("uv pip install --system --compile-bytecode -r /root/pyproject.toml")
    .add_local_python_source("taxi_etl")
    .add_local_python_source("ui")
)

volume_path = "/taxi_etl"
os.environ["VOLUME_PATH"] = volume_path
volume = modal.Volume.from_name("taxi_etl", create_if_missing=True)

def get_volume_path():
    return Path(volume_path)

volumes = {
    volume_path: volume,
}

app_name = "taxi-etl"
app = modal.App(name=app_name)

def get_modal_function_config(): 
    return {
        "image": image,
        "volumes": volumes,
        "cpu": (2.0),
        "memory": (1024*2, 3*1024),
    }
