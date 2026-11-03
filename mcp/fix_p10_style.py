"""Limpia el '</style>' duplicado de la pág. 10 (el snippet quedó antes del cierre):
   '  },' '  <script>snippet</script>',' '  </style>',' '  </style>~');'
→        '  },' '  <script>snippet</script>',' '  </style>~');'
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
ANCLA = "'  </script>~'');',"


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
    orig = texto

    i = texto.index("--application/pages/page_00010")
    j = texto.index("--application/pages/page_00020")
    blk = texto[i:j]
    # el par duplicado: '</style>',  <newline>  '</style>~');
    d = re.compile(r"'\s*</style>',\s*\n(\s*'([^']*?~'\);')',)")
    m = d.findall(blk)
    if len(m) != 1:
        raise SystemExit(f"[fix10] ancla x{len(m)} (se esperaba 1)")
    blk_n = d.sub(lambda m2: "'" + m2.group(1), blk, count=1) if False else d.sub(lambda mm: "'" + mm.group(1), blk, count=1)
    # añade el snippet JUSTO antes del </style> propio (queda dentro de la <style>)
    snippet = ("'  <script>(function(){var b=document.body;"
               "b&&(b.classList.add(\"js-navExpanded\"),b.classList.remove(\"js-navCollapsed\"));"
               "try{sessionStorage.setItem(\"ORA_WWV_apex.toggleCore.nav.215.preferenceForExpanded\",\"true\")}"
               "catch(e){}})();</script>',\n")
    blk_n = blk_n.replace("'  </style>~');'", snippet + "'  </style>~');'")
    if "js-navExpanded" not in blk_n:
        raise SystemExit("[fix10] el snippet no entró")
    texto = texto[:i] + blk_n + texto[j:]

    txt = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    from mcp.importar_export import sentencias
    chunks = sentencias(txt)

    adm = conectar()
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print("[fix10] app previa eliminada")
        except Exception as e:
            print(f"[fix10] remove: {str(e)[:90]}")
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
            print(f"[fix10] FALLO sentencia #{idx}: {str(e)[:300]}")
            print("\n".join(cbody.splitlines()[:8]))
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print("[fix10] OK — pág. 10 exacta")


if __name__ == "__main__":
    main()
