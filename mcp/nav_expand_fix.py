"""Repara la barra lateral en todas las páginas, línea a línea (idempotente):
  - cierra el `</style>` del bloque aqua donde falte (págs. 1/20/30)
  - garantiza el snippet js-navExpanded en TODAS las páginas
Detecta por estado real de cada región, sin anclas frágiles.

Uso:  python mcp/nav_expand_fix.py
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

SNIPPET_VALUES = (
    '  <script>(function(){var b=document.body;'
    'b&&(b.classList.add("js-navExpanded"),b.classList.remove("js-navCollapsed"));'
    'try{sessionStorage.setItem("ORA_WWV_apex.toggleCore.nav.215.preferenceForExpanded","true")}'
    'catch(e){}})();</script>'
)
SNIPPET_EXPORT = "'" + SNIPPET_VALUES.replace("'", "''") + "',"
STYLE_CLOSE = "'  </style>',"


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
    n_fix = 0

    for num in (1, 10, 20, 30, 40, 50):
        pg = f"page_{num:05d}"
        i = texto.index(f"--application/pages/{pg}")
        cand = [t for t in (texto.find(f"--application/pages/page_{(p):05d}", i) for p in
                            (num + 1, 20, 30, 40, 50, 51)) if t > i]
        cand += [texto.find("--application/shared_components", i),
                 texto.find("--application/deployment", i)]
        fin = min([j for j in cand if j > i])
        bloque = texto[i:fin]

        # localizar el cierre de nuestra zona nav (las 4 líneas del bloque)
        j_k = bloque.find(".t-TreeNav li.is-selected{")
        if j_k < 0:
            print(f"[nav] AVISO {pg}: sin bloque nav; se omite")
            continue
        lineas = bloque.splitlines()
        p_line = None
        for k, l in enumerate(lineas):
            if ".t-TreeNav li.is-selected{" in l:
                p_line = k
                break
        # a partir de ahí: encontrar la línea `' }',` (cierra la última regla)
        k_close = None
        k = p_line
        while k < len(lineas) - 1:
            k += 1
            if lineas[k].strip() in ("}',", "'}',", "}',"):
                k_close = k
                break
        if k_close is None:
            print(f"[nav] AVISO {pg}: no encuentro el cierre de reglas; se omite")
            continue
        # ¿qué sigue al cierre? variantes:
        #   a) '\'  </style>\',\'  </style>~\'\';\'...   (pág. 10: doble cierre)
        #   b) '\'~\');\'...\x27 END;\x27))'              (1/20/30: sin </style>)
        k_resto = k_close + 1
        restos = " ".join(l.strip() for l in lineas[k_resto: k_resto + 8])
        ya_style = "</style>" in restos[:400]
        ya_snippet = "js-navExpanded" in restos[:1200]

        inserciones = []
        if not ya_style:
            # cerrar el style del bloque: insertamos tras la regla de cierre
            inserciones.append(lineas[k_close] + "\n" + STYLE_CLOSE)
            k_resto += 0
        if not ya_snippet:
            if ya_style:
                # el snippet va justo después del primer '</style>' conocido
                for k2 in range(k_close, min(k_close + 12, len(lineas))):
                    if "</style>" in lineas[k2]:
                        lineas.insert(k2, SNIPPET_EXPORT)
                        ya_snippet = True
                        break
            else:
                pass
        # reconstruir
        if not ya_style:
            lineas.insert(k_close + 1, STYLE_CLOSE)
        if not ya_snippet:
            # insertar el snippet después de la línea '</style>' propia o al final del bloque
            pos = k_close + (2 if not ya_style else 1)
            ya2 = False
            for k2 in range(pos, min(pos + 8, len(lineas))):
                if "</style>" in lineas[k2]:
                    lineas.insert(k2, SNIPPET_EXPORT)
                    ya2 = True
                    ya_snippet = True
                    break
            if not ya2:
                lineas.insert(min(pos, len(lineas)), SNIPPET_EXPORT)
                ya_snippet = True
        nuevo_bloque = "\n".join(lineas)
        texto = texto[:i] + nuevo_bloque + texto[fin:]
        ok = "con cierre" if "</style>" in lineas[k_close + 1: k_close + 4] else "sin estilo cerrado"
        n_fix += 1
        print(f"[nav] {pg}: reparado ({ok}, snippet {'sí' if ya_snippet else 'no'})")

    if texto == orig:
        print("[nav] sin cambios")
        return

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
    print(f"[nav] {n} sentencias OK")


if __name__ == "__main__":
    main()
