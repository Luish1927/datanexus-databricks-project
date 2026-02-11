# Pipeline: Silver Comércio Exterior Estatísticas

## Notebooks
- `.../comercio_ext_estatisticas/tb_exportacoes.ipynb`
- `.../comercio_ext_estatisticas/tb_importacoes.ipynb`
- `.../comercio_ext_estatisticas/tb_exportacoes_municipios.ipynb`
- `.../comercio_ext_estatisticas/tb_importacoes_municipios.ipynb`

## Objetivo
Consolidar séries anuais/mensais de exportação e importação em fatos Silver tipados e deduplicados.

## Entradas
- Pastas Bronze com padrão:
  - `EXP_<YYYY>_delta`
  - `IMP_<YYYY>_delta`
  - `EXP_<YYYY>_MUN_delta`
  - `IMP_<YYYY>_MUN_delta`

## Saídas
- `silver_comercio_ext_estatisticas.tb_exportacoes`
- `silver_comercio_ext_estatisticas.tb_importacoes`
- `silver_comercio_ext_estatisticas.tb_exportacoes_municipios`
- `silver_comercio_ext_estatisticas.tb_importacoes_municipios`

## Transformações
1. União de múltiplos anos (`unionByName`).
2. Normalização de tipos e padronização textual.
3. Regras de domínio:
- `CO_MES between 1 and 12`
- medidas negativas -> `0`
4. Enriquecimento técnico:
- `TS_REF = current_timestamp()`
- `NM_ORIGEM = <pattern de origem>`
5. Deduplicação por chave de negócio.

## Carga
- `tb_exportacoes` e `tb_importacoes`: `merge` (upsert).
- `tb_exportacoes_municipios`: `merge`.
- `tb_importacoes_municipios`: grava apenas quando destino não existe (`if (!silverExists)`).

## Qualidade
- filtros de `isNotNull` para chaves obrigatórias.
- deduplicação explícita por chave composta.
