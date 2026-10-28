"""Actualiza SOLO la región de la página 40 (Mapa) con el FRONT_MAPA actual.
Requiere la app 215 en RUN_AND_BUILD (para que el export funcione).

Uso:  python mcp/actualizar_front_mapa.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from dotenv import load_dotenv
load_dotenv(r'C:\Users\juan\apex-mcp\.env', override=True)
import os  # noqa: E402
from mcp.front_mapa import CABECERA_MAPA, FRONT_MAPA  # noqa: E402
from src.common.oracle import conectar  # noqa: E402

APP_ID = 215


def esc(l: str) -> str:
    return l.replace("'", "''")


def attr_region() -> str:
    out = [",p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2("]
    out.append("'BEGIN',")
    out.append("'  -- 1. Estilos de la cabecera',")
    css = CABECERA_MAPA.splitlines()
    out.append("'  HTP.P(q''~" + esc(css[0]) + "',")
    for line in css[1:]:
        out.append("'" + esc(line) + "',")
    out.append("'~'');',")
    out.append("'',")
    out.append("'  -- 2. Mapa: estilos, HTML y JS',")
    fl = FRONT_MAPA.splitlines()
    out.append("'  HTP.P(q''~" + esc(fl[0]) + "',")
    for line in fl[1:-1]:
        out.append("'" + esc(line) + "',")
    out.append("'" + esc(fl[-1]) + "~'');',")
    out.append("'END;'")
    out.append("))")
    return "\n".join(out)


def main() -> None:
    user = os.getenv('APEX_IMPORT_USER') or os.getenv('ORACLE_DB_USER')
    pwd = os.getenv('APEX_IMPORT_PASS') or os.getenv('ORACLE_DB_PASS')

    # 1) export del estado vivo
    conn = conectar(usuario=user, contraseña=pwd)
    cur = conn.cursor()
    o = cur.var(str, 65_000_000)
    cur.execute(
        """DECLARE l apex_t_export_files; BEGIN
             l := apex_export.get_application(p_application_id => :app);
             :o := l(1).contents; END;""", app=APP_ID, o=o)
    texto = o.getvalue()
    print(f"[upd] export OK ({len(texto):,} chars)")

    # 2) sustituir el source de la región de la pág. 40 y el del proceso GEO
    ancla = "p_static_id=>'mapa-interactivo'"
    i_a = texto.index(ancla)
    i_ini = texto.index(",p_plug_source=>", i_a)
    i_ini = texto.rfind("\n", 0, i_ini) + 1
    i_fin = texto.index(",p_plug_source_type=>", i_ini)
    i_fin = texto.rfind("\n", 0, i_fin) + 1
    texto = texto[:i_ini] + attr_region() + "\n" + texto[i_fin:]

    i_geo = texto.index("p_process_name=>'GEO'")
    i_cg = texto.index(",p_process_sql_clob=>", i_geo)
    i_cg = texto.rfind("\n", 0, i_cg) + 1
    i_fg = texto.index(",p_process_clob_language=>", i_cg)
    i_fg = texto.rfind("\n", 0, i_fg) + 1
    from mcp.anadir_pagina_mapa import GEO_SRC, attr_proceso, PRED_SRC
    texto = texto[:i_cg] + attr_proceso(GEO_SRC) + "\n" + texto[i_fg:]

    i_pred = texto.index("p_process_name=>'PRED'")
    i_cp = texto.index(",p_process_sql_clob=>", i_pred)
    i_cp = texto.rfind("\n", 0, i_cp) + 1
    i_fp = texto.index(",p_process_clob_language=>", i_cp)
    i_fp = texto.rfind("\n", 0, i_fp) + 1
    texto = texto[:i_cp] + attr_proceso(PRED_SRC) + "\n" + texto[i_fp:]
    print(f"[upd] región pág. 40 actualizada ({len(texto):,} chars)")

    # 3) reimportar (borrar + importar)
    import re
    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    from mcp.importar_export import sentencias
    chunks = sentencias(texto)

    adm = conectar()
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[upd] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[upd] remove: {str(e)[:90]}")
    adm.commit()
    adm.close()

    cur.execute(
        """BEGIN
             apex_application_install.set_application_id(215);
             apex_application_install.set_schema('WKSP_DATATHON');
             apex_application_install.set_build_status('RUN_AND_BUILD');
             apex_application_install.generate_offset;
           END;""")
    n = 0
    for idx, cbody in enumerate(chunks):
        if cbody is None:
            continue
        try:
            cur.execute(cbody)
            n += 1
        except Exception as e:
            print(f"[upd] FALLO sentencia #{idx}: {str(e)[:250]}")
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[upd] {n} sentencias OK — región pág. 40 actualizada")


if __name__ == "__main__":
    main()
