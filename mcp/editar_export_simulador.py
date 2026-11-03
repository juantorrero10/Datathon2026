"""Genera oracle_db/backups/simulador.sql a partir de oracle_db/backups/sql_original.sql.

Operaciones sobre el texto del export, cada una con marcador único:
  1. workspace id del import: 9407325500210183 -> 9407325500210184 (el real).
  2. Página 10 'Perfil Institucional' -> 'Simulador What-If' (nombre + título),
     front nuevo (overlay+blur hasta simular; resultado solo del JSON) y
     proceso SIMULAR re-emitido con 7 parámetros.
  3. Página 20 'Perfil Ciudadano' -> 'Perfil Ciudadano (retirada)' y región
     reducida a un cartel con enlace a la página 10.
  4. Menú: entrada 'Perfil Institucional' -> 'Simulador What-If'; se elimina
     la entrada 'Perfil Ciudadano'.
  5. Portada (pág. 1): enlaces f?p=&APP_ID.:20: -> :10: si existen.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from mcp.editar_export_contenido import FRONT, SIMULAR_SRC, STUB20_LINES  # noqa: E402

DIR_EXP = REPO / "oracle_db" / "backups"
ORIG = DIR_EXP / "sql_original.sql"
DEST = DIR_EXP / "simulador.sql"


def esc(l: str) -> str:
    return l.replace("'", "''")


def attr_clob_region(lines: list[str]) -> str:
    """Atributo p_plug_source en formato export.

    runtime = `BEGIN HTP.P(q'~<line1>\\n<line2>\\n...\\n<lineN>~'); END;`
    con cada línea como elemento del array (join añade el salto de línea).
    """
    out = [",p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2("]
    out.append("'" + esc("BEGIN HTP.P(q'~" + lines[0]) + "',")
    for line in lines[1:-1]:
        out.append("'" + esc(line) + "',")
    out.append("'" + esc(lines[-1]) + "~''); END;'")
    out.append("))")
    return "\n".join(out)


def attr_process_clob(lines: list[str]) -> str:
    out = [",p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2("]
    for line in lines[:-1]:
        out.append("'" + esc(line) + "',")
    out.append("'" + esc(lines[-1]) + "'")
    out.append("))")
    return "\n".join(out)


def reemplazar_bloque(texto: str, ancla: str, ini_key: str, fin_key: str, nuevo: str) -> str:
    """Sustituye el rango de LÍNEAS [ini_key, fin_key) localizado tras `ancla`."""
    i_ancla = texto.index(ancla)
    i_ini = texto.index(ini_key, i_ancla)
    i_ini = texto.rfind("\n", 0, i_ini) + 1
    i_fin = texto.index(fin_key, i_ini)
    i_fin = texto.rfind("\n", 0, i_fin) + 1
    return texto[:i_ini] + nuevo + "\n" + texto[i_fin:]


def main() -> None:
    text = ORIG.read_text(encoding="utf-8")
    done = []

    # 1) workspace id real
    assert text.count("9407325500210183") == 1, "workspace id no es única"
    text = text.replace("9407325500210183", "9407325500210184")
    done.append("workspace id -> 9407325500210184")

    # 2) página 10
    assert text.count("p_name=>'Perfil Institucional'") == 1
    text = text.replace("p_name=>'Perfil Institucional'", "p_name=>'Simulador What-If'")
    text = text.replace("p_step_title=>'Perfil Institucional'", "p_step_title=>'Simulador What-If'")
    done.append("página 10 renombrada")

    text = reemplazar_bloque(
        text, "p_static_id=>'dashboard-institucional'",
        ",p_plug_source=>", ",p_plug_source_type=>",
        attr_clob_region(FRONT.splitlines()),
    )
    done.append("front nuevo pág. 10")

    text = reemplazar_bloque(
        text, "p_process_name=>'SIMULAR'",
        ",p_process_sql_clob=>", ",p_process_clob_language=>",
        attr_process_clob(SIMULAR_SRC),
    )
    done.append("proceso SIMULAR (7 params)")

    # 3) página 20
    assert text.count("p_name=>'Perfil Ciudadano'") == 1
    text = text.replace("p_name=>'Perfil Ciudadano'", "p_name=>'Perfil Ciudadano (retirada)'")
    text = text.replace("p_step_title=>'Perfil Ciudadano'", "p_step_title=>'Perfil Ciudadano (retirada)'")
    text = reemplazar_bloque(
        text, "p_static_id=>'dashboard-ciudadano'",
        ",p_plug_source=>", ",p_plug_source_type=>",
        attr_clob_region(STUB20_LINES),
    )
    done.append("página 20 -> cartel de retirada")

    # 4) menú
    assert text.count("p_list_item_link_text=>'Perfil Institucional'") == 1
    text = text.replace("p_list_item_link_text=>'Perfil Institucional'",
                        "p_list_item_link_text=>'Simulador What-If'")
    done.append("menú: entrada renombrada a Simulador What-If")

    # entrada 'Perfil Ciudadano' del menú: borrado por LÍNEAS
    ls = text.splitlines(keepends=False)
    out, i, n = [], 0, len(ls)
    borradas = 0
    while i < n:
        if "wwv_flow_imp_shared.create_list_item(" in ls[i]:
            j = i
            while j < n and not ls[j].rstrip().endswith(");"):
                j += 1
            bloque = ls[i : j + 1]
            if any("'Perfil Ciudadano'" in b for b in bloque):
                borradas += len(bloque)
                i = j + 1
                continue
        out.append(ls[i])
        i += 1
    text = "\n".join(out) + "\n"
    if borradas:
        done.append(f"menú: entrada 'Perfil Ciudadano' eliminada ({borradas} líneas)")

    # 5) portada
    n_enlaces = text.count("f?p=&APP_ID.:20:")
    if n_enlaces:
        text = text.replace("f?p=&APP_ID.:20:", "f?p=&APP_ID.:10:")
        done.append(f"portada: {n_enlaces} enlace(s) reenrutados a la pág. 10")

    # verificaciones de integridad
    #    (codificado en el export para que SOBREVIVA a los reimports: los cambios
    #    hechos a mano en el builder se pierden con cada reinstalación).
    assert text.count("p_plug_name=>'Dashboard institucional'") == 1
    text = text.replace("p_plug_name=>'Dashboard institucional'", "p_plug_name=>'Simulador What-If'")
    i_ancla = text.index("p_static_id=>'dashboard-institucional'")
    i_t = text.index(",p_plug_template=>4073835273271169698", i_ancla)
    text = text[:i_t] + ",p_plug_template=>4502917002193490937" + text[i_t + len(",p_plug_template=>4073835273271169698"):]
    done.append("región pág. 10: 'Simulador What-If' + plantilla Blank with Attributes")

    # verificaciones de integridad
    assert "Perfil Institucional" not in text, "quedan restos de 'Perfil Institucional'"
    assert text.count("'Simulador What-If'") == 4, "renombres no son 4"
    assert "p_name=>'Perfil Ciudadano (retirada)'" in text
    assert "WKSP_DATATHON.PV_SIMULA(" in text and "g_x07" in text
    assert "g_x07" in text

    DEST.write_text(text, encoding="utf-8")
    print(f"[export] ORIG={len(ORIG.read_text(encoding='utf-8')):,} -> MUTADO={len(text):,} chars")
    for d in done:
        print("[export]   ok,", d)


if __name__ == "__main__":
    main()
