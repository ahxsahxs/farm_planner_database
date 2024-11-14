from sqlalchemy import create_engine, sql
import os
import geopandas
import pandas as pd

# %%
MUNICIPALITIES_SHAPEFILE = './polygons/administrativo/BR_Municipios_2020/BR_Municipios_2020.shp'
SIGEF_RURAL_PROPS_SHAPEFILE = './polygons/administrativo/Sigef Brasil_GO/Sigef Brasil_GO.shp'
SILOS_SHAPEFILE = './polygons/infraestrutura/armazens-silos/armazens-silos.shp'
REFRIGERATOR_SHAPEFILE = './polygons/infraestrutura/frigorificos/frigorificos.shp'
ROADS_SHAPEFILE = './polygons/geociencias/ibge_bc250_shapefile._2023_11_23/rod_trecho_rodoviario_l.shp'
IRRIGATION_SHAPEFILE = './polygons/area_irrigada/area_irrigada.shp'
PAM_CSV = './polygons/PAM/PAM_2021_2023_goias.xlsx'
LML_STATES_SHAPEFILE = './polygons/geociencias/ibge_bc250_shapefile._2023_11_23/lml_unidade_federacao_a.shp'

class Datasets:
    # ADMINISTRATIVO
    MUNICIPALITIES = geopandas.read_file(MUNICIPALITIES_SHAPEFILE).to_crs('EPSG:5880')
    RURAL_PROPS = geopandas.read_file(SIGEF_RURAL_PROPS_SHAPEFILE).to_crs('EPSG:5880')
    # INFRAESTRUTURA
    SILOS = geopandas.read_file(SILOS_SHAPEFILE).to_crs('EPSG:5880')
    REFRIGERATORS = geopandas.read_file(REFRIGERATOR_SHAPEFILE).to_crs('EPSG:5880')
    ROADS = geopandas.read_file(ROADS_SHAPEFILE).to_crs('EPSG:5880')
    # PRODUÇÃO
    IRRIGATION = geopandas.read_file(IRRIGATION_SHAPEFILE).to_crs('EPSG:5880')
    PAM = pd.read_excel(PAM_CSV, index_col=list(range(6)))
    # MISC
    LML_UNITIES = geopandas.read_file(LML_STATES_SHAPEFILE).to_crs('EPSG:5880')
    
    

DATASETS = Datasets()

# %%
DATASETS.PAM.Medida = DATASETS.PAM.replace('...', pd.NA).replace('-', pd.NA).Medida.fillna(0)
pam_df = (Datasets.PAM.reset_index()
          .replace({
              'Área plantada ou destinada à colheita (Hectares)': 'Area',
              'Valor da produção (Mil Reais)': 'Value',
          })
          .drop('Nível', axis=1))
pam_df.rename({
    'Cód.': 'Code',
    'Variável': 'Variable',
    'Ano': 'Year',
    'Município': 'Municipality',
    'Produto das lavouras temporárias e permanentes': 'Product',
    'Medida': 'Measure'
}, axis=1, inplace=True)
pam_df['Municipality'] = [x.replace(' (GO)', '') for x in pam_df['Municipality']]
pam_df.replace('Abacaxi*', 'Abacaxi', inplace=True)
pam_df.replace('Coco-da-baía*', 'Coco-da-baía', inplace=True)

