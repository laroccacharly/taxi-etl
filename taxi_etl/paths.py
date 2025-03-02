from pathlib import Path
from .modal_app import get_volume_path
from .config import is_dev


def get_data_path():
    if is_dev():
        return Path("data")
    else:
        return get_volume_path()