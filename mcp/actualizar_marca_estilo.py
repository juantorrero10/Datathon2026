"""Marca + estilo global: 'Pueblos con Vida' → 'MadridNext', cabecera aqua y
selección blanca del nav en TODAS las páginas de la app 215.

En el export del estado vivo:
  1. Marca: p_logo_text, p_name (create_flow) y comentarios.
  2. Páginas 10/40/50 (con cabecera propia): añade tras la regla del logo la
     regla de SELECCIÓN blanca del nav.
  3. Páginas 1/20/30 (sin cabecera propia): inserta un segundo HTP.P con el
     bloque de estilos aqua antes del cierre de su región.

Uso:  python mcp/actualizar_marca_estilo.py
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

BLOQUE_NAV_BLANCO = [
    ".a-TreeView li.is-selected>.a-TreeView-label,",
    ".a-TreeView a.is-selected,",
    ".a-TreeView .a-TreeView-label.is-selected,",
    ".t-TreeNav li.is-selected{",
    "  background-color:#fff!important;",
    "  color:#0f2a44!important;",
    "}",
]

BLOQUE_CABECERA = [
    ".t-Header,.t-Header .t-Header-branding,.t-Header .t-Header-navBar{background:#0f766e!important}",
    ".t-Header .a-Logo,.t-Header .a-Logo .a-Logo-text,.t-Header .t-Header-branding .a-Logo span{color:#fff!important}",
    ".t-Header .a-Logo:hover{color:#5eead4!important}",
] + BLOQUE_NAV_BLANCO

def esc(l: str) -> str:
    return l.replace("'", "''")


CERRADURAS = {
    "page_00001": (
        ["'</script>~'');',"],
        "'</script>~'');',\n"
        + "'  HTP.P(q''~<style>',\n"
        + "\n".join("'" + esc(l) + "'," for l in BLOQUE_CABECERA)
        + "\n'~'');',"
    ),
    "page_00020": (
        # cierre combinado en UNA línea
        ["'</div>~''); END;'))"],
        "'</div>~'');',\n"
        + "'  HTP.P(q''~<style>',\n"
        + "\n".join("'" + esc(l) + "'," for l in BLOQUE_CABECERA)
        + "\n'~'');',\n'END;'))"
    ),
    "page_00030": (
        # cierre COMBINADO: '</script>' + "'~''); END;'))" en dos líneas (par único)
        ["'</script>',\n'~''); END;'))"],
        "'</script>',\n"
        + "'  HTP.P(q''~<style>',\n"
        + "\n".join("'" + esc(l) + "'," for l in BLOQUE_CABECERA)
        + "\n'~'');',\n'END;'))"
    ),
}


def export_vivo() -> tuple[str, str]:
    conn = conectar(os.getenv('APEX_IMPORT_USER') or os.getenv('ORACLE_DB_USER'),
                    os.getenv('APEX_IMPORT_PASS') or os.getenv('ORACLE_DB_PASS'))
    cur = conn.cursor()
    o = cur.var(str, 65_000_000)
    cur.execute(
        "DECLARE l apex_t_export_files; BEGIN l := apex_export.get_application(p_application_id => :app); :o := l(1).contents; END;",
        app=APP_ID, o=o,
    )
    texto = o.getvalue()
    baseline_path = None
    cur.close()
    conn.close()
    return texto, baseline_path


def main() -> None:
    texto, baseline_path = export_vivo()
    print(f"[marca] export OK ({len(texto):,} chars)")
    orig = texto

    # ── 1) marca ──
    texto = texto.replace("prompt APPLICATION 215 - Pueblos con Vida", "prompt APPLICATION 215 - MadridNext")
    texto = texto.replace("--   Name:            Pueblos con Vida", "--   Name:            MadridNext")
    texto = texto.replace(
        ",p_name=>nvl(wwv_flow_application_install.get_application_name,'Pueblos con Vida')",
        ",p_name=>nvl(wwv_flow_application_install.get_application_name,'MadridNext')")
    texto = texto.replace(",p_logo_text=>'Pueblos con Vida'", ",p_logo_text=>'MadridNext'")
    texto = texto.replace(",p_substitution_value_01=>'Pueblos con Vida'", ",p_substitution_value_01=>'MadridNext'")
    texto = texto.replace("<h1>Pueblos con Vida</h1>", "<h1>MadridNext</h1>")
    restos = len(re.findall(r"Pueblos con Vida", texto))
    print(f"[marca] restos 'Pueblos con Vida' tras reemplazo: {restos}")

    # ── 2) nav-blanco en 10/40/50 (ya tienen la regla del logo) ──
    nav_nl = "\n".join("'" + esc(l) + "'," for l in BLOQUE_NAV_BLANCO)
    pat_logol = re.compile(r"('[^\n]*?\.t-Header \.a-Logo:hover\{color:#5eead4!important\}',)")
    def sub_nav(m):
        if "li.is-selected{" in texto[m.end(): m.end() + 60]:
            return m.group(1)
        return m.group(1) + "\n" + nav_nl
    texto = pat_logol.sub(sub_nav, texto)
    n_rp = texto.count(".a-TreeView li.is-selected>.a-TreeView-label,")
    print(f"[marca] nav-blanco insertado en {n_rp} regiones (10/40/50)")

    # ── 3) cabecera aqua en 1/20/30 ──
    n_ins = 0
    for pg, (encontrados, reemplazo) in CERRADURAS.items():
        i = texto.index(f"--application/pages/{pg}")
        cand = [texto.find(t, i) for t in (
            "--application/pages/page_00020", "--application/pages/page_00030",
            "--application/pages/page_00040", "--application/pages/page_00050",
            "--application/shared_components",)]
        cand = [j for j in cand if j > i]
        fin = min(cand)
        bloque = texto[i:fin]
        # comprobamos que la cerradura tal cual está presente (una vez)
        # ancla = la ÚLTIMA cerradura dentro del bloque de la página
        #   (los </script> intermedios de cada script fuente no cuentan)
        i_an = bloque.rfind(encontrados[0])
        if i_an < 0:
            print(f"[marca] AVISO {pg}: cerradura ausente; se omite")
            continue
        bloque_nuevo = bloque[:i_an] + reemplazo + bloque[i_an + len(encontrados[0]):]
        texto = texto[:i] + bloque_nuevo + texto[fin:]
        n_ins += 1
    print(f"[marca] cabecera aqua insertada en {n_ins}/3 páginas")

    if texto == orig:
        raise SystemExit("[marca] sin cambios en el export; abortando")

    if "--dump" in sys.argv:
        Path(r"C:\Users\juan\AppData\Local\Temp\opencode\export_mutado.sql").write_text(texto, encoding="utf-8")
        print(f"[marca] dump escrito (mutado {len(texto):,} chars)")
        return

    # ── reimport ──
    texto = re.sub(r"p_default_workspace_id=>\d+", "p_default_workspace_id=>NULL", texto, count=1)
    from mcp.importar_export import sentencias
    chunks = sentencias(texto)

    adm = conectar()
    with adm.cursor() as c:
        try:
            c.execute(f"BEGIN apex_instance_admin.remove_application({APP_ID}); END;")
            print(f"[marca] app {APP_ID} previa eliminada")
        except Exception as e:
            print(f"[marca] remove: {str(e)[:90]}")
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
            print(f"[marca] FALLO sentencia #{idx}: {str(e)[:300]}")
            print("\n".join(cbody.splitlines()[:8]))
            raise SystemExit(1)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[marca] {n} sentencias OK — marca y estilo aplicados")


if __name__ == "__main__":
    main()
