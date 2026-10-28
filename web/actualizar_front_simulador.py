"""Actualiza SOLO la región de la página 10 (Simulador What-If) con el
front canonizado de web/front_simulador.py (incluye el parche de auto-jugada
desde el Mapa). Requiere la app 215 en RUN_AND_BUILD.

Uso:  python web/actualizar_front_simulador.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from dotenv import load_dotenv  # noqa: E402
load_dotenv(r'C:\Users\juan\apex-mcp\.env', override=True)
import os  # noqa: E402

from web.front_simulador import CABECERA_SIM, FRONT_SIM  # noqa: E402
from src.common.oracle import conectar  # noqa: E402

APP_ID = 215


def esc(l: str) -> str:
    return l.replace("'", "''")


def region_source_lines() -> list[str]:
    """BEGIN + dos HTP.P(q'~...~'); (formato ejecutable), por líneas."""
    out = ["BEGIN",
           "  -- 1. Estilos de la cabecera",
           "  HTP.P(q'~" + CABECERA_SIM.splitlines()[0]]
    out += ["  " + line for line in CABECERA_SIM.splitlines()[1:]]
    out[-1] += "~');"
    out += ["", "  -- 2. Estilos, HTML y JS del simulador (prediccion + what-if)",
            "  HTP.P(q'~" + FRONT_SIM.splitlines()[0]]
    out += ["  " + line for line in FRONT_SIM.splitlines()[1:]]
    out[-1] += "~');"
    out.append("END;")
    return out


def attr_region() -> str:
    """p_plug_source en formato export (comillas dobladas por esc())."""
    lines = region_source_lines()
    out = [",p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2("]
    out.append("'" + esc(lines[0]) + "',")
    for line in lines[1:-1]:
        out.append("'" + esc(line) + "',")
    out.append("'" + esc(lines[-1]) + "'")
    out.append("))")
    return "\n".join(out)


def attr_region() -> str:
    lines = region_source_lines()
    out = [",p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2("]
    out.append("'" + esc(lines[0]) + "',")
    for line in lines[1:-1]:
        out.append("'" + esc(line) + "',")
    out.append("'" + esc(lines[-1]) + "'")
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
        "DECLARE l apex_t_export_files; BEGIN l := apex_export.get_application(p_application_id => :app); :o := l(1).contents; END;",
        app=APP_ID, o=o,
    )
    texto = o.getvalue()
    print(f"[sim] export OK ({len(texto):,} chars)")

    # 2) sustituir el source de la región de la pág. 10
    ancla = "p_static_id=>'dashboard-institucional'"
    i_a = texto.index(ancla)
    i_ini = texto.index(",p_plug_source=>", i_a)
    i_ini = texto.rfind("\n", 0, i_ini) + 1
    i_fin = texto.index(",p_plug_source_type=>", i_ini)
    i_fin = texto.rfind("\n", 0, i_fin) + 1
    texto = texto[:i_ini] + attr_region() + "\n" + texto[i_fin:]
    print(f"[sim] región pág. 10 re-emitida ({len(texto):,} chars)")

    # 3) reimportar (borrar + importar)
    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    from web.importar_export import sentencias
    chunks = sentencias(texto)

    adm = conectar()
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[sim] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[sim] remove: {str(e)[:90]}")
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
            print(f"[sim] FALLO sentencia #{idx}: {str(e)[:250]}")
            print("\n".join(cbody.splitlines()[:8]))
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[sim] {n} sentencias OK — región pág. 10 actualizada")


if __name__ == "__main__":
    main()
