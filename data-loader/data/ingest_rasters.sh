#!/bin/bash

TARGET_SRS="5880"
TEMP_RASTER_PATH="temp_raster.tif"

ingest_raster() {
    gdalwarp -t_srs "EPSG:$TARGET_SRS" "$1" "$TEMP_RASTER_PATH"
    raster2pgsql -I -C -e -Y -F -s "$TARGET_SRS" -d -t 50x50 "$TEMP_RASTER_PATH" "$2" | psql
}

ingest_raster "./rasters/ambdata/GO_Elevacao.tif" "public.map_elevation"
ingest_raster "./rasters/ambdata/GO_Precipitacao.tif" "public.map_precipitation"
ingest_raster "./rasters/ambdata/GO_Temperatura_Media.tif" "public.map_temperature"
ingest_raster "./rasters/mapbiomas/mapbiomas-brazil-collection-90-go-2019.tif" "public.map_lulc"
