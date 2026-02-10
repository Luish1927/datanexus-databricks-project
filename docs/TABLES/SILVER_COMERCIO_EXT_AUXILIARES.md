# Silver - Comércio Exterior Auxiliares

Schema: `silver_comercio_ext_auxiliares`  
Camada: `silver`  
Storage base: `abfss://silver@storagedatanexus.dfs.core.windows.net/landingbeca2026jan/comercio_ext_auxiliares/`

## Objetivo
Tabelas de referência para enriquecer fatos de comércio exterior (país, UF, município, via de transporte, URF e bloco econômico).

## Padrão técnico dos notebooks
- Fonte: Bronze Delta (`*_delta`) em `/mnt/bronze/autoloader/landingbeca2026jan/balancacomercial/...`.
- Transformações: `trim`, `upper`, cast explícito por coluna.
- DQ: filtro de chave não nula + `dropDuplicates`.
- Colunas técnicas adicionadas em notebooks: `TS_REF`, `NM_ORIGEM`.
- Estratégia de carga recorrente: `if (!silverExists) ... mode("overwrite")`.

## Tabelas

### `silver_comercio_ext_auxiliares.tb_auxiliar_paises`
- Location (DDL): `abfss://silver@storagedatanexus.dfs.core.windows.net/landingbeca2026jan/comercio_ext_auxiliares/tb_auxiliar_paises`
- Chave natural: `CO_PAIS`
- Grão: 1 linha por país
- Colunas (DDL):
  - `CO_PAIS` STRING
  - `CO_PAIS_ISON3` STRING
  - `CO_PAIS_ISOA3` STRING
  - `NO_PAIS` STRING
  - `NO_PAIS_ING` STRING
  - `NO_PAIS_ESP` STRING
- Notebook: adiciona `TS_REF`, `NM_ORIGEM`.

### `silver_comercio_ext_auxiliares.tb_auxiliar_unidades_federativas`
- Location (DDL): `abfss://silver@storagedatanexus.dfs.core.windows.net/landingbeca2026jan/comercio_ext_auxiliares/tb_auxiliar_unidades_federativas`
- Chave natural: `CO_UF`
- Grão: 1 linha por UF
- Colunas (DDL):
  - `CO_UF` STRING
  - `SG_UF` STRING
  - `NO_UF` STRING
  - `NO_REGIAO` STRING
- Notebook: adiciona `TS_REF`, `NM_ORIGEM`.

### `silver_comercio_ext_auxiliares.tb_auxiliar_vias`
- Location (DDL): `abfss://silver@storagedatanexus.dfs.core.windows.net/landingbeca2026jan/comercio_ext_auxiliares/tb_auxiliar_vias`
- Chave natural: `CO_VIA`
- Grão: 1 linha por via de transporte
- Colunas (DDL):
  - `CO_VIA` STRING
  - `NO_VIA` STRING
- Notebook: adiciona `TS_REF`, `NM_ORIGEM`.

### `silver_comercio_ext_auxiliares.tb_auxiliar_recintos_alfandegarios`
- Location (DDL): `abfss://silver@storagedatanexus.dfs.core.windows.net/landingbeca2026jan/comercio_ext_auxiliares/tb_auxiliar_recintos_alfandegarios`
- Chave natural: `CO_URF`
- Grão: 1 linha por URF
- Colunas (DDL):
  - `CO_URF` STRING
  - `NO_URF` STRING
- Notebook: adiciona `TS_REF`, `NM_ORIGEM`.

### `silver_comercio_ext_auxiliares.tb_referencia_pais_bloco`
- Location (DDL): `abfss://silver@storagedatanexus.dfs.core.windows.net/landingbeca2026jan/comercio_ext_auxiliares/tb_referencia_pais_bloco`
- Chave natural composta: `CO_PAIS`, `CO_BLOCO`
- Grão: relação país-bloco econômico
- Colunas (DDL):
  - `CO_PAIS` STRING
  - `CO_BLOCO` STRING
  - `NO_BLOCO` STRING
  - `NO_BLOCO_ING` STRING
  - `NO_BLOCO_ESP` STRING
- Notebook: adiciona `TS_REF`, `NM_ORIGEM`.

### `silver_comercio_ext_auxiliares.tb_referencia_uf_mun`
- Location (DDL): `abfss://silver@storagedatanexus.dfs.core.windows.net/landingbeca2026jan/comercio_ext_auxiliares/tb_referencia_uf_mun`
- Chave natural: `CO_MUN_GEO`
- Grão: 1 linha por município geográfico
- Colunas (DDL):
  - `CO_MUN_GEO` STRING
  - `NO_MUN` STRING
  - `NO_MUN_MIN` STRING
  - `SG_UF` STRING
- Notebook: adiciona `TS_REF`, `NM_ORIGEM`.

## Regras de qualidade relevantes
- Códigos normalizados em caixa alta (`upper`) e sem espaços marginais (`trim`).
- Registros com chave nula são descartados.
- `dropDuplicates` por chave natural de cada tabela.

## Queries de validação

### Unicidade de chave (`tb_auxiliar_paises`)
```sql
SELECT CO_PAIS, count(*) c
FROM silver_comercio_ext_auxiliares.tb_auxiliar_paises
GROUP BY CO_PAIS
HAVING c > 1;
```

### Cobertura de municípios por UF
```sql
SELECT SG_UF, count(*) qtd_municipios
FROM silver_comercio_ext_auxiliares.tb_referencia_uf_mun
GROUP BY SG_UF
ORDER BY qtd_municipios DESC;
```

### Relação país x bloco
```sql
SELECT CO_PAIS, count(*) qtd_blocos
FROM silver_comercio_ext_auxiliares.tb_referencia_pais_bloco
GROUP BY CO_PAIS
ORDER BY qtd_blocos DESC;
```

## ⚠️ Atenção
1. Divergência DDL vs notebook:
- O DDL de auxiliares não traz `TS_REF` e `NM_ORIGEM` na maioria das tabelas.
- Os notebooks adicionam essas colunas técnicas.

2. Incrementalidade:
- Várias cargas usam `if (!silverExists)`, então mudanças futuras na origem podem não atualizar automaticamente a tabela Silver.
- Para reprocessamento, revisar estratégia de overwrite/merge.
