# Pipeline: Silver Comércio Exterior Índices

## Notebooks
Diretório: `notebooks/silver/abs_landingbeca2026jan/comercio_ext_indices/`

- `tb_nomenclatura_brasileira.ipynb`
- `tb_nomenclatura_mercosul.ipynb`
- `tb_referencia_isic_cuci.ipynb`
- `tb_referencia_nbm_ncm.ipynb`
- `tb_referencia_ncm_cgce.ipynb`
- `tb_referencia_ncm_cuci.ipynb`
- `tb_referencia_ncm_isic.ipynb`
- `tb_referencia_ncm_ppe.ipynb`
- `tb_referencia_ncm_ppi.ipynb`
- `tb_referencia_ncm_sh.ipynb`
- `tb_referencia_ncm_unidade.ipynb`

## Objetivo
Construir dimensões e bridges de classificação econômica/produto (NCM/ISIC/CUCI/SH/PPE/PPI/CGCE/NBM).

## Padrão de transformação
1. Leitura de tabela Delta de referência no Bronze (`*_delta`).
2. Normalização (`trim`, `upper`, cast para string).
3. `TS_REF` + `NM_ORIGEM`.
4. `dropDuplicates` por chave natural.

## Estratégia de carga
- Maioria: grava em path Silver somente se não existir (`if (!silverExists)`).
- Exceção: `tb_nomenclatura_brasileira` usa `merge` em `silver_comercio_ext_indices.tb_nomenclatura_brasileira`.

## Qualidade
- validação de chave natural não nula.
- deduplicação por chave.
