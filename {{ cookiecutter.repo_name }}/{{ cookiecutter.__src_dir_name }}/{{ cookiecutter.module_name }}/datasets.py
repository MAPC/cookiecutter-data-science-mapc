import csv
from pathlib import Path

# from adbc_driver_postgresql import dbapi
# import pandas as pd
# import geopandas as gpd
from sqlalchemy import create_engine, select, text
from loguru import logger
from tqdm import tqdm
import typer

from {{ cookiecutter.module_name }}.config import DATA_DIR, TABULAR_CONNECTION_STRING, SPATIAL_CONNECTION_STRING

app = typer.Typer()

def load_tabular_datasets(tables):
    """
    Load tabular data from Postgres and save as CSVs

    Arguments:
    tables -- a list of table names
    """
    engine = create_engine(TABULAR_CONNECTION_STRING)
    session = Session(engine)

    for table in tables:
        rows = [row._asdict() for row in session.execute(text(f"select * from {table}")).all()]
        if len(rows) > 0:
            with open(f"{table}.csv", 'w', newline='') as csv_file:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
        # Alternatively, using pandas:
        # with dbapi.connect(TABULAR_CONNECTION_STRING) as conn:
        #     df = pd.read_sql('SELECT * FROM {table}', conn)
        #     df.to_csv(DATA_DIR / f"{table}.csv", index=False)

def load_spatial_datasets(tables):
    """
    Load spatial data from Postgres and save as GeoJSON

    Arguments:
    tables -- a list of table names
    """
    engine = create_engine(SPATIAL_CONNECTION_STRING)
    session = Session(engine)

    empty_feature_collection = {
        "type": "FeatureCollection",
        "features": []
    }

    empty_feature = {
        "type": "Feature",
        "properties": {},
        "geometry": {}
    }

    skip_properties = new set(["shape", "geometry"])

    for table in tables:
        sql = f"select *, ST_AsGeoJSON(ST_Transform(shape, 4326)) as geometry from {table}"
        rows = [row._asdict() for row in session.execute(text(sql)).all()]
        if len(rows) > 0:
            new_feature_collection = empty_feature_collection.copy()
            with open(f"{table}.geojson", 'w', newline='') as json_file:
                for row in rows:
                    new_feature = empty_feature.copy()
                    new_feature['properties'] = {key: value for key, value in row.items() if key not in skip_properties}
                    new_feature['geometry'] = json.loads(row['geometry'])
                    new_feature_collection['features'].append(new_feature)
        # Alternatively, using geopandas:
        # gdf = geopandas.read_postgis(sql, engine)
        # gdf.to_file(DATA_DIR / f"{table}.geojson", driver="GeoJSON")

@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = DATA_DIR / "input.csv",
    output_path: Path = DATA_DIR / "output.csv",
    # ----------------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Processing dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Processing dataset complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