commodities_mapping = {
    'Soybean': {
        'ibge_code': 39,
        'commodities': ['Soja (em grão)']
    },
    'Sugar cane': {
        'ibge_code': 20,
        'commodities': ['Cana-de-açúcar', 'Cana para forragem',]
    },
    'Rice': {
        'ibge_code': 40,
        'commodities': ['Arroz (em casca)',]
    },
    'Cotton': {
        'ibge_code': 62,
        'commodities': ['Algodão arbóreo (em caroço)', 'Algodão herbáceo (em caroço)',]
    },
    'Other Temporary Crops': {
        'ibge_code': 41,
        'commodities': ['Abacaxi', 'Alho', 'Amendoim (em casca)', 'Aveia (em grão)', 'Batata-doce', 'Batata-inglesa', 'Cebola','Centeio (em grão)', 'Cevada (em grão)','Ervilha (em grão)', 'Fava (em grão)', 'Feijão (em grão)', 'Fumo (em folha)', 'Girassol (em grão)', 'Linho (semente)', 'Mandioca', 'Melancia', 'Melão', 'Milho (em grão)', 'Palmito', 'Pimenta-do-reino', 'Rami (fibra)','Sisal ou agave (fibra)', 'Sorgo (em grão)','Tangerina', 'Tomate', 'Trigo (em grão)', 'Triticale (em grão)']
    },
    'Coffee': {
        'ibge_code': 46,
        'commodities': ['Café (em grão) Total', 'Café (em grão) Arábica','Café (em grão) Canephora']
    },
    'Citrus': {
        'ibge_code': 47,
        'commodities': ['Laranja', 'Limão',]
    },
    'Palm Oil': {
        'ibge_code': 35,
        'commodities': ['Dendê (cacho de coco)',]
    },
    'Other Perennial Crops': {
        'ibge_code': 48,
        'commodities': ['Abacate', 'Azeitona','Banana (cacho)', 'Açaí', 'Alfafa fenada', 'Borracha (látex coagulado)', 'Borracha (látex líquido)', 'Cacau (em amêndoa)', 'Caju',  'Caqui', 'Castanha de caju', 'Coco-da-baía', 'Erva-mate (folha verde)', 'Chá-da-índia (folha verde)', 'Figo','Goiaba','Guaraná (semente)', 'Juta (fibra)', 'Maçã', 'Malva (fibra)', 'Mamão','Mamona (baga)', 'Manga', 'Maracujá', 'Marmelo','Noz (fruto seco)','Pera', 'Pêssego', 'Tungue (fruto seco)', 'Urucum (semente)', 'Uva']
    }
}
commodity_groups = pd.DataFrame.from_records([
    {'ibge_code': group_info['ibge_code'], 'group_name': group_name}
    for group_name, group_info in commodities_mapping.items()
])

commodities = pd.DataFrame.from_records([
    {'commodity_name': commodity, 'group_id': group_info['ibge_code']}
    for group_name, group_info in commodities_mapping.items()
    for commodity in group_info['commodities'] 
])
commodities['id'] = [idx+1 for idx in commodities.index]

commodities

# %%
pam_df = pam_df.replace('Total', pd.NA).dropna().replace({
    commodity_name: commodity_id
    for commodity_id, commodity_name in zip(commodities.id, commodities.commodity_name)
})
pam_area_df = pam_df[pam_df.Variable == 'Area'][['Code', 'Year', 'Product', 'Measure']]
pam_value_df = pam_df[pam_df.Variable == 'Value'][['Code', 'Year', 'Product', 'Measure']]

pam_area_df = (pam_area_df.set_index(['Code', 'Year', 'Product'])
               .rename({'Measure': 'cultivated_area'}, axis=1))
pam_value_df = (pam_value_df.set_index(['Code', 'Year', 'Product'])
                .rename({'Measure': 'production_value'}, axis=1))

commodity_productivity = (pd.concat([pam_area_df, pam_value_df], axis=1)
                          .reset_index().rename({
                              'Code': 'municipality_id',
                              'Year': 'year',
                              'Product': 'commodity_id'
                            }, axis=1))
commodity_productivity

# %%
countries = pd.DataFrame.from_records([
    {'id': 1, 'country_name': 'Brazil'}
])
regions = pd.DataFrame.from_records([
    {'id':1, 'region_name': 'Goiás', 'country_id': 1}
])

municipalities = Datasets.MUNICIPALITIES
municipalities = municipalities[municipalities.SIGLA_UF == 'GO']
municipalities = (municipalities[['CD_MUN', 'NM_MUN', 'geometry']]
                  .rename({
                    'CD_MUN': 'ibge_code',
                    'NM_MUN': 'municipality_name',
                    'geometry': 'geom',
                  }, axis=1).set_geometry('geom'))
