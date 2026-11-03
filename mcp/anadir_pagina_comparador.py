"""Añade la página 50 'Comparador' a la app 215 desde el export del estado ACTUAL.

Basado en `anadir_pagina_mapa.py` (clonado de la pág. 10 y mutación), con:
  - ids nuevos (página 50, región ...0050, procesos ...0051/0052)
  - nombre 'Comparador', alias 'COMPARADOR'
  - región con el front del comparador (web/front_comparador.py)
  - procesos AJAX: DATOS (se conserva tal cual, lista de municipios) y
    CMP (PV_MAPA(año, cod) — métricas del mapa para UN municipio)
Además coloca la entrada 'Comparador' en el Navigation Menu.

Uso:  python web/anadir_pagina_comparador.py
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from dotenv import load_dotenv  # noqa: E402
load_dotenv(r'C:\Users\juan\apex-mcp\.env', override=True)
from mcp.front_comparador import CABECERA_COMPARADOR, FRONT_COMPARADOR  # noqa: E402
from mcp.menu_comparador import coloca_entrada_comparador  # noqa: E402
from src.common.oracle import conectar  # noqa: E402

BACKUPS = REPO / "oracle_db" / "backups"
APP_ID = 215
PAGE_ID = 50


def esc(l: str) -> str:
    return l.replace("'", "''")


def attr_region(lines: list[str]) -> str:
    """p_plug_source en el formato del export (BEGIN + HTP.P q''~ ... ~'')."""
    cb = CABECERA_COMPARADOR.splitlines()
    fr = FRONT_COMPARADOR.splitlines()
    out = [",p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2("]
    out.append("'BEGIN',")
    out.append("'  -- 1. Estilos de la cabecera',")
    out.append("'  HTP.P(q''~" + esc(cb[0]) + "',")
    for line in cb[1:]:
        out.append("'" + esc(line) + "',")
    out.append("'~'');',")
    out.append("'',")
    out.append("'  -- 2. Comparador: estilos, HTML y JS',")
    out.append("'  HTP.P(q''~" + esc(fr[0]) + "',")
    for line in fr[1:-1]:
        out.append("'" + esc(line) + "',")
    out.append("'" + esc(fr[-1]) + "~'');',")
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


CMP_SRC = [
    "DECLARE",
    "  v_json CLOB;",
    "  v_len PLS_INTEGER;",
    "  v_pos PLS_INTEGER := 1;",
    "BEGIN",
    "  v_json := WKSP_DATATHON.PV_MAPA(TO_NUMBER(apex_application.g_x01), apex_application.g_x02);",
    "  v_len := DBMS_LOB.GETLENGTH(v_json);",
    "  WHILE v_pos <= v_len LOOP",
    "    HTP.PRN(DBMS_LOB.SUBSTR(v_json, 8000, v_pos));",
    "    v_pos := v_pos + 8000;",
    "  END LOOP;",
    "END;",
]


def mutar_clon(bloque: str) -> str:
    b = bloque

    # ids DEL CLON (export vivo: ids ya offseteados): los reasignamos con un
    # base = max(ids del clon) + 100, garantizando unicidad dentro del import
    # (el import se ejecuta sobre la app borrada, ids nuevos aplicados ahí).
    ids_orig = sorted({int(x) for x in re.findall(r"wwv_flow_imp\.id\((\d+)\)", b)})
    base = (ids_orig[-1] if ids_orig else 8900550584000000) + 100
    mapping = {}
    nuevo_id = base + 1
    for viejo in ids_orig:
        mapping[f"wwv_flow_imp.id({viejo})"] = f"wwv_flow_imp.id({nuevo_id})"
        nuevo_id += 1
    for a, nb in mapping.items():
        b = b.replace(a, nb)

    b = b.replace("prompt --application/pages/page_00010", "prompt --application/pages/page_00050")
    b = b.replace(" p_id=>10", " p_id=>50", 1)
    b = b.replace("p_name=>'Simulador What-If'", "p_name=>'Comparador'")
    b = b.replace("p_alias=>'PERFIL-INSTITUCIONAL'", "p_alias=>'COMPARADOR'")
    b = b.replace("p_step_title=>'Simulador What-If'", "p_step_title=>'Comparador'")
    b = b.replace("p_static_id=>'dashboard-institucional'", "p_static_id=>'comparador-interactivo'")
    b = b.replace("p_plug_name=>'Simulador What-If'", "p_plug_name=>'Comparador'")

    # región: sustituir el source completo
    i_ini = b.index(",p_plug_source=>")
    i_ini = b.rfind("\n", 0, i_ini) + 1
    i_fin = b.index(",p_plug_source_type=>", i_ini)
    i_fin = b.rfind("\n", 0, i_fin) + 1
    b = b[:i_ini] + attr_region(CABECERA_COMPARADOR.splitlines()) + "\n" + b[i_fin:]

    # procesos: ids nuevos para evitar colisiones con la pág. 10
    # (ya remapeados arriba; sólo renombramos SIMULAR -> CMP)
    b = b.replace("p_process_name=>'SIMULAR'", "p_process_name=>'CMP'")
    b = b.replace("p_static_id=>'simular'", "p_static_id=>'cmp'")
    i_name = b.index("p_process_name=>'" + "CMP'")
    i_clob = b.index(",p_process_sql_clob=>", i_name)
    i_clob = b.rfind("\n", 0, i_clob) + 1
    i_end = b.index(",p_process_clob_language=>", i_clob)
    i_end = b.rfind("\n", 0, i_end) + 1
    b = b[:i_clob] + attr_proceso(CMP_SRC) + "\n" + b[i_end:]
    return b


def main() -> None:
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    baseline = BACKUPS / f"sql_{stamp}_estado_usuario.sql"

    from dotenv import load_dotenv  # noqa: E402
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
        print(f"[cmp] export no disponible ahora ({str(e)[:120]}); usando último baseline")
        previos = sorted(BACKUPS.glob("sql_*_estado_usuario.sql"), key=lambda p: p.stat().st_mtime)
        if previos:
            texto = previos[-1].read_text(encoding="utf-8")
            print(f"[cmp] baseline usado: {previos[-1].name}")
    if texto is None:
        raise SystemExit("[cmp] sin baseline para mutar")
    if "--application/pages/page_00050" in texto:
        raise SystemExit("[cmp] la página 50 ya existe en el export; nada que hacer")
    BACKUPS.mkdir(parents=True, exist_ok=True)
    baseline.write_text(texto, encoding="utf-8")
    print(f"[cmp] base de mutación ({len(texto):,} chars)")

    # clone la página 10 (page_00010) hasta el inicio de la page_00020
    i10 = texto.index("--application/pages/page_00010")
    i10 = texto.rfind("prompt", 0, i10 + 8)
    i20 = texto.index("--application/pages/page_00020")
    i20 = texto.rfind("prompt", 0, i20 + 8)
    clon = texto[i10:i20]

    clon = mutar_clon(clon)
    bloque50 = clon.rstrip() + "\n/\n\n"

    # insertar tras el bloque de la página 40 (antes del deployment/definition)
    IDEP = texto.index("--application/deployment/definition")
    idep = texto.rfind("prompt", 0, IDEP + 8)
    idep = texto.rfind("\n", 0, idep) + 1
    texto = texto[:idep] + bloque50 + texto[idep:]

    # menú lateral compartido
    texto, detalle = coloca_entrada_comparador(texto)
    print(f"[cmp] menú: {detalle}")

    # importar
    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    from mcp.importar_export import sentencias
    chunks = sentencias(texto)

    adm = conectar()   # borrado de la app: requiere ADMIN (APEX_INSTANCE_ADMIN)
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[cmp] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[cmp] remove: {str(e)[:90]}")
    adm.commit()
    adm.close()

    conn = conectar(usuario=user, contraseña=pwd)
    print(f"[cmp] importando como {user or 'ADMIN'}")
    cur = conn.cursor()
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
            print(f"[cmp] FALLO sentencia #{idx}: {str(e)[:300]}")
            print("\n".join(cbody.splitlines()[:8]))
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[cmp] {n} sentencias ejecutadas")
    print("[cmp] OK — página 50 creada")


if __name__ == "__main__":
    main()
