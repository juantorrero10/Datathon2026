"""Ciclo completo de reimport de la app 215 con el front del Simulador.

1. Conexión ADMIN: elimina la app 215 si existe (el import exige que no exista).
2. Conexión como parsing schema (WKSP_DATATHON, credenciales en .env con
   APEX_IMPORT_USER/APEX_IMPORT_PASS): ejecuta el export modificado
   (web/backups/simulador.sql) con p_default_workspace_id=>NULL, que es la
   única variante que ha funcionado en este Autonomous (el 0183/0184 del export
   provocan ORA-02291 / ORA-20987).

Uso:  python mcp/importar_export.py [ruta_del_f_sql]
      (por defecto: web/backups/simulador.sql)
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from src.common.oracle import conectar  # noqa: E402

DEFAULT = REPO / "web" / "backups" / "simulador.sql"
SQLPLUS = re.compile(r"^\s*(set|whenever|prompt|col|skip)\b", re.I)
WORKSPACE = 9407325500210184
APP_ID = 215


def sentencias(texto: str) -> list[str | None]:
    chunks = []
    for chunk in re.split(r"\n?^\s*/\s*$", texto, flags=re.M):
        lineas = [l for l in chunk.splitlines() if not SQLPLUS.match(l)]
        cuerpo = "\n".join(lineas).strip()
        if not cuerpo:
            continue
        c = cuerpo.lstrip()
        if c.startswith("begin") or c.startswith("declare") or c.startswith("--"):
            chunks.append(c)
        else:
            chunks.append(None)
    return chunks


def main() -> None:
    fichero = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    texto = fichero.read_text(encoding="utf-8")
    # única variante que funciona: el workspace lo resuelve el schema al que conectamos
    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    chunks = sentencias(texto)

    # 1) borrar la app actual (conexión ADMIN)
    adm = conectar()
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[import] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[import] sin app previa que borrar ({str(e)[:90]})")
    adm.commit()
    adm.close()

    # 2) importar como parsing schema
    user = os.getenv("APEX_IMPORT_USER") or os.getenv("ORACLE_DB_USER")
    pwd = os.getenv("APEX_IMPORT_PASS") or os.getenv("ORACLE_DB_PASS")
    load = None
    from src.common.oracle import ENV_FILE
    if (user, pwd) == (os.getenv("ORACLE_DB_USER"), None):
        from dotenv import load_dotenv
        load_dotenv(ENV_FILE, override=False)
        user = os.getenv("APEX_IMPORT_USER") or user
    conn = conectar(usuario=user, contraseña=pwd)
    print(f"[import] importando {fichero.name} como {user}")
    cur = conn.cursor()
    n_ejec = 0
    for idx, cbody in enumerate(chunks):
        if cbody is None:
            continue
        try:
            cur.execute(cbody)
            n_ejec += 1
        except Exception as e:
            print(f"[import] FALLO en sentencia #{idx}: {str(e)[:300]}")
            print("---- inicio ----")
            print("\n".join(cbody.splitlines()[:6]))
            raise SystemExit(1)
    conn.commit()
    print(f"[import] {n_ejec} sentencias ejecutadas")
    cur.close(); conn.close()

    # 3) verificación con conexión ADMIN (apex_applications es visible solo ahí)
    adm = conectar()
    with adm.cursor() as c:
        c.execute(
            "SELECT page_id, page_name FROM apex_application_pages "
            "WHERE application_id = :1 ORDER BY page_id",
            [APP_ID],
        )
        for row in c.fetchall():
            print("[import]   página", row[0], "-", row[1])
    adm.close()
    print("[import] OK")


if __name__ == "__main__":
    main()
