from pathlib import Path
from .modal_app import get_volume_path
from .config import is_dev


def get_data_path():
    if is_dev():
        path = Path("data")
        path.mkdir(exist_ok=True)  
        return path
    else:
        return get_volume_path()