# Tabelas Gold

Schema: `gold`

## `gold.rst_comercio_exterior`
- Camada: Gold (fato).
- Location: `/mnt/gold/rst_comercio_exterior`
- Particionamento: `an_operacao`, `me_operacao`.
- Colunas:
  - `an_operacao` INT
  - `me_operacao` INT
  - `sg_unidade_federativa` STRING
  - `cd_classificacao_internacional` STRING
  - `tp_operacao` STRING
  - `vl_free_on_board` FLOAT
  - `qt_peso_liquido_kg` DECIMAL(20,3)

## `gold.rst_exp_imp_pais`
- Camada: Gold (fato).
- Location: `abfss://gold@storagedatanexus.dfs.core.windows.net/rst_exp_imp_pais`
- Particionamento: `ano_operacao`, `mes_operacao`.
- Grão: mês + país + NCM + ISIC.
- Colunas:
  - `ano_operacao`, `mes_operacao`, `ano_mes`
  - `cod_pais`, `cod_ncm`, `cod_isic`, `cod_div_isic`
  - `total_exportado`, `total_importado`, `saldo`

## `gold.rst_base_empresarial`
- Camada: Gold (fato agregado).
- Location: `abfss://gold@storagedatanexus.dfs.core.windows.net/rst_base_empresarial`
- Grão: `sg_unidade_federativa`, `cod_cnae`.
- Métricas: `empresas_ativas`, `empresas_matriz`, `capital_social_total`, `qtd_mei`, `qtd_simples`.

## `gold.dim_ncm_isic`
- Camada: Gold (dimensão).
- Location: `abfss://gold@storagedatanexus.dfs.core.windows.net/dim_ncm_isic`
- Colunas:
  - `cod_ncm`, `cod_isic`, `cod_div_isic`, `nome_produto`, `div_isic`, `setor_produto`

## `gold.dim_pais`
- Camada: Gold (dimensão).
- Location: `abfss://gold@storagedatanexus.dfs.core.windows.net/dim_pais`
- Colunas: `cod_pais`, `pais`, `bloco_economico`

## `gold.dim_calendario`
- Camada: Gold (dimensão).
- Location: `abfss://gold@storagedatanexus.dfs.core.windows.net/dim_calendario`
- Colunas: `ano`, `mes`, `ano_mes`

## `gold.dim_cnaes`
- Camada: Gold (dimensão).
- Location: `abfss://gold@storagedatanexus.dfs.core.windows.net/dim_cnaes`
- Colunas: `cod_cnae`, `descricao`

## `gold.dim_uf`
- Camada: Gold (dimensão).
- Criada em `notebooks/gold/dim_tables.ipynb`.
- Colunas observadas: `cod_uf`, `sigla_uf`, `nome_uf`, `regiao`.

## Exemplo de consulta
```sql
SELECT ano_operacao, mes_operacao, cod_pais, sum(saldo) AS saldo
FROM gold.rst_exp_imp_pais
GROUP BY ano_operacao, mes_operacao, cod_pais
ORDER BY ano_operacao, mes_operacao, cod_pais;
```
