# Farm Planner Database

This project contains resources to deploy a PostgreSQL spatial database designed to model agricultural productivity. Developed for analyzing productivity in Goiás, Brazil, this database addresses the challenges of unifying agricultural data from diverse official sources.

## Table of Contents

* Motivation and Goals
* Features
* Deployment
* Interacting with the Database
* Related Work

## Motivation and Goals

The primary motivation for this project is to facilitate the analysis of agricultural productivity data for Goiás, Brazil. The lack of a unified data source covering the region’s productivity information led to the development of this database, which integrates official data from sources like the Pesquisa Agropecuária Municipal by IBGE and the rural properties database by SIGEF.

The database schema mirrors the original schemas of the data sources, with some tables and columns directly corresponding to official publications, while others are customized to support relational modeling and spatial analysis.

With PostGIS enabled for georeferenced data handling, this project aims to support efficient and meaningful ETL processes for spatial data analysis in agriculture.


## Features:

* PostgreSQL with PostGIS: Provides robust support for geospatial data.
* Data Loader Service: A Docker service for loading data from scripts and initializing the schema.
* ETL-Friendly Schema: Modeled for integration and spatial analysis of agricultural productivity data.

## Deployment

The [docker-compose.yaml](docker-compose.yaml) file defines two Docker services:

* `postgis`: A PostgreSQL instance with PostGIS, where the spatial database resides.
* `data_loader`: A Linux instance that initializes the database with schema and data.

The `data_loader` service uses scripts in the [data-loader/](data-loader/) directory:

* A SQL script to initialize the schema.
* A Python script for loading discrete entities.
* A shell script for ingesting raster data.
* A shell script to manage the data loading process.

Note: Due to GitHub’s file size limitations, the actual data is not included in this repository. If you need access to the data, please contact us.

## Volumes

The Docker containers use the following volumes:

* [pgdata/](pgdata/): Mounted by `postgis` to store database files.
* [data/](data/): Mounted by `data_loader` to access the ingestion scripts and raw data.

## Local Deployment

To deploy the services locally:

* Copy the raw data to the data directory.
* Run the following command:

```shell
docker compose up -d
```

This command will start the services and initiate the data ingestion process.


## Interacting with the Database

The postgis service exposes the database on port `5432`. You can find connection details (such as username and password) in [docker-compose.yaml](docker-compose.yaml).

For example queries and visualizations, refer to the [data_exploration.ipynb](data_exploration.ipynb) notebook, which provides insights into interacting with the database.

## Data Insertion Examples

Examples of data insertion can be found in the following files:

* [ingest_rasters.sh](data-loader/data/ingest_rasters.sh)
* [ingest_polygons.py](data-loader/data/ingest_polygons.py)

## Related Work

Research papers are planned using this database. Relevant publications will be added here over time.

* [Modelagem de Dados de Produtividade Agrícola em Goiás](related_work/modelagem_dados_goias.pdf)