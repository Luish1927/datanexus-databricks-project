# Setup (Databricks/Azure)

## Pré-requisitos
- Workspace Databricks com acesso a cluster Spark.
- Storage Account `storagedatanexus` acessível pelo workspace.
- Chave de acesso da Storage Account configurada no cluster Databricks (Spark config).
- Permissões de leitura/escrita nos containers: `raw`, `bronze`, `silver`, `gold`, `metastore`.

## Configuração de acesso
Referência: `config/config.ipynb`.

```python
storage_key = "<azure-storage-key-configurada-no-cluster>"
spark.conf.set("fs.azure.account.key.storagedatanexus.dfs.core.windows.net", storage_key)
```

⚠️ Atenção
- No repositório, os notebooks de configuração ainda usam `dbutils.secrets.get(...)` como exemplo.
- Operacionalmente, considerar a configuração do cluster como fonte de verdade atual.

## Como aplicar no cluster (recomendado no cenário atual)
1. Abrir a configuração do cluster Databricks.
2. Definir Spark config para acesso ADLS:
```text
fs.azure.account.key.storagedatanexus.dfs.core.windows.net=<valor-da-chave-no-ambiente>
```
3. Reiniciar o cluster para aplicar a configuração.
4. Validar em notebook:
```python
spark.conf.get("fs.azure.account.key.storagedatanexus.dfs.core.windows.net")
```

⚠️ Atenção
- Nunca commitar valores reais da chave no repositório.
- Em ambientes com governança mais rígida, migrar para secret scope + Key Vault.

### Otimizações Delta habilitadas
```python
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
```

## Montagem de storage (opcional)
Referência: `config/mount_storage.ipynb`.
- Mount points:
  - `/mnt/raw`
  - `/mnt/bronze`
  - `/mnt/silver`
  - `/mnt/gold`
  - `/mnt/metastore`

Exemplo:
```python
dbutils.fs.mount(
  source="wasbs://silver@storagedatanexus.blob.core.windows.net",
  mount_point="/mnt/silver",
  extra_configs=configs
)
```

## Criação de schemas/tabelas
Ordem recomendada:
1. `notebooks/bronze/_ddl_bronze.ipynb`
2. `notebooks/silver/_ddl_silver.ipynb`
3. `notebooks/gold/_ddl_gold.ipynb`

## Compute recomendado (a validar em ambiente)
⚠️ Atenção
- O repositório não versiona especificação de cluster/job (DBR, node type, autoscaling).
- Validar no workspace Databricks os parâmetros operacionais reais.

Sugestão operacional mínima:
- Runtime com suporte a Delta Lake.
- Autoscaling habilitado para ingestões Auto Loader.
- Permissões de cluster para leitura/escrita nos paths `abfss://` usados nos notebooks.

## Bibliotecas e linguagem
- PySpark: notebooks de configuração e parte do Gold.
- Scala Spark + DeltaTable: maioria dos notebooks Silver e `gold/rst_comercio_exterior.ipynb`.
- SQL em células `%sql` para DDL.

## Segurança
- A chave está sendo aplicada diretamente na configuração do cluster/sessão Spark.
- Não hardcodear connection string/token em notebooks.
- Revisar periodicamente permissões de cluster e política de rotação da chave.

### ⚠️ Segurança
Se surgir qualquer credencial em texto puro no workspace (não observada neste repo), mover para Databricks Secrets + integração com Key Vault.
