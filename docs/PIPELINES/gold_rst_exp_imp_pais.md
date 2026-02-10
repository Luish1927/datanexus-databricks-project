# Pipeline: Gold `rst_exp_imp_pais`

## Notebook
- `notebooks/gold/rst_exp_imp_pais.ipynb`

## Objetivo
Consolidar exportações e importações por país/produto/período, incluindo saldo comercial.

## Entradas
- Silver estatísticas: `tb_exportacoes`, `tb_importacoes`
- Silver dimensões auxiliares/índices: `tb_auxiliar_paises`, `tb_nomenclatura_mercosul`, `tb_referencia_ncm_isic`

## Saída
- `gold.rst_exp_imp_pais`

## Transformações
1. Agrega `VL_FOB` por `CO_ANO/CO_MES/CO_PAIS/CO_NCM` para exportação e importação.
2. Join `full` entre export e import.
3. `coalesce` para preencher ausência de lado export/import.
4. Enriquecimento com ISIC e país.
5. Geração de `ano_mes` e cálculo de `saldo`.

## Carga
- overwrite particionado por `ano_operacao`, `mes_operacao`.
- pós-carga: `OPTIMIZE gold.rst_exp_imp_pais ZORDER BY (cod_pais, cod_isic)`.