municipalities['region_id'] = 1
municipalities['ibge_code'] = [int(x) for x in municipalities['ibge_code']]
municipalities

# %%
go_buffer_50km = (Datasets.LML_UNITIES[Datasets.LML_UNITIES.sigla == 'GO']
                  .union_all()
                  .buffer(50000))
go_buffer_50km

# %%
silos = Datasets.SILOS.clip(go_buffer_50km)
refrigerators = Datasets.REFRIGERATORS.clip(go_buffer_50km)

silos = (silos[['cd_geocmu', 'armazenado', 'capacidade','geometry']]
              .rename({
                  'armazenado': 'facility_name',
                  'capacidade': 'facility_capacity',
                  'cd_geocmu': 'municipality_id',
                  'geometry': 'geom'
              }, axis=1)).set_geometry('geom')
silos['facility_type'] = 'silo'

refrigerators = (refrigerators[['razao_soci', 'cd_geocmu', 'geometry']]
 .rename({
     'razao_soci': 'facility_name', 
     'cd_geocmu': 'municipality_id',
     'geometry': 'geom',
 }, axis=1)).set_geometry('geom')
refrigerators['facility_type'] = 'refrigerator'
refrigerators['facility_capacity'] = -1

facilities = pd.concat([silos, refrigerators], axis=0)
facilities

# %%
farms = (Datasets.RURAL_PROPS
         .sjoin(municipalities, how='inner', predicate='covered_by')
         .rename({
            'nome_area': 'farm_name',
            'ibge_code': 'municipality_id',
            'geometry': 'geom'
         }, axis=1)[['farm_name','municipality_id','geom']]
         .set_geometry('geom'))
farms.geom = farms.geom.force_2d()
farms.fillna('Unknown', inplace=True)
farms['farm_type'] = 'SIGEF'

farms.head()

# %%
roads = Datasets.ROADS.clip(go_buffer_50km).rename({
    'sigla': 'road_name',
    'revestimen': 'road_type',
    'geometry': 'geom'
}, axis=1)[['road_name','road_type','geom',]].fillna('Unknown').set_geometry('geom')

roads.sort_values('road_name')


# %%
pg_data_dict = {
    'commodity_group': commodity_groups,
    'commodity': commodities,
    'country': countries,
    'region': regions,
    'municipality': municipalities,
    'commodity_productivity':commodity_productivity,
    'facility': facilities,
    'farm': farms,
    'public_road': roads,
}

# Connection configuration
DB_HOST = os.getenv("PGHOST")
DB_PORT = os.getenv("PGPORT")
DB_NAME = os.getenv("PGDATABASE")
DB_USER = os.getenv("PGUSER")
DB_PASSWORD = os.getenv("PGPASSWORD")
PG_CON_STR = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(PG_CON_STR)

with open('init.sql', 'r') as init_sql:
    INIT_DB_SQL_COMMANDS = init_sql.read()

with engine.connect() as connection:
    connection.begin()
    connection.execute(sql.text(INIT_DB_SQL_COMMANDS))    
    connection.commit()

already_written = {}


# %%
with engine.connect() as connection:
    sql_params = dict(con=connection, if_exists='append', 
                      schema='public', index=False)
    
    for table_name, table_df in pg_data_dict.items():

        if already_written.get(table_name, False):
            continue

        print(f'Writing data to table {table_name}')
        try:
            connection.begin()
            
            if isinstance(table_df, geopandas.GeoDataFrame):
                table_df.to_postgis(name=table_name, **sql_params)
            
            elif isinstance(table_df, pd.DataFrame):    
                table_df.to_sql(name=table_name, **sql_params)

            connection.commit()
            already_written[table_name] = True
        except Exception as e:
            print(e)
            connection.rollback()
            already_written[table_name] = False
