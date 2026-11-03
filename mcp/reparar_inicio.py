"""Repara la región 'Inicio' (pág. 1): restaura el bloq definitions intacto,
elimina duplicados CSS y añade UN bloque aqua bien construido y cerrado.
También cierra el `</style>` de los bloques aqua insertados en 20 y 30.

Uso:  python mcp/reparar_inicio.py
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

BLOQUE_AQUA = [
    "  HTP.P(q'~<style>",
    ".t-Header,.t-Header .t-Header-branding,.t-Header .t-Header-navBar{background:#0f766e!important}",
    ".t-Header .a-Logo,.t-Header .a-Logo .a-Logo-text,.t-Header .t-Header-branding .a-Logo span{color:#fff!important}",
    ".t-Header .a-Logo:hover{color:#5eead4!important}",
    ".a-TreeView li.is-selected>.a-TreeView-label,",
    ".a-TreeView a.is-selected,",
    ".a-TreeView .a-TreeView-label.is-selected,",
    ".t-TreeNav li.is-selected{",
    "  background-color:#fff!important;",
    "  color:#0f2a44!important;",
    "}",
    "</style>",
    "~');",
]


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


def esc(l: str) -> str:
    return l.replace("'", "''")


def main() -> None:
    texto = export_vivo()
    print(f"[reparar] export OK ({len(texto):,} chars)")
    orig = texto

    i = texto.index("--application/pages/page_00001")
    cand = [texto.find("--application/pages/page_00020", i),
            texto.find("--application/shared", i),
            texto.find("--application/deployment", i)]
    fin = min([j for j in cand if j > i])
    bloque = texto[i:fin]

    # ── reconstrucición de la región 'Portada' (page 1, bloque pv-portal) ──
    m = bloque.search if False else None
    ini = bloque.index("p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(")
    ini = bloque.rfind("\n", 0, ini) + 1
    m = re.search(r"'</script>~''\);',", bloque)
    if not m:
        raise SystemExit("[reparar] no encuentro la primera baliza de cierre del pv-portal")
    fin_portal = m.end()
    # el texto de la fuente: desde el join( hasta la baliza; cada línea strip de ,'
    lineas = []
    cuerpo = bloque[ini:fin_portal]
    for ln in cuerpo.splitlines():
        s = ln.strip()
        if s.startswith("'") and s.endswith("',"):
            lineas.append(s[1:-2].replace("''", "'"))
        elif s.startswith("'") and s.endswith("'" ) or s == "'":
            lineas.append(s[1:-1].replace("''", "'"))
    # primero: BEGIN; después el resto con el cierre del primer HTP.P:
    # conservamos TODO hasta la PRIMERA baliza de cierre del pv-portal: puede
    # venir combinada ("...</script>~');" en un solo elemento del export) o
    # separada ("</script>" y a continuación "~');").
    j_cierre = None
    forma_combinada = False
    for k, l in enumerate(lineas):
        if l == "</script>":
            j_cierre = k
            forma_combinada = False
            break
        if l.endswith("</script>~');"):
            lineas[k] = l[: l.rindex("</script>") + len("</script>")]
            lineas.insert(k + 1, "~');")
            j_cierre = k
            forma_combinada = True
            break
    if j_cierre is None:
        raise SystemExit("[reparar] el pv-portal no termina en </script>")
    # líneas válidas del cuerpo original: BEGIN + HTP.P(q'~ ... hasta ~');
    while lineas[j_cierre + 1] != "~');":
        j_cierre += 1
    fuente_limpia = lineas[: j_cierre + 2]   # ... </script>  ~');
    fuente_limpia.append("END;")             # cierro el bloque BEGIN

    # ── ahora el bloque aqua nuevo, con reglas y cierre completo ──
    extra = ["'BEGIN',"]
    for l in fuente_limpia:
        extra.append("'" + esc(l) + "',")
    for l in BLOQUE_AQUA:
        extra.append("'" + esc(l) + "',")   # el ÚLTIMO es "~');" (cierre del q')
    extra.append("'END;'")                   # cierra el BEGIN
    nuevo = ("p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(\n"
             + "\n".join(extra) + "\n))")

    i_ini = bloque.index("p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(")
    i_ini = bloque.rfind("\n", 0, i_ini) + 1
    i_fin = bloque.index(",p_plug_source_type=>", i_ini)
    i_fin = bloque.rfind("\n", 0, i_fin) + 1
    bloque_nuevo = bloque[:i_ini] + nuevo + "\n" + bloque[i_fin:]
    texto = texto[:i] + bloque_nuevo + texto[fin:]
    print("[reparar] página 1 reconstruida:", len(fuente_limpia), "líneas + aqua")

    # ── páginas 20 y 30: cierre </style> antes del ~'); del BLOQUE aqua ──
    for pg, marca in (("page_00020", "sw20"), ("page_00030", "pv30")):
        i = texto.index(f"--application/pages/{pg}")
        cand = [texto.find("--application/pages/page_00030", i),
                texto.find("--application/pages/page_00040", i),
                texto.find("--application/pages/page_00050", i),
                texto.find("--application/deployment", i)]
        fin = min([j for j in cand if j > i])
        b2 = texto[i:fin]
        if "t-TreeNav li.is-selected{" not in b2:
            print(f"[reparar] {pg}: sin bloque aqua; se omite")
            continue
        # último "~');" del bloque — su HTP.P aqua; asegurar que el <style> cierra
        if "HTP.P(q'~<style>" in b2 and "li.is-selected{" in b2:
            idx2 = b2.rindex("~');")
            # el carácter antes del cierre '='?': si el bloque no cierra </style>, lo añadimos
            zona = b2[idx2 - 2000: idx2 + 4]
            if "</style>~');" not in zona:
                b2n = b2[:idx2] + "</style>\n" + b2[idx2:]
                texto = texto[:i] + b2n + texto[fin:]
                print(f"[reparar] {pg}: </style> añadido al bloque aqua")

    if texto == orig:
        raise SystemExit("[reparar] sin cambios; nada que hacer")

    # ── reimport ──
    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    from mcp.importar_export import sentencias
    chunks = sentencias(texto)

    adm = conectar()
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[reparar] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[reparar] remove: {str(e)[:90]}")
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
            print(f"[reparar] FALLO sentencia #{idx}: {str(e)[:300]}")
            print("\n".join(cbody.splitlines()[:8]))
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[reparar] {n} sentencias OK — región Inicio reparada")


if __name__ == "__main__":
    main()
