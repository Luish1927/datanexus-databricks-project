# Silver - Comércio Exterior Índices

Schema: `silver_comercio_ext_indices`

## Tabelas principais

### `tb_nomenclatura_mercosul`
- Camada: Silver (dimensão produto/hub).
- Chave natural: `CO_NCM`.
- Location (DDL): `.../comercio_ext_indices/tb_nomenclatura_mercosul`
- Colunas chave:
  - `CO_NCM`, `CO_UNID`, `CO_SH6`, `CO_PPE`, `CO_PPI`, `CO_CUCI_ITEM`, `CO_CGCE_N3`, `CO_ISIC_CLASSE`, `TS_REF`, `NM_ORIGEM`.

### `tb_referencia_ncm_isic`
- Tipo: dimensão hierárquica ISIC.
- Chave natural: `CO_ISIC_CLASSE`.
- Colunas: classe/grupo/divisão/seção em PT/EN/ES.

### `tb_referencia_ncm_cuci`
- Tipo: dimensão hierárquica CUCI.
- Chave natural: `CO_CUCI_ITEM`.

### `tb_referencia_ncm_sh`
- Tipo: dimensão hierárquica SH (2/4/6 dígitos + seção).
- Chave natural: `CO_SH6`.

### `tb_referencia_ncm_ppe`
- Chave natural: `CO_PPE`.

### `tb_referencia_ncm_ppi`
- Chave natural: `CO_PPI`.

### `tb_referencia_ncm_cgce`
- Chave natural: `CO_CGCE_N3`.

### `tb_referencia_ncm_unidade`
- Chave natural: `CO_UNID`.

### `tb_nomenclatura_brasileira`
- Tipo: legado NBM.
- Chave natural: `CO_NBM`.
- Carga com `merge` no notebook.

### `tb_referencia_isic_cuci`
- Tipo: bridge ISIC seção x CUCI grupo.
- Chave natural composta: `CO_ISIC_SECAO`, `CO_CUCI_GRUPO`.

### `tb_referencia_ncm_nbm` (DDL) / `tb_referencia_nbm_ncm` (notebook)
- Tipo: bridge NBM <-> NCM.
- Chave natural composta: `CO_NBM`, `CO_NCM`.

## Regras comuns nos notebooks
- Leitura Delta do Bronze (`*_delta`).
- cast para `StringType` com `trim(upper(...))` em códigos.
- inclusão de `TS_REF` e `NM_ORIGEM`.
- `dropDuplicates` por chave natural.
- carga majoritariamente `if (!silverExists) overwrite`.

## Exemplo de consulta
```sql
SELECT CO_NCM, CO_ISIC_CLASSE
FROM silver_comercio_ext_indices.tb_nomenclatura_mercosul
LIMIT 20;
```

## ⚠️ Atenção
1. Divergência de nome/path em `isic_cuci`:
- DDL: `tb_referencia_isic_cuci`.
- notebook: `tb_classificacao_isic_cuci`.

2. Divergência de nome em bridge NBM/NCM:
- DDL: `tb_referencia_ncm_nbm`.
- notebook: `tb_referencia_nbm_ncm`.

3. Estratégia `if (!silverExists)` pode impedir atualização incremental.
