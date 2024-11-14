#!/bin/bash

set -e

python3 -m venv venv
venv/bin/pip install geopandas psycopg2-binary openpyxl geoalchemy2 matplotlib

./venv/bin/python ingest_polygons.py

./ingest_rasters.sh
