# Silver - Comércio Exterior Estatísticas

Schema: `silver_comercio_ext_estatisticas`

## `silver_comercio_ext_estatisticas.tb_exportacoes`
- Camada: Silver (fato).
- Location (DDL): `abfss://silver@storagedatanexus.dfs.core.windows.net/landingbeca2026jan/comercio_ext_estatisticas/tb_exportacoes`
- Particionamento: `CO_ANO`, `CO_MES`.
- Grão (chave de negócio usada no merge):
  - `CO_ANO`, `CO_MES`, `CO_NCM`, `CO_UNID`, `CO_PAIS`, `SG_UF_NCM`, `CO_VIA`, `CO_URF`
- Colunas:
  - `CO_ANO` INT
  - `CO_MES` INT
  - `CO_NCM` STRING
  - `CO_UNID` STRING
  - `CO_PAIS` STRING
  - `SG_UF_NCM` STRING
  - `CO_VIA` STRING
  - `CO_URF` STRING
  - `QT_ESTAT` DECIMAL(18,2)
  - `KG_LIQUIDO` DECIMAL(18,3)
  - `VL_FOB` DECIMAL(18,2)
  - `TS_REF` TIMESTAMP
  - `NM_ORIGEM` STRING

## `silver_comercio_ext_estatisticas.tb_importacoes`
- Camada: Silver (fato).
- Location: `abfss://silver@storagedatanexus.dfs.core.windows.net/landingbeca2026jan/comercio_ext_estatisticas/tb_importacoes`
- Particionamento: `CO_ANO`, `CO_MES`.
- Grão (merge):
  - `CO_ANO`, `CO_MES`, `CO_NCM`, `CO_UNID`, `CO_PAIS`, `SG_UF_NCM`, `CO_VIA`, `CO_URF`
- Colunas:
  - mesmas de exportações + `VL_FRETE` DECIMAL(18,2), `VL_SEGURO` DECIMAL(18,2)

## `silver_comercio_ext_estatisticas.tb_exportacoes_municipios`
- Camada: Silver (fato).
- Location: `abfss://silver@storagedatanexus.dfs.core.windows.net/landingbeca2026jan/comercio_ext_estatisticas/tb_exportacoes_municipios`
- Particionamento: `CO_ANO`, `CO_MES`.
- Grão (dedup):
  - `CO_ANO`, `CO_MES`, `SH4`, `CO_PAIS`, `SG_UF_MUN`, `CO_MUN`
- Colunas (DDL):
  - `CO_ANO` INT
  - `CO_MES` INT
  - `SH4` STRING
  - `CO_PAIS` STRING
  - `SG_UF_NCM` STRING
  - `CO_MUN` STRING
  - `KG_LIQUIDO` DECIMAL(18,3)
  - `VL_FOB` DECIMAL(18,2)
  - `TS_REF` TIMESTAMP
  - `NM_ORIGEM` STRING

## `silver_comercio_ext_estatisticas.tb_importacoes_municipios`
- Camada: Silver (fato).
- Particionamento (DDL): `CO_ANO`, `CO_MES`.
- Colunas no DDL incluem `CO_NCM`, `CO_UNID`, `CO_VIA`, `CO_URF`, `QT_ESTAT`, `VL_FRETE`, `VL_SEGURO`.

## Regras técnicas aplicadas (notebooks)
- Cast e padronização de tipos.
- `trim/upper` em códigos.
- valores negativos para zero em medidas.
- filtros de obrigatoriedade e `CO_MES between 1 and 12`.
- `dropDuplicates` por chave de negócio.
- carga por `merge` em parte dos notebooks.

## Exemplo de consulta
```sql
SELECT CO_ANO, CO_MES, sum(VL_FOB) AS vl_fob
FROM silver_comercio_ext_estatisticas.tb_exportacoes
GROUP BY CO_ANO, CO_MES
ORDER BY CO_ANO, CO_MES;
```
