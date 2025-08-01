import csv
from pathlib import Path

# from adbc_driver_postgresql import dbapi
# import pandas as pd
# import geopandas as gpd
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from {{ cookiecutter.module_name }}.config import DATA_DIR, TABULAR_CONNECTION_STRING, SPATIAL_CONNECTION_STRING

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
            filename = DATA_DIR / f"{table}.csv"
            with open(filename, 'w', newline='') as csv_file:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
            print(f"Saved to {filename}")
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
    # TODO: Upgrade PostGIS so can use ST_AsGeoJSON, then try this again
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

    skip_properties = set(["shape", "geometry"])

    for table in tables:
        sql = f"select *, ST_AsGeoJSON(ST_Transform(shape, 4326)) as geometry from {table}"
        rows = [row._asdict() for row in session.execute(text(sql)).all()]
        if len(rows) > 0:
            new_feature_collection = empty_feature_collection.copy()
            with open(DATA_DIR / f"{table}.geojson", 'w', newline='') as json_file:
                for row in rows:
                    new_feature = empty_feature.copy()
                    new_feature['properties'] = {key: value for key, value in row.items() if key not in skip_properties}
                    new_feature['geometry'] = json.loads(row['geometry'])
                    new_feature_collection['features'].append(new_feature)
        # Alternatively, using geopandas:
        # gdf = geopandas.read_postgis(sql, engine)
        # gdf.to_file(DATA_DIR / f"{table}.geojson", driver="GeoJSON")
    """
    return None
