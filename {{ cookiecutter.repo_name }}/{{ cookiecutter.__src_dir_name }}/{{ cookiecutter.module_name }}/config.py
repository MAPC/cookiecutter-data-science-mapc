import os
from pathlib import Path
import urllib.parse

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
try:
    DATA_DIR = Path(os.environ['DATA_DIR'])
    VIZ_DIR = Path(os.environ['VIZ_DIR'])
    FIGURES_DIR = VIZ_DIR / "figures"
    PG_CONNECTION_STRING = f"postgresql://{os.environ['PGUSER']}:{urllib.parse.quote_plus(os.environ['PGPASSWORD'])}@{os.environ['PGHOST']}:{os.environ['PGPORT']}"
    TABULAR_CONNECTION_STRING = f"{PG_CONNECTION_STRING}/ds"
    SPATIAL_CONNECTION_STRING = f"{PG_CONNECTION_STRING}/gisdata"
except ValueError:
    print("Warning: Unable to configure project constants from environment variables: check that the .env file exists and has the necessary entries")
