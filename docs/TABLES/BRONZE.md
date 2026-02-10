# Tabelas Bronze

## Escopo
Camada de ingestão bruta para comércio exterior e (parcialmente) CNPJ.

## Schemas/Databases
- `bronze_cnpj`
  - Location: `abfss://bronze@storagedatanexus.dfs.core.windows.net/autoloader/landingbeca2026jan/cnpj/`
- `bronze_balancacomercial`
  - Location: `abfss://bronze@storagedatanexus.dfs.core.windows.net/autoloader/landingbeca2026jan/balancacomercial/`

Referência: `notebooks/bronze/_ddl_bronze.ipynb`.

## Estratégia de criação de tabelas
`notebooks/bronze/balancacomercial.ipynb` cria tabelas dinamicamente por arquivo CSV via:
```python
.toTable(f"bronze_balancacomercial.{tableName}")
```

### Padrão de nomes
- Nome da tabela = nome do arquivo sem `.csv`.
- Exemplo de famílias de origem usadas depois no Silver:
  - `EXP_<ANO>_delta`
  - `IMP_<ANO>_delta`
  - `EXP_<ANO>_MUN_delta`
  - `IMP_<ANO>_MUN_delta`
  - `PAIS_delta`, `UF_delta`, `VIA_delta`, `NCM_delta`, etc.

## Colunas técnicas adicionadas
- `SOURCE_FILE` (adicionada no notebook Bronze de balança comercial).
- `_rescued` (coluna de dados não parseados pelo Auto Loader, configurada por `rescuedDataColumn`).

## Regras de ingestão
- `cloudFiles.format = csv`
- `cloudFiles.inferColumnTypes = true`
- `cloudFiles.includeExistingFiles = true`
- `mergeSchema = true`
- `badRecordsPath` por tabela
- checkpoints por tabela (`_checkpoint`)

## ⚠️ Atenção
- Não há schema estático versionado para cada tabela Bronze dinâmica.
- Validar schema real com:
```sql
DESCRIBE TABLE bronze_balancacomercial.<tabela>;
```
