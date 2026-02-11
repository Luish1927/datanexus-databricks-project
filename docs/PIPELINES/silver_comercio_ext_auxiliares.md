# Pipeline: Silver Comércio Exterior Auxiliares

## Notebooks
Diretório: `notebooks/silver/abs_landingbeca2026jan/comercio_ext_auxiliares/`

- `tb_auxiliar_paises.ipynb`
- `tb_auxiliar_vias.ipynb`
- `tb_auxiliar_recintos_alfandegarios.ipynb`
- `tb_auxiliar_unidades_federativas.ipynb`
- `tb_referencia_pais_bloco.ipynb`
- `tb_referencia_uf_mun.ipynb`

## Objetivo
Publicar dimensões auxiliares para enriquecer fatos de comércio exterior (país, via, URF, UF, município, bloco).

## Entradas
- Tabelas Bronze `*_delta` de referência: `PAIS`, `VIA`, `URF`, `UF`, `UF_MUN`, `PAIS_BLOCO`.

## Saídas
- Tabelas no schema `silver_comercio_ext_auxiliares`.

## Regras
- Normalização de códigos/textos.
- filtros de chave não nula.
- deduplicação por chave natural.
- inclusão de `TS_REF`, `NM_ORIGEM` nos notebooks.

## Carga
- padrão `if (!silverExists) overwrite path`.
