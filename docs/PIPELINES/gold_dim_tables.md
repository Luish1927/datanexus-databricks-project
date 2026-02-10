# Pipeline: Gold Dimensões (`dim_tables`)

## Notebook
- `notebooks/gold/dim_tables.ipynb`

## Objetivo
Construir dimensões analíticas Gold: país, NCM-ISIC, calendário, CNAE e UF.

## Entradas
- Silver legado (`antigo_landingbeca2026jan/...`) e `antigo_cnaes`.

## Saídas
- `gold.dim_pais`
- `gold.dim_ncm_isic`
- `gold.dim_calendario`
- `gold.dim_cnaes`
- `gold.dim_uf`

## Transformações-chave
- `dropDuplicates` em dimensões fonte.
- `split`/`trim` de descrição de produto em NCM.
- join país + bloco econômico.
- construção de calendário por `sequence(2020, 2030)` x meses.

## Carga
- `saveAsTable(...).mode("overwrite")` para cada dimensão.
