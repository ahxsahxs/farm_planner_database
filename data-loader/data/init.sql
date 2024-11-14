CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_raster;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
SET postgis.gdal_enabled_drivers = 'ENABLE_ALL';


ALTER TABLE IF EXISTS public.facility DROP CONSTRAINT IF EXISTS fk_facility_municipality CASCADE;
ALTER TABLE IF EXISTS public.farm DROP CONSTRAINT IF EXISTS fk_farm_municipality CASCADE;
ALTER TABLE IF EXISTS public.municipality DROP CONSTRAINT IF EXISTS fk_municipality_region CASCADE;
ALTER TABLE IF EXISTS public.plot DROP CONSTRAINT IF EXISTS fk_plot_commodity CASCADE;
ALTER TABLE IF EXISTS public.plot DROP CONSTRAINT IF EXISTS fk_plot_farm CASCADE;
ALTER TABLE IF EXISTS public.commodity_productivity DROP CONSTRAINT IF EXISTS fk_commodity_productivity_municipality CASCADE;
ALTER TABLE IF EXISTS public.commodity_productivity DROP CONSTRAINT IF EXISTS fk_commodity_productivity_commodity CASCADE;
ALTER TABLE IF EXISTS public.region DROP CONSTRAINT IF EXISTS fk_region_country CASCADE;
ALTER TABLE IF EXISTS public.plot DROP CONSTRAINT IF EXISTS fk_region_country CASCADE;

DROP TABLE IF EXISTS public.public_road CASCADE;

DROP TABLE IF EXISTS public.commodity_productivity CASCADE;
DROP TABLE IF EXISTS public.commodity CASCADE;
DROP TABLE IF EXISTS public.commodity_group CASCADE;

DROP TABLE IF EXISTS public.plot CASCADE;
DROP TABLE IF EXISTS public.farm CASCADE;
DROP TABLE IF EXISTS public.facility CASCADE;

DROP TABLE IF EXISTS public.municipality CASCADE;
DROP TABLE IF EXISTS public.region CASCADE;
DROP TABLE IF EXISTS public.country CASCADE;


CREATE TABLE IF NOT EXISTS public.commodity_group
(
    ibge_code int NOT NULL,
    group_name character varying NOT NULL,
    CONSTRAINT commodity_group_pkey PRIMARY KEY (ibge_code)
);
CREATE TABLE IF NOT EXISTS public.commodity
(
    id bigserial NOT NULL,
    commodity_name character varying NOT NULL,
    group_id int NOT NULL,
    CONSTRAINT commodity_pkey PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS public.country
(
    id bigserial NOT NULL,
    country_name character varying NOT NULL,
    CONSTRAINT country_pkey PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS public.region
(
    id bigserial NOT NULL,
    region_name character varying NOT NULL,
    country_id bigserial NOT NULL,
    CONSTRAINT region_pkey PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS public.municipality
(
    ibge_code bigserial NOT NULL,
    municipality_name character varying NOT NULL,
    region_id bigserial NOT NULL,
    geom geometry(MULTIPOLYGON, 5880),
    CONSTRAINT municipality_pkey PRIMARY KEY (ibge_code)
);
CREATE TABLE IF NOT EXISTS public.commodity_productivity
(
    commodity_id bigserial not null,
    municipality_id bigserial not null,
    year int not null,
    cultivated_area double precision NOT NULL,
    production_value double precision NOT NULL,
    CONSTRAINT fk_commodity_productivity PRIMARY KEY (commodity_id, municipality_id, year)
);
CREATE TABLE IF NOT EXISTS public.facility
(
    id bigserial NOT NULL,
    facility_name character varying NOT NULL,
    facility_type character varying NOT NULL,
    facility_capacity int NOT NULL,
    municipality_id bigserial not null,
    geom geometry(POINT, 5880) NOT NULL,
    CONSTRAINT facility_pkey PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS public.farm
(
    id bigserial NOT NULL,
    farm_name character varying NOT NULL,
    municipality_id bigserial NOT NULL,
    farm_type character varying NOT NULL,
    farm_description character varying,
    geom geometry(MULTIPOLYGON, 5880) NOT NULL,
    CONSTRAINT farm_pkey PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS public.plot
(
    id bigserial NOT NULL,
    farm_id bigserial NOT NULL,
    commodity_id bigserial,
    commodity_group_id bigserial,
    date_start date,
    date_end date,
    geom geometry(MULTIPOLYGON, 5880),
    CONSTRAINT plot_pkey PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS public.public_road
(
    id bigserial NOT NULL,
    road_name character varying NOT NULL,
    road_type character varying NOT NULL,
    geom geometry(MULTILINESTRING, 5880) NOT NULL,
    CONSTRAINT public_road_pkey PRIMARY KEY (id)
);

-- ALTER TABLE IF EXISTS public.facility
--     ADD CONSTRAINT fk_facility_municipality FOREIGN KEY (municipality_id)
--     REFERENCES public.municipality (ibge_code) MATCH SIMPLE
--     ON UPDATE CASCADE
--     ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.farm
    ADD CONSTRAINT fk_farm_municipality FOREIGN KEY (municipality_id)
    REFERENCES public.municipality (ibge_code) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.municipality
    ADD CONSTRAINT fk_municipality_region FOREIGN KEY (region_id)
    REFERENCES public.region (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
   
ALTER TABLE IF EXISTS public.commodity_productivity
    ADD CONSTRAINT fk_commodity_productivity_municipality FOREIGN KEY (municipality_id)
    REFERENCES public.municipality (ibge_code) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
   
ALTER TABLE IF EXISTS public.commodity
    ADD CONSTRAINT fk_commodity_commodity_group FOREIGN KEY (group_id)
    REFERENCES public.commodity_group (ibge_code) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
   
ALTER TABLE IF EXISTS public.commodity_productivity
    ADD CONSTRAINT fk_commodity_productivity_commodity FOREIGN KEY (commodity_id)
    REFERENCES public.commodity (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.plot
    ADD CONSTRAINT fk_plot_commodity FOREIGN KEY (commodity_id)
    REFERENCES public.commodity (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.plot
    ADD CONSTRAINT fk_plot_commodity_group FOREIGN KEY (commodity_group_id)
    REFERENCES public.commodity_group (ibge_code) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.plot
    ADD CONSTRAINT fk_plot_farm FOREIGN KEY (farm_id)
    REFERENCES public.farm (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.region
    ADD CONSTRAINT fk_region_country FOREIGN KEY (country_id)
    REFERENCES public.country (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;
 