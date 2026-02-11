# Pipeline: Gold `rst_comercio_exterior`

## Notebook
- `notebooks/gold/rst_comercio_exterior.ipynb`

## Objetivo
Entregar panorama macro de comércio exterior por período, UF e classificação internacional.

## Entradas
- `tb_exportacoes` (Silver estatísticas)
- `tb_importacoes` (Silver estatísticas)
- `tb_nomenclatura_mercosul` (Silver índices)

## Saída
- `gold.rst_comercio_exterior`

## Transformações
1. Seleção e cast de colunas de exportações/importações.
2. União (`unionByName`).
3. Join com nomenclatura para obter classificação internacional.
4. Agregação (`groupBy` + `sum`) para métricas FOB e peso.

## Carga
- `merge` em `gold.rst_comercio_exterior` por chave de negócio.
