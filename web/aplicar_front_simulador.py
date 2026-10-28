"""Aplica el front v3 al estado ACTUAL de la app 215 (no desde sql_original).

Difiere de editar_export_simulador.py: el usuario edita la app en el builder,
así que aquí el baseline es el export del estado VIVO (se guarda con fecha en
web/backups/) y la única mutación es sustituir la fuente de la región de
la pág. 10 por el front nuevo (mismo formato del usuario: BEGIN + HTP.P q'~...~').

Uso:  python mcp/aplicar_front_simulador.py
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from web.editar_export_contenido import CABECERA_CSS, FRONT_V3  # noqa: E402
from web.importar_export import sentencias  # noqa: E402
from src.common.oracle import conectar  # noqa: E402

BACKUPS = REPO / "web" / "backups"
APP_ID = 215
WORKSPACE = 9407325500210184


def esc(l: str) -> str:
    return l.replace("'", "''")


def attr_nuevo_source() -> str:
    """Atributo p_plug_source con el formato del usuario: BEGIN + 2 HTP.P."""
    rt: list[str] = ["BEGIN", "  -- 1. Estilos de la cabecera"]
    css = CABECERA_CSS.splitlines()
    rt.append("  HTP.P(q'~" + css[0])
    rt.extend(css[1:])
    rt.append("</style>~');")
    rt.append("")
    rt.append("  -- 2. Estilos, HTML y JS del simulador (prediccion + what-if)")
    fr = FRONT_V3.splitlines()
    rt.append("  HTP.P(q'~" + fr[0])
    rt.extend(fr[1:])
    rt.append("</script>~');")
    rt.append("END;")

    out = [",p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2("]
    for l in rt[:-1]:
        out.append("'" + esc(l) + "',")
    out.append("'" + esc(rt[-1]) + "'")
    out.append("))")
    return "\n".join(out)


def exportar_actual(cur) -> str:
    o = cur.var(str, 65_000_000)
    cur.execute(
        """
        DECLARE
            l apex_t_export_files;
        BEGIN
            l := apex_export.get_application(p_application_id => :app);
            :o := l(1).contents;
        END;
        """, app=APP_ID, o=o,
    )
    return o.getvalue()


def main() -> None:
    fecha = dt.date.today().isoformat()
    baseline = BACKUPS / f"sql_{fecha}_estado_usuario.sql"

    # 1) export del estado vivo (conexión ADMIN: apex_export requiere el rol)
    adm = conectar()
    texto = exportar_actual(adm.cursor())
    adm.close()
    texto_backup = texto
    BACKUPS.mkdir(parents=True, exist_ok=True)
    baseline.write_text(texto, encoding="utf-8")
    print(f"[front] baseline del estado del usuario -> {baseline.name} ({len(texto):,} chars)")

    # 2) sustituir el source de la región de la pág. 10
    ancla = "p_static_id=>'dashboard-institucional'"
    assert ancla in texto, "ancla de la región de la pág. 10 no encontrada"
    i_a = texto.index(ancla)
    i_ini = texto.index(",p_plug_source=>", i_a)
    i_ini = texto.rfind("\n", 0, i_ini) + 1
    i_fin = texto.index(",p_plug_source_type=>", i_ini)
    i_fin = texto.rfind("\n", 0, i_fin) + 1
    texto = texto[:i_ini] + attr_nuevo_source() + "\n" + texto[i_fin:]

    # 3) importar (borrar + importar como parsing schema)
    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    chunks = sentencias(texto)

    adm = conectar()
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[front] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[front] sin app previa que borrar ({str(e)[:90]})")
    adm.commit()
    adm.close()

    import os
    user = os.getenv("APEX_IMPORT_USER") or os.getenv("ORACLE_DB_USER")
    pwd = os.getenv("APEX_IMPORT_PASS") or os.getenv("ORACLE_DB_PASS")
    conn = conectar(usuario=user, contraseña=pwd)
    cur = conn.cursor()
    n = 0
    for idx, cbody in enumerate(chunks):
        if cbody is None:
            continue
        try:
            cur.execute(cbody)
            n += 1
        except Exception as e:
            print(f"[front] FALLO en sentencia #{idx}: {str(e)[:300]}")
            print("---- inicio ----")
            print("\n".join(cbody.splitlines()[:8]))
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[front] {n} sentencias ejecutadas")

    # 4) verificación
    adm = conectar()
    with adm.cursor() as c:
        c.execute(
            "SELECT page_id, region_name, TO_CHAR(template_id) AS t "
            "FROM apex_application_page_regions WHERE application_id = :1 ORDER BY page_id", [APP_ID],
        )
        for row in c.fetchall():
            print("[front]   región", row[0], "-", row[1], "- tpl", row[2])
    adm.close()
    print(f"[front] OK — baseline del estado previo en {baseline.name}")


if __name__ == "__main__":
    main()
