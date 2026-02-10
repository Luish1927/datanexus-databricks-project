# Arquitetura

## Visão ponta a ponta
Fluxo observado no repositório:
1. Arquivos de entrada em storage (principalmente `landingbeca2026jan` e containers de origem).
2. Ingestão para Bronze com Auto Loader em Delta.
3. Curadoria Silver por domínio (`comercio_ext_estatisticas`, `comercio_ext_indices`, `comercio_ext_auxiliares`).
4. Publicação Gold para consumo analítico (`rst_*`, `dim_*`).

## Camadas

### Bronze
- Notebooks:
  - `notebooks/bronze/_ddl_bronze.ipynb`
  - `notebooks/bronze/balancacomercial.ipynb`
- Estratégia:
  - `cloudFiles.format = csv`
  - `cloudFiles.schemaLocation`, `badRecordsPath`, `rescuedDataColumn`
  - escrita streaming `toTable("bronze_balancacomercial.<arquivo>")`
- Armazenamento:
  - `abfss://bronze@storagedatanexus.dfs.core.windows.net/autoloader/landingbeca2026jan/balancacomercial/`

### Silver
- DDL central em `notebooks/silver/_ddl_silver.ipynb`.
- Subdomínios:
  - `silver_comercio_ext_estatisticas`
  - `silver_comercio_ext_indices`
  - `silver_comercio_ext_auxiliares`
  - schemas adicionais: `silver_entidades_base`, `silver_entidades_referencias`
- Padrão de transformação:
  - leitura Delta do Bronze
  - cast/normalização (`trim`, `upper`, tipos)
  - validações (`isNotNull`, domínios)
  - deduplicação (`dropDuplicates`)
  - carga via `merge` (parte dos fatos) ou `overwrite` condicional `if (!silverExists)`

### Gold
- DDL em `notebooks/gold/_ddl_gold.ipynb`.
- Tabelas finais:
  - fatos: `gold.rst_comercio_exterior`, `gold.rst_exp_imp_pais`, `gold.rst_base_empresarial`
  - dimensões: `gold.dim_ncm_isic`, `gold.dim_pais`, `gold.dim_calendario`, `gold.dim_cnaes`, `gold.dim_uf`
- Regras principais:
  - agregações por período/chaves analíticas
  - joins com dimensões
  - `OPTIMIZE` e `ZORDER`

## Fontes e destinos

### Fontes principais mapeadas no código
- Comércio exterior (balança comercial):
  - `/mnt/bronze/autoloader/landingbeca2026jan/balancacomercial/*`
- Bases empresariais legadas usadas em Gold:
  - `abfss://silver@storagedatanexus.dfs.core.windows.net/antigo_estabelecimentos`
  - `abfss://silver@storagedatanexus.dfs.core.windows.net/antigo_empresas`
  - `abfss://silver@storagedatanexus.dfs.core.windows.net/antigo_simples`
  - `abfss://silver@storagedatanexus.dfs.core.windows.net/antigo_cnaes`
  - `abfss://silver@storagedatanexus.dfs.core.windows.net/antigo_landingbeca2026jan/...`

### Destinos
- Bronze: schema `bronze_balancacomercial`.
- Silver: schemas `silver_comercio_ext_*`.
- Gold: schema `gold`.

## Decisões técnicas observadas e trade-offs

1. Hive Metastore + schemas lógicos
- Evidência: DDL usando `CREATE SCHEMA`/`CREATE TABLE` sem referência explícita a Unity Catalog.
- Trade-off: simples para ambientes legados; menor governança nativa que UC.

2. Uso misto de `abfss://` e `/mnt/...`
- Evidência: notebooks de DDL e Python usam `abfss://`; vários notebooks Scala usam `/mnt/...`.
- Trade-off: flexibilidade operacional; risco de inconsistência entre caminhos configurados e montagens.

3. Estratégias de carga heterogêneas
- `merge/upsert` em parte dos fatos.
- `overwrite` condicional `if (!silverExists)` em várias dimensões/referências.
- Trade-off: simplicidade de carga inicial; risco de não atualização em execuções futuras para tabelas com `if (!silverExists)`.

4. DDL separado dos notebooks de transformação
- Trade-off: boa separação de responsabilidade; exige disciplina operacional (rodar DDL antes dos jobs).

## ⚠️ Atenção (inconsistências detectadas)
1. `tb_referencia_isic_cuci`:
- notebook grava em `tb_classificacao_isic_cuci`, enquanto DDL define `tb_referencia_isic_cuci`.
- Validar caminho e nome final antes de produção.

2. `tb_referencia_nbm_ncm` vs DDL `tb_referencia_ncm_nbm`:
- nomenclatura invertida entre notebook e DDL.
- Validar tabela oficial consumida a jusante.

3. `tb_importacoes_municipios` (DDL):
- `LOCATION` aponta para pasta de `tb_importacoes` no DDL extraído.
- Validar localização física para evitar sobrescrita indevida.

4. `gold.rst_comercio_exterior`:
- notebook agrega em `dfAgg`, mas `merge` usa `dfJoin`.
- revisar se o alvo deve receber dados agregados ou nível detalhado.

5. notebooks incompletos:
- `notebooks/silver/abs_landingbeca2026jan/entidades_base/tb_empresas.ipynb` vazio.
- `build/*` parcialmente placeholder e com dependências externas de workspace.
