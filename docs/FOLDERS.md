# Estrutura de Pastas

## Raiz
- `README.md`: documentação principal.
- `docs/`: documentação técnica detalhada.
- `build/`: notebooks utilitários/experimentais de ingestão e DDL auxiliar.
- `config/`: configuração de acesso ao storage e mounts.
- `notebooks/`: pipelines por camada (`bronze`, `silver`, `gold`).
- `tools/`: utilitários de parâmetros e funções (inclui Scala para unzip/cópia).

## `notebooks/bronze`
- `_ddl_bronze.ipynb`: criação de databases Bronze.
- `balancacomercial.ipynb`: ingestão Auto Loader de CSV para Delta tabelado.

## `notebooks/silver`
- `_ddl_silver.ipynb`: criação de schemas/tabelas Silver (estatísticas, índices, auxiliares).
- `testes.ipynb`: leituras exploratórias e validação manual.
- `abs_landingbeca2026jan/comercio_ext_estatisticas/`: fatos de exportação/importação.
- `abs_landingbeca2026jan/comercio_ext_indices/`: dimensões e bridges de classificação.
- `abs_landingbeca2026jan/comercio_ext_auxiliares/`: dimensões auxiliares (país, UF, via, URF, etc.).
- `abs_landingbeca2026jan/entidades_base/`: entidade empresarial (parcial/incompleta).

## `notebooks/gold`
- `_ddl_gold.ipynb`: criação de tabelas Gold.
- `dim_tables.ipynb`: construção de dimensões Gold.
- `rst_exp_imp_pais.ipynb`: fato consolidado por país/produto.
- `rst_comercio_exterior.ipynb`: fato macro de comércio exterior.
- `rst_base_empresarial.ipynb`: fato agregado empresarial por UF/CNAE.

## `config`
- `config.ipynb`: configura paths e `spark.conf` de acesso ao storage.
- `mount_storage.ipynb`: monta containers em `/mnt/*`.

## `build`
- `Tools.py`: parâmetros e helpers de ingestão.
- `Cnpj_Into_Raw.ipynb`, `Balancacomercial_Into_Raw.ipynb`: notebooks de ingestão em estado parcial.
- `Databases.ipynb`, `Schemas.ipynb`: comandos SQL auxiliares.
- `Untitled Notebook ...ipynb`: rotina ZIP->Volume->Delta para CNPJ.

## `tools`
- `storage_parameters.ipynb`: parâmetros e helpers de path ABFSS.
- `funcoes_scala.ipynb`: funções Scala para unzip e operações em filesystem.
