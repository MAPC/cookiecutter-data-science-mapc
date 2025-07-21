import os
from pathlib import Path
import urllib.parse

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[2]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"

VIZ_DIR = PROJ_ROOT / "visualizations"
FIGURES_DIR = VIZ_DIR / "figures"
PG_CONNECTION_STRING = f"postgresql://{os.environ['PGUSER']}:{urllib.parse.quote_plus(os.environ['PGPASSWORD'])}@{os.environ['PGHOST']}:{os.environ['PGPORT']}"
TABULAR_CONNECTION_STRING = f"{PG_CONNECTION_STRING}/ds"
SPATIAL_CONNECTION_STRING = f"{PG_CONNECTION_STRING}/gisdata"

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
