# Databricks notebook source
# MAGIC %md
# MAGIC # TOOLS :)
# MAGIC ## adicione as demais funções que for utilizar aqui S2

# COMMAND ----------

# MAGIC %md
# MAGIC ## Imports

# COMMAND ----------

import re, os, shutil, zipfile
from pyspark.sql.utils import AnalysisException

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parâmetros

# COMMAND ----------

# ================== PARAMS ==================
storage_account    = "storagedatanexus"

# Landing (raw):
landing_base       = f"abfss://raw@{storage_account}.dfs.core.windows.net/landingbeca2026jan"
src_cnpj_dir       = f"{landing_base}/cnpj"                 # *.zip
src_balanca_dir    = f"{landing_base}/balancacomercial"     # *.csv

# Bronze:
raw_base           = f"abfss://bronze@{storage_account}.dfs.core.windows.net"
raw_catalog        = "bronze"
raw_schema_cnpj    = "cnpj"
raw_schema_balanca = "comercio_exterior"

# Volume de staging (UC):
vol_dbfs_base      = "dbfs:/Volumes/raw/cnpj/stage"    # para Spark/dbutils.fs
vol_local_base     = "/Volumes/raw/cnpj/stage"         # para Python/zipfile (POSIX)

# Leitura de CSV:
csv_options = {
    "header": "true",
    "inferSchema": "true",
    "multiLine": "true",
    "encoding": "UTF-8",
    "sep": ";"           # ajuste se necessário
}

dry_run = False  # True = só imprime; False = executa
# ============================================

# COMMAND ----------

# MAGIC %md
# MAGIC ## Functions

# COMMAND ----------

def sanitize(name: str) -> str:
    n = re.sub(r'[^a-zA-Z0-9_]', '_', (name or '').strip().lower())
    n = re.sub(r'_+', '_', n).strip('_')
    if not n: n = "tabela"
    if n[0].isdigit(): n = "_" + n
    return n

def create_or_replace_external_delta_table(fqn_table: str, delta_path: str):
    stmt = f"CREATE OR REPLACE TABLE {fqn_table} USING DELTA LOCATION '{delta_path}'"
    if dry_run:
        print("[DRY-RUN] SQL:", stmt)
    else:
        spark.sql(stmt)


# COMMAND ----------

# MAGIC %md
# MAGIC ### hadoop

# COMMAND ----------

# MAGIC %md
# MAGIC ### pathJoin

# COMMAND ----------

# MAGIC %md
# MAGIC ### sanitizeName

# COMMAND ----------

# MAGIC %md
# MAGIC ### unzipAbfsToAbfs

# COMMAND ----------

# MAGIC %md
# MAGIC ### writeCsvAsDeltaRegisterTable

# COMMAND ----------

# MAGIC %md
# MAGIC ### copyCsvLandingToRawAsDelta
