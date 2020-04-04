from backend.application.config import BACKEND_CONFIGS as B_CONF
from backend.application.config import BASE_DIR, ROOT_DIR


class BackendSettings:
    # Main paths:
    BASE_DIR = BASE_DIR
    DATA_DIR = f"{ROOT_DIR}/data"
    STATIC_DIR = f"{BASE_DIR}/static"
    # Geospatial Data paths:
    GEOSPATIAL_DIR = f"{BASE_DIR}/geospatial"
    DETAILED_COUNTRIES_FILE_NAME = "US_CAN_CHN_AUS.shp"
    WORLD_FILE_NAME = "GOV_BOUNDS.shp"
    DETAILED_COUNTRIES_FILE_PATH = f"{GEOSPATIAL_DIR}/{DETAILED_COUNTRIES_FILE_NAME}"
    WORLD_FILE_PATH = f"{GEOSPATIAL_DIR}/{WORLD_FILE_NAME}"
    # Main application settings:
    UPDATE_DATA_EVERY_X_HOUR = 6

    # DATABASE:
    DB_NAME = B_CONF["DB_NAME"]
    DB_USER = B_CONF["DB_USER"]
    DB_PASSWORD = B_CONF["DB_PASSWORD"]
    DB_HOST = B_CONF["DB_HOST"]
    DB_PORT = B_CONF["DB_PORT"]
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
