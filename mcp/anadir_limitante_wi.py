"""Añade el FACTOR LIMITANTE como píldora coloreada en el WI (antes y escenario).

Anclas sobre el export del estado vivo (la región de la pág. 10 lleva fuera de
repo los insertos de marca/nav, así que NO se re-emite con front_simulador):
  1. HTML: "<span id="swDelta"></span> <span id="swLimit"...>" → añade
     <span id="swLimitA"> (píldora del ANTES del corte 2025).
  2. JS: la línea $("swLimit").textContent="factor limitante: ..." → píldoras
     coloreadas con el mismo mapa de colores del Mapa, y cálculo client-side
     del antes (argmin de dim_*_antes).

Uso:  python mcp/anadir_limitante_wi.py
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

from src.common.oracle import conectar  # noqa: E402

APP_ID = 215


def esc(l: str) -> str:
    return l.replace("'", "''")


PILL_JS = [
    "    var LIMS=[['Demografía','#7C3AED'],['Vivienda','#B7791F'],['Servicios','#0078A8'],['Accesibilidad','#38A169'],['Empleo','#D69E2E']];",
    "    function pillLim(nombre){var c='#64748b';for(var i=0;i<LIMS.length;i++)if(LIMS[i][0]===String(nombre||'').trim())c=LIMS[i][1];",
    "      return '<span style=\"border:1px solid '+c+';color:'+c+';background:'+c+'14;border-radius:99px;padding:2px 9px;font-size:10px;font-weight:800;vertical-align:middle;\">'+esc(nombre)+'</span>';}",
    "    var candA=[[r.dim_dem_antes,'Demografía'],[r.dim_viv_antes,'Vivienda'],[r.dim_ser_antes,'Servicios'],[r.dim_acc_antes,'Accesibilidad'],[r.dim_emp_antes,'Empleo']];",
    "    var bestA=null;candA.forEach(function(x){if(bestA==null||x[0]<bestA[0])bestA=x;});",
    "    $(\"swLimitA\").innerHTML=pillLim(bestA[1]);",
    "    $(\"swLimit\").innerHTML=pillLim(r.factor_limitante);",
]


def main() -> None:
    conn = conectar(os.getenv('APEX_IMPORT_USER') or os.getenv('ORACLE_DB_USER'),
                    os.getenv('APEX_IMPORT_PASS') or os.getenv('ORACLE_DB_PASS'))
    cur = conn.cursor()
    o = cur.var(str, 65_000_000)
    cur.execute(
        "DECLARE l apex_t_export_files; BEGIN l := apex_export.get_application(p_application_id => :app); :o := l(1).contents; END;",
        app=APP_ID, o=o,
    )
    texto = o.getvalue()
    cur.close()
    conn.close()
    print(f"[lim] export OK ({len(texto):,} chars)")
    orig = texto

    # 1) HTML: añade la píldora del ANTES
    a1 = '<span id="swDelta"></span> <span id="swLimit" style="color:#64748b"></span>'
    b1 = ('<span id="swLimitA"></span> <span id="swDelta"></span> <span id="swLimit"></span>')
    n1 = texto.count(a1)
    if n1 != 1:
        raise SystemExit(f"[lim] ancla 1 (html) x{n1} (se esperaba 1) — ya aplicado? swLimitA: {texto.count('swLimitA')}")
    texto = texto.replace(a1, b1)
    print("[lim] html: píldora ANTES + escenario")

    # 2) JS: píldoras coloreadas (reemplaza la línea gris)
    a2 = '$("swLimit").textContent="factor limitante: "+esc(r.factor_limitante);'
    n2 = texto.count(a2)
    if n2 != 1:
        raise SystemExit(f"[lim] ancla 2 (js) x{n2} (se esperaba 1)")
    new_lines = "\n".join("'" + esc(l) + "'," for l in PILL_JS)
    texto = texto.replace("'" + esc(a2) + "',", new_lines)
    print("[lim] js: pillLim + argmin de dim_*_antes")

    if texto == orig:
        raise SystemExit("[lim] sin cambios")

    # reimport
    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    from mcp.importar_export import sentencias
    chunks = sentencias(texto)

    adm = conectar()
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[lim] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[lim] remove: {str(e)[:90]}")
    adm.commit()
    adm.close()

    conn = conectar(os.getenv('APEX_IMPORT_USER') or os.getenv('ORACLE_DB_USER'),
                    os.getenv('APEX_IMPORT_PASS') or os.getenv('ORACLE_DB_PASS'))
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
            print(f"[lim] FALLO sentencia #{idx}: {str(e)[:300]}")
            print("\n".join(cbody.splitlines()[:8]))
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[lim] {n} sentencias OK — factor limitante coloreado en el WI")


if __name__ == "__main__":
    main()
