# FAQ e Troubleshooting

## 1. Erro de acesso ao Storage (`Permission denied` / `Invalid configuration value`)
- Validar se a chave da Storage Account está configurada no cluster.
- Confirmar `spark.conf.set("fs.azure.account.key....")` carregado na sessão/cluster.

## 2. Notebook Silver não atualiza dados após primeira execução
Causa comum: padrão `if (!silverExists) { ... mode("overwrite") ... }`.

Como resolver:
- Ajustar notebook para permitir overwrite incremental/reprocessamento controlado.
- Ou remover destino de forma controlada antes da carga.

## 3. Merge falha por coluna inexistente
Conferir divergências conhecidas:
- `SG_UF_MUN` vs `SG_UF_NCM` em `tb_exportacoes_municipios`.
- Nomes de tabela/path divergentes em índices (`isic_cuci`, `nbm_ncm`).

## 4. Tabela existe no DDL, mas não é carregada pelo notebook esperado
- Verificar se nome de tabela/path no notebook coincide com `_ddl_silver.ipynb`.
- Executar `DESCRIBE DETAIL <tabela>` para conferir location.

## 5. Gold não bate com Silver
Checklist:
- Conferir período e filtros (`CO_ANO`, `CO_MES`).
- Validar deduplicação no Silver.
- Reexecutar pipeline Gold após refresh da Silver.

## 6. Como validar qualidade rapidamente?
- Contagem por partição (ano/mês).
- Duplicidade por chave de negócio.
- Percentual de nulos em chaves críticas.
- Distribuição de valores negativos (após tratamento devem estar zerados nos fatos tratados).

## 7. Há CI/CD versionado para os notebooks?
Não foi identificado no repositório (sem YAML/JSON de jobs/workflows).

## 8. Posso rodar localmente fora do Databricks?
⚠️ Atenção
- O projeto depende fortemente de `dbutils`, mounts `/mnt`, paths `abfss://`, Delta e contexto Databricks.
- Execução local só é viável com adaptação significativa e credenciais/infra equivalentes.
