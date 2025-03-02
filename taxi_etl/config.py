import os

def is_dev(): 
    value = os.environ.get("APP_ENV", "").lower()
    return value in ("dev", "development")

def is_prod():
    value = os.environ.get("APP_ENV", "").lower()
    return value in ("prod", "production")
