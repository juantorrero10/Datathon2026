"""Añade la página 40 'Mapa' a la app 215 desde el export del estado ACTUAL.

Bloque nuevo = clon del bloque de la página 10 con:
  - ids nuevos (página 40, región ...0040, procesos ...0041/0042)
  - nombre 'Mapa', alias 'MAPA'
  - región con el front del mapa (mcp/front_mapa.py)
  - procesos AJAX: PRED (PV_MAPA) y GEO (PV_GEO_MUNIS)
Además añade la entrada 'Mapa' al menú de navegación.

Uso:  python mcp/anadir_pagina_mapa.py
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from web.front_mapa import CABECERA_MAPA, FRONT_MAPA  # noqa: E402
from src.common.oracle import conectar  # noqa: E402

BACKUPS = REPO / "web" / "backups"
APP_ID = 215
PAGE_ID = 40


def esc(l: str) -> str:
    return l.replace("'", "''")


def attr_region(lines: list[str]) -> str:
    """Atributo p_plug_source con el formato del usuario (BEGIN + HTP.P q'~')."""
    out = [",p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2("]
    out.append("'BEGIN',")
    out.append("'  -- 1. Estilos de la cabecera',")
    out.append("'  HTP.P(q''~" + esc(CABECERA_MAPA.splitlines()[0]) + "',")
    for line in CABECERA_MAPA.splitlines()[1:]:
        out.append("'" + esc(line) + "',")
    out.append("'~'');',")
    out.append("'',")
    out.append("'  -- 2. Mapa: estilos, HTML y JS',")
    out.append("'  HTP.P(q''~" + esc(FRONT_MAPA.splitlines()[0]) + "',")
    for line in FRONT_MAPA.splitlines()[1:-1]:
        out.append("'" + esc(line) + "',")
    out.append("'" + esc(FRONT_MAPA.splitlines()[-1]) + "~'');',")
    out.append("'END;'")
    out.append("))")
    return "\n".join(out)


def attr_proceso(lines: list[str]) -> str:
    out = [",p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2("]
    for line in lines[:-1]:
        out.append("'" + esc(line) + "',")
    out.append("'" + esc(lines[-1]) + "'")
    out.append("))")
    return "\n".join(out)


PRED_SRC = [
    "DECLARE",
    "  v_json CLOB;",
    "  v_len PLS_INTEGER;",
    "  v_pos PLS_INTEGER := 1;",
    "BEGIN",
    "  v_json := WKSP_DATATHON.PV_MAPA(TO_NUMBER(apex_application.g_x01));",
    "  v_len := DBMS_LOB.GETLENGTH(v_json);",
    "  WHILE v_pos <= v_len LOOP",
    "    HTP.PRN(DBMS_LOB.SUBSTR(v_json, 8000, v_pos));",
    "    v_pos := v_pos + 8000;",
    "  END LOOP;",
    "END;",
]

GEO_SRC = [
    "DECLARE",
    "  v_arr CLOB;",
    "  v_json CLOB;",
    "  v_len PLS_INTEGER;",
    "  v_pos PLS_INTEGER := 1;",
    "BEGIN",
    "  SELECT JSON_ARRAYAGG(",
    "    JSON_OBJECT('type' VALUE 'Feature',",
    "      'geometry' VALUE JSON(g.GEO),",
    "      'properties' VALUE JSON_OBJECT('cod' VALUE g.COD_INE, 'nombre' VALUE g.NOMBRE RETURNING CLOB)",
    "      RETURNING CLOB) RETURNING CLOB)",
    "  INTO v_arr FROM PV_GEO_MUNIS g;",
    "  v_json := '{\"type\":\"FeatureCollection\",\"features\":' || v_arr || '}';",
    "  v_len := DBMS_LOB.GETLENGTH(v_json);",
    "  WHILE v_pos <= v_len LOOP",
    "    HTP.PRN(DBMS_LOB.SUBSTR(v_json, 8000, v_pos));",
    "    v_pos := v_pos + 8000;",
    "  END LOOP;",
    "END;",
]


def mutar_clon(bloque: str) -> str:
    b = bloque
    b = b.replace("prompt --application/pages/page_00010", "prompt --application/pages/page_00040")
    b = b.replace(" p_id=>10", " p_id=>40", 1)
    b = b.replace("p_name=>'Simulador What-If'", "p_name=>'Mapa'")
    b = b.replace("p_alias=>'PERFIL-INSTITUCIONAL'", "p_alias=>'MAPA'")
    b = b.replace("p_step_title=>'Simulador What-If'", "p_step_title=>'Mapa'")
    b = b.replace("p_static_id=>'dashboard-institucional'", "p_static_id=>'mapa-interactivo'")
    b = b.replace("p_plug_name=>'Simulador What-If'", "p_plug_name=>'Mapa interactivo'")
    b = b.replace("wwv_flow_imp.id(8900550584000013)", "wwv_flow_imp.id(8900550584000040)")

    # región: sustituir el source completo
    i_ini = b.index(",p_plug_source=>")
    i_ini = b.rfind("\n", 0, i_ini) + 1
    i_fin = b.index(",p_plug_source_type=>", i_ini)
    i_fin = b.rfind("\n", 0, i_fin) + 1
    b = b[:i_ini] + attr_region(FRONT_MAPA.splitlines()) + "\n" + b[i_fin:]

    # procesos: DATOS -> PRED, SIMULAR -> GEO
    b = b.replace("p_process_name=>'DATOS'", "p_process_name=>'PRED'")
    b = b.replace("p_static_id=>'datos'", "p_static_id=>'pred'")
    b = b.replace("wwv_flow_imp.id(8900550584000011)", "wwv_flow_imp.id(8900550584000041)")
    b = b.replace("p_process_name=>'SIMULAR'", "p_process_name=>'GEO'")
    b = b.replace("p_static_id=>'simular'", "p_static_id=>'geo'")
    b = b.replace("wwv_flow_imp.id(8900550584000012)", "wwv_flow_imp.id(8900550584000042)")

    # sources de procesos
    for nombre, src in [("PRED", PRED_SRC), ("GEO", GEO_SRC)]:
        i_name = b.index(f"p_process_name=>'{nombre}'")
        i_clob = b.index(",p_process_sql_clob=>", i_name)
        i_clob = b.rfind("\n", 0, i_clob) + 1
        i_end = b.index(",p_process_clob_language=>", i_clob)
        i_end = b.rfind("\n", 0, i_end) + 1
        b = b[:i_clob] + attr_proceso(src) + "\n" + b[i_end:]
    return b


def main() -> None:
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    baseline = BACKUPS / f"sql_{stamp}_estado_usuario.sql"

    # 1) export del estado vivo (como parsing schema); si no se puede (app en
    #    RUN_ONLY tras un reimport), se usa el último baseline del usuario.
    from dotenv import load_dotenv
    load_dotenv(r'C:\Users\juan\apex-mcp\.env', override=True)
    import os
    user = os.getenv('APEX_IMPORT_USER') or os.getenv('ORACLE_DB_USER')
    pwd = os.getenv('APEX_IMPORT_PASS') or os.getenv('ORACLE_DB_PASS')
    texto = None
    try:
        adm = conectar(usuario=user, contraseña=pwd)
        o = adm.cursor().var(str, 65_000_000)
        cur = adm.cursor()
        cur.execute(
            """DECLARE l apex_t_export_files; BEGIN
                 l := apex_export.get_application(p_application_id => :app);
                 :o := l(1).contents; END;""", app=APP_ID, o=o)
        texto = o.getvalue()
        adm.close()
    except Exception as e:
        print(f"[mapa] export no disponible ahora ({str(e)[:120]}); usando último baseline")
        previos = sorted(BACKUPS.glob("sql_*_estado_usuario.sql"), key=lambda p: p.stat().st_mtime)
        if previos:
            texto = previos[-1].read_text(encoding="utf-8")
            print(f"[mapa] baseline usado: {previos[-1].name}")
    if texto is None:
        raise SystemExit("[mapa] sin baseline para mutar")
    BACKUPS.mkdir(parents=True, exist_ok=True)
    baseline.write_text(texto, encoding="utf-8")
    print(f"[mapa] base de mutación ({len(texto):,} chars)")

    # 2) localizar el bloque de la página 10 (prompt ... page_00010) y su fin (page_00020)
    i10 = texto.index("--application/pages/page_00010")
    i10 = texto.rfind("prompt", 0, i10 + 8)
    i20 = texto.index("--application/pages/page_00020")
    i20 = texto.rfind("prompt", 0, i20 + 8)
    clon = texto[i10:i20]

    # 3) mutar el clon
    clon = mutar_clon(clon)
    # separador final "/" propio
    bloque40 = clon.rstrip() + "\n/\n\n"

    # 4) insertar el bloque tras el bloque de la página 30
    i30end = texto.index("--application/deployment/definition")
    i30end = texto.rfind("prompt", 0, i30end + 8)
    i30end = texto.rfind("\n", 0, i30end) + 1
    texto = texto[:i30end] + bloque40 + texto[i30end:]

    # 5) menú: entrada 'Mapa' correcta (helper compartido)
    from web.menu_mapa import coloca_entrada_mapa
    texto, detalle = coloca_entrada_mapa(texto)
    print(f"[mapa] menú: {detalle}")

    # 6) importar
    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    from web.importar_export import sentencias
    chunks = sentencias(texto)

    import os
    user = os.getenv('APEX_IMPORT_USER') or os.getenv('ORACLE_DB_USER')
    pwd = os.getenv('APEX_IMPORT_PASS') or os.getenv('ORACLE_DB_PASS')
    adm = conectar(usuario=user, contraseña=pwd)
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[mapa] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[mapa] sin app previa ({str(e)[:90]})")
    adm.commit()
    adm.close()

    import os
    user = os.getenv("APEX_IMPORT_USER") or os.getenv("ORACLE_DB_USER")
    pwd = os.getenv("APEX_IMPORT_PASS") or os.getenv("ORACLE_DB_PASS")
    conn = conectar(usuario=user, contraseña=pwd)
    print(f"[mapa] importando como {user or 'ADMIN'}")
    cur = conn.cursor()
    # contexto de instalación: build status builder para que la app sea exportable/editable
    cur.execute(
        """BEGIN
             apex_application_install.set_application_id(215);
             apex_application_install.set_schema('WKSP_DATATHON');
             apex_application_install.set_build_status('RUN_AND_BUILD');
             apex_application_install.generate_offset;
           END;""")
    print("[mapa] contexto apex_application_install fijado")
    n = 0
    for idx, cbody in enumerate(chunks):
        if cbody is None:
            continue
        try:
            cur.execute(cbody)
            n += 1
        except Exception as e:
            print(f"[mapa] FALLO sentencia #{idx}: {str(e)[:300]}")
            print("\n".join(cbody.splitlines()[:8]))
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[mapa] {n} sentencias ejecutadas")
    print("[mapa] OK — página 40 creada")


if __name__ == "__main__":
    main()
