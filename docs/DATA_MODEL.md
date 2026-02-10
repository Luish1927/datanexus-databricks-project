# Modelo de Dados

## Visão geral
O modelo final combina fatos de comércio exterior com dimensões de país, produto/classificação e calendário, além de uma visão empresarial por UF/CNAE.

## Fatos (Gold)

### `gold.rst_exp_imp_pais`
- Grão: `ano_operacao`, `mes_operacao`, `cod_pais`, `cod_ncm`, `cod_isic`, `cod_div_isic`.
- Métricas: `total_exportado`, `total_importado`, `saldo`.
- Particionamento: `ano_operacao`, `mes_operacao`.

### `gold.rst_comercio_exterior`
- Grão esperado (pelo DDL): `an_operacao`, `me_operacao`, `sg_unidade_federativa`, `cd_classificacao_internacional`, `tp_operacao`.
- Métricas: `vl_free_on_board`, `qt_peso_liquido_kg`.
- Particionamento: `an_operacao`, `me_operacao`.

⚠️ Atenção
- O notebook usa `merge` com `dfJoin`, não com `dfAgg`. Validar se o grão efetivo em produção é agregado ou detalhado.

### `gold.rst_base_empresarial`
- Grão: `sg_unidade_federativa`, `cod_cnae`.
- Métricas: `empresas_ativas`, `empresas_matriz`, `capital_social_total`, `qtd_mei`, `qtd_simples`.

## Dimensões (Gold)
- `gold.dim_pais`: `cod_pais`.
- `gold.dim_ncm_isic`: `cod_ncm` + atributos ISIC.
- `gold.dim_calendario`: `ano`, `mes`, `ano_mes`.
- `gold.dim_cnaes`: `cod_cnae`, `descricao`.
- `gold.dim_uf`: `cod_uf`, `sigla_uf`, `nome_uf`, `regiao`.

## Relacionamentos

Diagrama lógico simplificado:
```text
gold.rst_exp_imp_pais  --(cod_pais)------> gold.dim_pais
gold.rst_exp_imp_pais  --(cod_ncm)-------> gold.dim_ncm_isic
gold.rst_exp_imp_pais  --(ano,mes)-------> gold.dim_calendario

gold.rst_base_empresarial --(cod_cnae)---> gold.dim_cnaes
gold.rst_base_empresarial --(sigla_uf)---> gold.dim_uf
```

### Comércio exterior
- `gold.rst_exp_imp_pais.cod_pais` -> `gold.dim_pais.cod_pais` (N:1)
- `gold.rst_exp_imp_pais.cod_ncm` -> `gold.dim_ncm_isic.cod_ncm` (N:1)
- `gold.rst_exp_imp_pais.(ano_operacao, mes_operacao)` -> `gold.dim_calendario.(ano, mes)` (N:1)

### Base empresarial
- `gold.rst_base_empresarial.cod_cnae` -> `gold.dim_cnaes.cod_cnae` (N:1)
- `gold.rst_base_empresarial.sg_unidade_federativa` -> `gold.dim_uf.sigla_uf` (N:1 lógica)

⚠️ Atenção
- PK/FK não são materialmente impostas por constraint no código versionado; são chaves lógicas de modelagem/consumo.

## Modelo Silver de suporte
- Fatos:
  - `silver_comercio_ext_estatisticas.tb_exportacoes`
  - `silver_comercio_ext_estatisticas.tb_importacoes`
  - `silver_comercio_ext_estatisticas.tb_exportacoes_municipios`
  - `silver_comercio_ext_estatisticas.tb_importacoes_municipios`
- Dimensões/referências:
  - `silver_comercio_ext_indices.*`
  - `silver_comercio_ext_auxiliares.*`

## Exemplo de consulta analítica
```sql
SELECT
  f.ano_operacao,
  f.mes_operacao,
  p.pais,
  sum(f.total_exportado) AS exp_total,
  sum(f.total_importado) AS imp_total,
  sum(f.saldo) AS saldo_total
FROM gold.rst_exp_imp_pais f
LEFT JOIN gold.dim_pais p ON p.cod_pais = f.cod_pais
GROUP BY f.ano_operacao, f.mes_operacao, p.pais
ORDER BY f.ano_operacao, f.mes_operacao, p.pais;
```
