"""Cierra el '</style>' del bloque aqua en las páginas 1/20/30 (el navegador
se comía el HTML posterior) e inyecta el snippet que mantiene la barra lateral
EXPANDIDA en todas las páginas (10/40/50 incluidas).

Uso:  python mcp/estilo_nav_final.py
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

SNIPPET = (
    "'  <script>(function(){var b=document.body;",
    "b&&(b.classList.add('js-navExpanded'),b.classList.remove('js-navCollapsed'));",
    "try{sessionStorage.setItem(\"ORA_WWV_apex.toggleCore.nav.215.preferenceForExpanded\",\"true\")}catch(e){}})();</script>',"
)


def esc(l: str) -> str:
    return l.replace("'", "''")


def export_vivo() -> str:
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
    return texto


def main() -> None:
    texto = export_vivo()
    print(f"[nav] export OK ({len(texto):,} chars)")
    orig = texto

    instrucciones = [
        # el elemento del array es una línea de código PL/SQL del source;
        # cada línea entre comillas simples con apostrofes internos DOBLADOS.
        ("page_00001", ["'  }',\n'~'');',", "'  }',\n'</style>',\n" + SNIPPET[0] + SNIPPET[1] + SNIPPET[2] + "\n'~');',"]),
        ("page_00020", ["'  }',\n'~'');',", "'  }',\n'</style>',\n" + SNIPPET[0] + SNIPPET[1] + SNIPPET[2] + "\n'~');',"]),
        ("page_00030", ["'  }',\n'~'');',", "'  }',\n'</style>',\n" + SNIPPET[0] + SNIPPET[1] + SNIPPET[2] + "\n'~');',"]),
        # en 10/40/50 la '<style>' ya cierra: solo el snippet antes de '</style>'
        ("page_00010", ["'</style>',\n'~'');',", "'  <script>(function(){var b=document.body;b&&(b.classList.add(\"js-navExpanded\"),b.classList.remove(\"js-navCollapsed\"));try{sessionStorage.setItem(\"ORA_WWV_apex.toggleCore.nav.215.preferenceForExpanded\",\"true\")}catch(e){}})();</script>',\n'</style>',\n'~'');',"]),
        ("page_00040", ["'</style>',\n'~'');',", "'  <script>(function(){var b=document.body;b&&(b.classList.add(\"js-navExpanded\"),b.classList.remove(\"js-navCollapsed\"));try{sessionStorage.setItem(\"ORA_WWV_apex.toggleCore.nav.215.preferenceForExpanded\",\"true\")}catch(e){}})();</script>',\n'</style>',\n'~'');',"]),
        ("page_00050", ["'</style>',\n'~'');',", "'  <script>(function(){var b=document.body;b&&(b.classList.add(\"js-navExpanded\"),b.classList.remove(\"js-navCollapsed\"));try{sessionStorage.setItem(\"ORA_WWV_apex.toggleCore.nav.215.preferenceForExpanded\",\"true\")}catch(e){}})();</script>',\n'</style>',\n'~'');',"]),
    ]

    n_fix = 0
    for pg, (ancla, reemplazo) in instrucciones:
        i = texto.index(f"--application/pages/{pg}")
        cand = [texto.find(x, i) for x in (
            "--application/pages/page_00020", "--application/pages/page_00030",
            "--application/pages/page_00040", "--application/pages/page_00050",
            "--application/shared_components", "--application/deployment")]
        fin = min([j for j in cand if j > i])
        bloque = texto[i:fin]
        c = bloque.count(ancla)
        if c != 1:
            print(f"[nav] AVISO {pg}: ancla x{c}; se omite")
            continue
        texto = texto[:i] + bloque.replace(ancla, reemplazo) + texto[fin:]
        n_fix += 1
    print(f"[nav] snippets/cierres aplicados en {n_fix}/6 páginas")

    if texto == orig:
        raise SystemExit("[nav] sin cambios; abortando")

    # reimport
    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    from mcp.importar_export import sentencias
    chunks = sentencias(texto)

    adm = conectar()
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[nav] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[nav] remove: {str(e)[:90]}")
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
            print(f"[nav] FALLO sentencia #{idx}: {str(e)[:300]}")
            print("\n".join(cbody.splitlines()[:8]))
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[nav] {n} sentencias OK — estilos cerrados y nav expandido")


if __name__ == "__main__":
    main()
