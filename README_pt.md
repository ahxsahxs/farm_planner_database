# Farm Planner Database

Este projeto contém recursos para implantar um banco de dados espacial PostgreSQL projetado para modelar a produtividade agrícola. Desenvolvido para análise de produtividade em Goiás, Brasil, este banco de dados aborda os desafios de unificar dados agrícolas de diversas fontes oficiais.

## Índice

* Motivação e Objetivos
* Características
* Implementação
* Interagindo com o Banco de Dados
* Trabalhos Relacionados

## Motivação e Objetivos

A principal motivação para este projeto é facilitar a análise de dados de produtividade agrícola para Goiás, Brasil. A falta de uma fonte de dados unificada cobrindo informações de produtividade na região levou ao desenvolvimento deste banco de dados, que integra dados oficiais de fontes como a Pesquisa Agropecuária Municipal do IBGE e o banco de dados de propriedades rurais do SIGEF.

O esquema do banco de dados espelha os esquemas originais das fontes de dados, com algumas tabelas e colunas correspondendo diretamente às publicações oficiais, enquanto outras foram personalizadas para suportar modelagem relacional e análise espacial.

Com PostGIS habilitado para o gerenciamento de dados georreferenciados, este projeto visa suportar processos ETL eficientes e significativos para análise de dados espaciais na agricultura.

## Características

* PostgreSQL com PostGIS: Oferece suporte robusto para dados geoespaciais.
* Serviço de Carregamento de Dados: Um serviço Docker para carregar dados a partir de scripts e inicializar o esquema.
* Esquema Amigável para ETL: Modelado para integração e análise espacial de dados de produtividade agrícola.

## Implementação

O arquivo [docker-compose.yaml](docker-compose.yaml) define dois Docker services:

* `postgis`: Uma instância PostgreSQL com PostGIS, onde o banco de dados espacial reside.
* `data_loader`: Uma instância Linux que inicializa o banco de dados com esquema e dados.

O serviço `data_loader` usa scripts no diretório [data-loader/](data-loader/):

* Um script SQL para inicializar o esquema.
* Um script Python para carregar entidades discretas.
* Um script shell para ingestão de dados raster.
* Um script shell para gerenciar o processo de carregamento de dados.

*Nota*: Devido às limitações de tamanho de arquivo do GitHub, os dados reais não estão incluídos neste repositório. Se precisar de acesso aos dados, entre em contato conosco.

### Volumes

Os containers Docker utilizam os seguintes volumes:

* [pgdata/](pgdata/): Montado pelo `postgis` para armazenar os arquivos do banco de dados.
* [data/](data/): Montado pelo `data_loader` para acessar os scripts de ingestão e os dados brutos.

### Rodando locamente

Para rodar os serviços localmente:

* Copie os dados brutos para os diretórios [data](data).
* Execute o seguinte comando:

```shell
docker compose up -d
```

Este comando iniciará os serviços e executará o processo de ingestão de dados.


## Interagindo com o Banco de Dados

O serviço `postgis` expõe o banco de dados na porta `5432`. Você pode encontrar os detalhes de conexão (como nome de usuário e senha) em [docker-compose.yaml](docker-compose.yaml).

Para consultas e visualizações de exemplo, consulte o notebook [data_exploration.ipynb](data_exploration.ipynb), que fornece insights sobre como interagir com o banco de dados.

## Exemplos de inserção de dados

Exemplos de inserção de dados podem ser encontrados nos seguintes arquivos:

** ingest_rasters.sh
** ingest_polygons.py

## Trabalhos Relacionados

Trabalhos de pesquisa estão planejados usando este banco de dados. Publicações relevantes serão adicionadas aqui ao longo do tempo.

* [Modelagem de Dados de Produtividade Agrícola em Goiás](related_work/modelagem_dados_goias.pdf)