# Pipeline: Build Ingestão CNPJ/Raw

## Artefatos
- `build/Cnpj_Into_Raw.ipynb`
- `build/Untitled Notebook 2026-02-03 14:15:12.ipynb`
- `build/Tools.py`

## Objetivo
Ingerir arquivos ZIP de CNPJ, extrair CSVs e gravar Delta em camada raw/bronze com registro de tabela externa.

## Fluxo observado
1. Garante catálogo/schema (`ensure_catalog_schema`).
2. Copia ZIPs para staging em Volume (`dbfs:/Volumes/raw/cnpj/stage`).
3. Extrai ZIP para `/Volumes/...`.
4. Lê CSVs recursivamente e grava Delta com `saveAsTable(fqn_table)`.

## Entradas
- `abfss://raw@storagedatanexus.dfs.core.windows.net/landingbeca2026jan/cnpj/*.zip`

## Saídas
- Paths Delta em `abfss://bronze@storagedatanexus.dfs.core.windows.net/cnpj/<base_no_ext>`
- Tabelas `<raw_catalog>.<raw_schema_cnpj>.<base_no_ext>`

## ⚠️ Atenção
1. `build/Cnpj_Into_Raw.ipynb` depende de `%run /Workspace/Shared/build/Parametros_Ingest` (não versionado).
2. Há notebooks `build/*` com células vazias/placeholders.
3. Não há workflow/job versionado para essa execução.
