# DataNexus Databricks Project

Este projeto implementa um lakehouse em Databricks para dados de comércio exterior (Comex/MDIC) e base empresarial, com camadas Bronze, Silver e Gold.

- Ingestão automática de arquivos CSV/ZIP para Delta no Bronze.
- Curadoria e padronização de tabelas de referência, estatísticas e índices no Silver.
- Entrega de tabelas analíticas Gold para consumo em BI (incluindo agregações por país, UF, ISIC e CNAE).
- Organização por notebooks Databricks (PySpark/SQL) com DDL separado por camada.
- Suporte a otimizações Delta (`OPTIMIZE`, `ZORDER`, particionamento por período).

## Sumário
- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Como Rodar](#como-rodar)
- [Configuração de Acesso/Secrets](#configuração-de-acessosecrets)
- [Pipelines](#pipelines)
- [Modelo de Dados](#modelo-de-dados)
- [Tabelas](#tabelas-com-links)
- [Observabilidade e Qualidade](#observabilidade-e-qualidade)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)

## Visão Geral
Contexto observado no código:
- Fontes principais: arquivos de balança comercial e referências (`/mnt/bronze/autoloader/landingbeca2026jan/balancacomercial/...`) e bases empresariais legadas (`antigo_*`).
- Camadas:
  - Bronze: ingestão com Auto Loader para Delta.
  - Silver: normalização, tipagem, deduplicação e enriquecimentos básicos.
  - Gold: fatos e dimensões para análise (comércio exterior e base empresarial).

Referências detalhadas:
- Arquitetura: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Modelo de dados: [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md)
- Índice geral: [`docs/INDEX.md`](docs/INDEX.md)

## Arquitetura
Resumo:
1. Arquivos chegam em `raw/landingbeca2026jan` e/ou containers de origem.
2. Ingestão Bronze com Auto Loader (`cloudFiles`) para tabelas Delta.
3. Notebooks Silver aplicam casts, validações, tratamento de negativos, deduplicação e carga (merge/overwrite condicional).
4. Notebooks Gold agregam e relacionam dimensões/fatos para consumo analítico.

Fluxo completo e trade-offs: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Estrutura de Pastas
Mapa completo e propósito de cada diretório: [`docs/FOLDERS.md`](docs/FOLDERS.md).

## Como Rodar
### Quickstart
Exemplo de sequência real baseada no repositório (Databricks):

```sql
-- 1) Criar schemas/tabelas base
-- executar notebooks:
-- notebooks/bronze/_ddl_bronze.ipynb
-- notebooks/silver/_ddl_silver.ipynb
-- notebooks/gold/_ddl_gold.ipynb
```

```python
# 2) Configurar acesso ao storage e otimizações
# notebook: config/config.ipynb
storage_key = dbutils.secrets.get(scope="kv-datanexus", key="storagedatanexus")
spark.conf.set("fs.azure.account.key.storagedatanexus.dfs.core.windows.net", storage_key)
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
```

```python
# 3) Ingestão Bronze (exemplo)
# notebook: notebooks/bronze/balancacomercial.ipynb
query = (
  spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.includeExistingFiles", "true")
    .toTable("bronze_balancacomercial.<tabela>")
)
```

```scala
// 4) Curadoria Silver (exemplo)
// notebook: notebooks/silver/abs_landingbeca2026jan/comercio_ext_estatisticas/tb_exportacoes.ipynb
val deltaTarget = DeltaTable.forName("silver_comercio_ext_estatisticas.tb_exportacoes")
// merge/upsert por chave de negócio
```

```python
# 5) Publicação Gold (exemplo)
# notebook: notebooks/gold/rst_exp_imp_pais.ipynb
rst_exp_imp_pais.write.format("delta").mode("overwrite") \
  .partitionBy("ano_operacao", "mes_operacao") \
  .saveAsTable("gold.rst_exp_imp_pais")
```

Instruções operacionais completas: [`docs/RUNBOOK.md`](docs/RUNBOOK.md).

## Configuração de Acesso/Secrets
- Secrets via Databricks Secret Scope (`kv-datanexus`) em `config/config.ipynb` e `config/mount_storage.ipynb`.
- Não há segredos em texto puro no repositório.
- Detalhes: [`docs/SETUP.md`](docs/SETUP.md).

## Pipelines
Documentação por pipeline/job:
- [`docs/PIPELINES/bronze_ingest_balancacomercial.md`](docs/PIPELINES/bronze_ingest_balancacomercial.md)
- [`docs/PIPELINES/build_ingest_cnpj_raw.md`](docs/PIPELINES/build_ingest_cnpj_raw.md)
- [`docs/PIPELINES/silver_comercio_ext_estatisticas.md`](docs/PIPELINES/silver_comercio_ext_estatisticas.md)
- [`docs/PIPELINES/silver_comercio_ext_indices.md`](docs/PIPELINES/silver_comercio_ext_indices.md)
- [`docs/PIPELINES/silver_comercio_ext_auxiliares.md`](docs/PIPELINES/silver_comercio_ext_auxiliares.md)
- [`docs/PIPELINES/silver_entidades_base.md`](docs/PIPELINES/silver_entidades_base.md)
- [`docs/PIPELINES/gold_dim_tables.md`](docs/PIPELINES/gold_dim_tables.md)
- [`docs/PIPELINES/gold_rst_comercio_exterior.md`](docs/PIPELINES/gold_rst_comercio_exterior.md)
- [`docs/PIPELINES/gold_rst_exp_imp_pais.md`](docs/PIPELINES/gold_rst_exp_imp_pais.md)
- [`docs/PIPELINES/gold_rst_base_empresarial.md`](docs/PIPELINES/gold_rst_base_empresarial.md)

## Modelo de Dados
- Relações fato/dimensão, grão e cardinalidade: [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md).

## Tabelas com links
- Visão por camada:
  - [`docs/TABLES/BRONZE.md`](docs/TABLES/BRONZE.md)
  - [`docs/TABLES/SILVER_COMERCIO_EXT_ESTATISTICAS.md`](docs/TABLES/SILVER_COMERCIO_EXT_ESTATISTICAS.md)
  - [`docs/TABLES/SILVER_COMERCIO_EXT_INDICES.md`](docs/TABLES/SILVER_COMERCIO_EXT_INDICES.md)
  - [`docs/TABLES/SILVER_COMERCIO_EXT_AUXILIARES.md`](docs/TABLES/SILVER_COMERCIO_EXT_AUXILIARES.md)
  - [`docs/TABLES/GOLD.md`](docs/TABLES/GOLD.md)

## Detalhamento por Pasta
- Mapa de diretórios: [`docs/FOLDERS.md`](docs/FOLDERS.md)
- Índice de documentos por tema: [`docs/INDEX.md`](docs/INDEX.md)

## Tabelas e Colunas
- Consulte o modelo consolidado: [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md)
- Consulte os schemas detalhados por camada: [`docs/TABLES`](docs/TABLES)

## Decisões de Arquitetura e Trade-offs
Baseado no código atual:
- Hive Metastore com schemas explícitos (ex.: `silver_comercio_ext_estatisticas`) ao invés de Unity Catalog explícito.
- Mistura de acesso por `abfss://` e `/mnt/...`.
- Estratégias de carga heterogêneas (merge vs create-if-not-exists), com impacto em incrementalidade.
- DDL e notebooks de transformação separados por camada.

Discussão completa: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Observabilidade e Qualidade
Práticas implementadas no código:
- `dropDuplicates` por chaves de negócio.
- filtros de obrigatoriedade (`isNotNull`) e domínio (`CO_MES between 1 and 12`).
- tratamento de métricas negativas para zero em fatos de comércio exterior.
- otimizações Delta (`OPTIMIZE`, `ZORDER`, auto optimize/compact).

Guia de validação: [`docs/RUNBOOK.md`](docs/RUNBOOK.md) e [`docs/FAQ.md`](docs/FAQ.md).

## Troubleshooting
Erros e correções frequentes: [`docs/FAQ.md`](docs/FAQ.md).

## Roadmap
Sugestões de evolução com base no estado atual:
1. Versionar jobs/workflows Databricks (não há JSON/YAML de jobs no repositório).
2. Padronizar estratégia de carga incremental no Silver.
3. Corrigir divergências entre nomes de colunas/tabelas entre DDL e notebooks.
4. Cobrir entidades base (`tb_empresas`) com implementação completa.

## Inventário Inicial do Repositório
Categorias encontradas:
- Notebooks Bronze: `notebooks/bronze/*`
- Notebooks Silver: `notebooks/silver/*` (subpastas `comercio_ext_*` e `entidades_base`)
- Notebooks Gold: `notebooks/gold/*`
- Configuração: `config/*`
- Utilitários: `tools/*`, `build/Tools.py`
- Build/ingest auxiliares: `build/*`

Observação: não foram encontrados arquivos de CI/CD, jobs Databricks exportados (`*.json`), SQL avulso (`*.sql`), ou infra declarativa (`*.yml`, `*.tf`).
