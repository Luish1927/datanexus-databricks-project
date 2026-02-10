# Runbook de Operação

## Ordem de execução recomendada
1. Configuração
- `config/config.ipynb`
- opcional: `config/mount_storage.ipynb`

2. DDL
- `notebooks/bronze/_ddl_bronze.ipynb`
- `notebooks/silver/_ddl_silver.ipynb`
- `notebooks/gold/_ddl_gold.ipynb`

3. Ingestão Bronze
- `notebooks/bronze/balancacomercial.ipynb`

4. Silver
- `notebooks/silver/abs_landingbeca2026jan/comercio_ext_auxiliares/*`
- `notebooks/silver/abs_landingbeca2026jan/comercio_ext_indices/*`
- `notebooks/silver/abs_landingbeca2026jan/comercio_ext_estatisticas/*`

5. Gold
- `notebooks/gold/dim_tables.ipynb`
- `notebooks/gold/rst_exp_imp_pais.ipynb`
- `notebooks/gold/rst_comercio_exterior.ipynb`
- `notebooks/gold/rst_base_empresarial.ipynb`

## Checklist pré-execução
- Secret scope `kv-datanexus` acessível.
- Paths `abfss://...` e/ou mounts `/mnt/...` disponíveis.
- Schemas/tabelas DDL já criados.
- Presença de arquivos novos no Bronze source.

## Estratégia de reprocessamento

### Bronze
- Reprocessar por arquivo/prefixo em `balancacomercial.ipynb`.
- Validar checkpoints `_checkpoint` e `_schema` por tabela.

### Silver
- Tabelas com `merge`: reprocessamento tende a ser idempotente por chave de negócio.
- Tabelas com `if (!silverExists)`: não atualizam após primeira carga.

⚠️ Atenção
- Para tabelas com `if (!silverExists)`, backfill exige ajuste do notebook (ou limpeza controlada da pasta/tabela).

### Gold
- Jobs usam `overwrite` em parte dos casos, com particionamento em fatos temporais.
- Reprocessamento completo é viável quando os dados Silver estiverem íntegros.

## Backfill
1. Determinar intervalo (ano/mês) e fontes impactadas.
2. Reingestar Bronze (se necessário).
3. Reexecutar Silver correspondente.
4. Reexecutar Gold dependente.
5. Validar contagens e consistência.

## Recuperação de falhas
- Falha de acesso storage/secret:
  - validar `dbutils.secrets.get` e ACL do scope.
- Falha de schema/cast:
  - comparar schema esperado no notebook com schema real do Delta source.
- Falha de merge:
  - conferir chaves de negócio e nomes de colunas em `merge condition`.

## Validadores de qualidade (exemplos)

### Contagem
```sql
SELECT CO_ANO, CO_MES, count(*)
FROM silver_comercio_ext_estatisticas.tb_exportacoes
GROUP BY CO_ANO, CO_MES
ORDER BY CO_ANO, CO_MES;
```

### Duplicidade por chave
```sql
SELECT CO_ANO, CO_MES, CO_NCM, CO_UNID, CO_PAIS, SG_UF_NCM, CO_VIA, CO_URF, count(*) c
FROM silver_comercio_ext_estatisticas.tb_importacoes
GROUP BY CO_ANO, CO_MES, CO_NCM, CO_UNID, CO_PAIS, SG_UF_NCM, CO_VIA, CO_URF
HAVING c > 1;
```

### Nulos críticos
```sql
SELECT
  sum(CASE WHEN CO_ANO IS NULL THEN 1 ELSE 0 END) AS n_ano_null,
  sum(CASE WHEN CO_MES IS NULL THEN 1 ELSE 0 END) AS n_mes_null,
  sum(CASE WHEN CO_NCM IS NULL THEN 1 ELSE 0 END) AS n_ncm_null
FROM silver_comercio_ext_estatisticas.tb_exportacoes;
```

## Agendamento
⚠️ Atenção
- O repositório não contém export de Jobs/Workflows Databricks.
- Validar cron, dependências e políticas de retry diretamente no workspace.
