"""V2 del parche JS: sustituye la LÍNEA real (con su sangría) de swLimit por
el bloque pillLim (colores del map)+ argmin del antes.

Uso:  python mcp/anadir_limitante_wi2.py
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

PILL_JS = [
    "    var LIMS=[['Demografía','#7C3AED'],['Vivienda','#B7791F'],['Servicios','#0078A8'],['Accesibilidad','#38A169'],['Empleo','#D69E2E']];",
    "    function pillLim(nombre){var c='#64748b';for(var i=0;i<LIMS.length;i++)if(LIMS[i][0]===String(nombre||'').trim())c=LIMS[i][1];",
    "      return '<span style=\"border:1px solid '+c+';color:'+c+';background:'+c+'14;border-radius:99px;padding:2px 9px;font-size:10px;font-weight:800;vertical-align:middle;\">'+esc(nombre)+'</span>';}",
    "    var candA=[[r.dim_dem_antes,'Demografía'],[r.dim_viv_antes,'Vivienda'],[r.dim_ser_antes,'Servicios'],[r.dim_acc_antes,'Accesibilidad'],[r.dim_emp_antes,'Empleo']];",
    "    var bestA=null;candA.forEach(function(x){if(bestA==null||x[0]<bestA[0])bestA=x;});",
    "    $(\"swLimitA\").innerHTML=pillLim(bestA[1]);",
    "    $(\"swLimit\").innerHTML=pillLim(r.factor_limitante);",
]


def esc(l: str) -> str:
    return l.replace("'", "''")


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
    print(f"[lim2] export OK ({len(texto):,} chars)")
    orig = texto

    # 1) HTML píldora (aplicado si falta)
    a1 = '<span id="swDelta"></span> <span id="swLimit" style="color:#64748b"></span>'
    if "<span id=\"swLimitA\"" not in texto:
        b1 = '<span id="swLimitA"></span> <span id="swDelta"></span> <span id="swLimit"></span>'
        if texto.count(a1) != 1:
            raise SystemExit("[lim2] ancla html x" + str(texto.count(a1)))
        texto = texto.replace(a1, b1)
        print("[lim2] html píldora antes aplicada")

    pat = re.compile(r"^'?\$\(\\?\"swLimit.*?factor limitante[^\n]*$,")
    hits = [l for l in texto.splitlines() if 'swLimit' in l and 'textContent' in l and 'factor limitante' in l]
    if "function pillLim" in texto:
        print("[lim2] pillLim ya está; nada que hacer en JS")
    elif len(hits) != 1:
        print(f"[lim2] líneas swLimit🖂{len(hits)} → se omite el JS")
        raise SystemExit("[lim2] sin ancla JS única")
    else:
        linea = hits[0]
        sangria = re.match(r"'?\s*", linea).group(0)
        indent = re.match(r"'\s*", linea).group(0)[1:] if linea.startswith("'") else sangria
        nuevo = []
        for l in PILL_JS:
            content = l.strip()
            nuevo.append("'" + esc(indent + content) + "',")
        # quitar la línea vieja y añadir las nuevas
        lineas2 = texto.splitlines()
        idx = None
        for k, l in enumerate(lineas2):
            if "swLimit" in l and "textContent" in l and "factor limitante" in l:
                idx = k
                break
        lineas2[idx:idx + 1] = nuevo
        texto = "\n".join(lineas2)
        print("[lim2] JS: píldoras coloreadas + argmin")

    # reimport
    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    from mcp.importar_export import sentencias
    chunks = sentencias(texto)

    adm = conectar()
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[lim2] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[lim2] remove: {str(e)[:90]}")
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
            print(f"[lim2] FALLO sentencia #{idx}: {str(e)[:300]}")
            print("\n".join(cbody.splitlines()[:8]))
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[lim2] {n} sentencias OK")


if __name__ == "__main__":
    main()
