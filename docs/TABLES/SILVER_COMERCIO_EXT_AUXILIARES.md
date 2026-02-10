# Silver - Comércio Exterior Auxiliares

Schema: `silver_comercio_ext_auxiliares`

## `tb_auxiliar_paises`
- Location: `.../comercio_ext_auxiliares/tb_auxiliar_paises`
- Chave natural: `CO_PAIS`
- Colunas:
  - `CO_PAIS`, `CO_PAIS_ISON3`, `CO_PAIS_ISOA3`, `NO_PAIS`, `NO_PAIS_ING`, `NO_PAIS_ESP`

## `tb_auxiliar_unidades_federativas`
- Chave natural: `CO_UF`
- Colunas: `CO_UF`, `SG_UF`, `NO_UF`, `NO_REGIAO`

## `tb_auxiliar_vias`
- Chave natural: `CO_VIA`
- Colunas: `CO_VIA`, `NO_VIA`

## `tb_auxiliar_recintos_alfandegarios`
- Chave natural: `CO_URF`
- Colunas: `CO_URF`, `NO_URF`

## `tb_referencia_pais_bloco`
- Chave natural composta: `CO_PAIS`, `CO_BLOCO`
- Colunas: `CO_PAIS`, `CO_BLOCO`, `NO_BLOCO`, `NO_BLOCO_ING`, `NO_BLOCO_ESP`

## `tb_referencia_uf_mun`
- Chave natural: `CO_MUN_GEO`
- Colunas: `CO_MUN_GEO`, `NO_MUN`, `NO_MUN_MIN`, `SG_UF`

## Regras comuns
- Normalização e padronização textual (`trim/upper`).
- `dropDuplicates` por chave natural.
- Inclusão de `TS_REF` e `NM_ORIGEM` no notebook (algumas não estão no DDL).
- carga com `if (!silverExists) overwrite` em path.

## Exemplo de consulta
```sql
SELECT CO_PAIS, NO_PAIS, CO_PAIS_ISOA3
FROM silver_comercio_ext_auxiliares.tb_auxiliar_paises
LIMIT 20;
```

## ⚠️ Atenção
- DDL de auxiliares não inclui `TS_REF` e `NM_ORIGEM` em várias tabelas, mas notebooks adicionam essas colunas.
- Validar schema efetivo em ambiente (`DESCRIBE TABLE`).
