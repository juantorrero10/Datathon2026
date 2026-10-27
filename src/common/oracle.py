"""Conexión LOCAL a Oracle (thin python-oracledb) con el clon de credenciales del MCP.

Se usa solo para las escrituras de datos gruesos (staging ONNX, INSERT masivos)
que serían ineficientes por el canal MCP. Las credenciales se leen del mismo
.env que usa el servidor apex-mcp (fuera del repo).
"""

from __future__ import annotations

from pathlib import Path
import os

import oracledb
from dotenv import load_dotenv

ENV_FILE = Path(os.getenv("APEX_MCP_ENV_FILE", r"C:\Users\juan\apex-mcp\.env"))


def conectar(usuario: str | None = None, contraseña: str | None = None) -> oracledb.Connection:
    load_dotenv(ENV_FILE, override=True)
    user = usuario or os.environ["ORACLE_DB_USER"]
    password = contraseña or os.environ["ORACLE_DB_PASS"]
    wallet_dir = Path(os.environ["ORACLE_WALLET_DIR"])
    conn = oracledb.connect(
        user=user,
        password=password,
        dsn=os.environ["ORACLE_DSN"],
        config_dir=wallet_dir,
        wallet_location=wallet_dir,
        wallet_password=os.environ.get("ORACLE_WALLET_PASSWORD"),
    )
    esquema = os.environ.get("APEX_SCHEMA", "WKSP_DATATHON").upper()
    with conn.cursor() as cur:
        cur.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {esquema}")
    return conn


ESQUEMA = os.environ  # placeholder, se calcula al conectar
