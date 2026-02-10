# Pipeline: Gold `rst_base_empresarial`

## Notebook
- `notebooks/gold/rst_base_empresarial.ipynb`

## Objetivo
Construir fato agregado de base empresarial por UF e CNAE.

## Entradas
- Silver legado: `antigo_estabelecimentos`, `antigo_empresas`, `antigo_simples`
- Gold dimensões: `gold.dim_uf`, `gold.dim_cnaes`

## Saída
- `gold.rst_base_empresarial`

## Regras de transformação
1. Filtra empresas ativas (`st_cadastral == '02'`).
2. Join por `cnpj` com empresa e simples.
3. Join com dimensões de UF e CNAE (broadcast).
4. Agrega métricas:
- `empresas_ativas`
- `empresas_matriz`
- `capital_social_total`
- `qtd_mei`
- `qtd_simples`

## Carga
- `saveAsTable(target_table)` com overwrite e `mergeSchema=true`.
- `OPTIMIZE ... ZORDER BY (cod_cnae)`.

## ⚠️ Atenção
- O DDL de `gold.rst_base_empresarial` e o conjunto de colunas efetivamente gravadas no notebook não estão 100% alinhados (ex.: `porte_empresa`, `qtd_mei`, `qtd_simples`).
