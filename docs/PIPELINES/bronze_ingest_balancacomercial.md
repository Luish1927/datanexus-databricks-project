# Pipeline: Bronze Ingestão Balança Comercial

## Notebook
- `notebooks/bronze/balancacomercial.ipynb`

## Objetivo
Ingerir arquivos CSV do container de origem para tabelas Delta no schema `bronze_balancacomercial` usando Auto Loader.

## Entrada
- `RAW_BASE = abfss://balancacomercial@landingbeca2026jan.dfs.core.windows.net/`
- Arquivos CSV listados via `dbutils.fs.ls(RAW_BASE)`.

## Saída
- Tabelas Delta: `bronze_balancacomercial.<arquivo_sem_csv>`
- Base física: `abfss://bronze@storagedatanexus.dfs.core.windows.net/autoloader/landingbeca2026jan/balancacomercial/`

## Etapas
1. Lista arquivos fonte.
2. Para cada arquivo:
- configura schema/checkpoint/bad records.
- lê com `spark.readStream.format("cloudFiles")`.
- adiciona `SOURCE_FILE`.
- escreve com `toTable(...)` em modo append + `availableNow=True`.

## Regras de qualidade
- `badRecordsPath` por tabela.
- `_rescued` para colunas inesperadas.
- contagem final por tabela (`dfBronze.count()`).

## Incrementalidade
- Sim, via Auto Loader com checkpoint e processamento de arquivos novos.
