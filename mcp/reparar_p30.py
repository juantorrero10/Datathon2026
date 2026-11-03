"""Repara la pág. 30: añade la primera baliza de cierre (~');) tras </script>.

El bloque aqua estaba correcto pero el cierre del PRIMER HTP.P fué consumido.
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
ANCLA = "'</script>',\n'  HTP.P(q''~<style>',"
REMPLAZO = "'</script>',\n'~'');',\n'  HTP.P(q''~<style>',"


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
    print(f"[p30] export OK ({len(texto):,} chars)")
    orig = texto

    i = texto.index("--application/pages/page_00030")
    cand = [texto.find("--application/pages/page_00040", i), texto.find("--application/shared", i)]
    fin = min([j for j in cand if j > i])
    bloque = texto[i:fin]
    n = bloque.count(ANCLA)
    if n != 1:
        raise SystemExit(f"[p30] el ancla aparece {n} veces (se esperaba 1)")
    bloque_nuevo = bloque.replace(ANCLA, REMPLAZO, 1)
    texto = texto[:i] + bloque_nuevo + texto[fin:]

    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    from mcp.importar_export import sentencias
    chunks = sentencias(texto)

    adm = conectar()
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[p30] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[p30] remove: {str(e)[:90]}")
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
            print(f"[p30] FALLO sentencia #{idx}: {str(e)[:300]}")
            print("\n".join(cbody.splitlines()[:8]))
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[p30] {n} sentencias OK — primera baliza restaurada en la pág. 30")


if __name__ == "__main__":
    main()
