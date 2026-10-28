"""Genera web/front_simulador.py a partir del front ACTUAL de la pág. 10.

Fuentes, por orden:  1) fichero dado como argumento (export .sql);
                     2) export vivo de la app 215 (si la app existe).

IMPORTANTE — des-escape del export: en el export, el source vive dentro de
literales SQL y TODAS las comillas simples van DOBLADAS ('' = '). Extrarlo
tal cual rompe el JS (SyntaxError: tokens inválidos). Aquí se des-escapa SIEMPRE
y front_simulador.py contiene el texto EJECUTABLE (comillas simples).
Al reinstalar, actualizar_front_simulador.py re-escapa con esc().

Parche AUTO-JUGADA: si sessionStorage trae 'pvWiJugada' ({cod, anio}; lo
guarda el Mapa al pinchar un municipio), la pág. 10 preselecciona el
municipio (tras rellenar el select con DATOS) y ejecuta la FASE 1
(SIMULAR con sliders a 0). La clave se limpia después.
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

OUT = REPO / "web" / "front_simulador.py"

# ── parches sobre el JS de la región (todo sobre texto DES-ESCAPADO) ──
ANCLA_DATOS = r'''   $("swCod").innerHTML=m.map(function(x){return "<option value=\""+esc(x.cod)+"\">"+esc(x.nombre)+"</option>";}).join("");'''
AUTO = [
    '   var pre=null;try{pre=JSON.parse(sessionStorage.getItem(\'pvWiJugada\')||"null");}catch(e){pre=null;}',
    '   if(pre&&pre.cod){var sel=$("swCod");var hay=false;Array.prototype.forEach.call(sel.options,function(o){if(o.value===String(pre.cod))hay=true;});',
    '    if(hay){sel.value=String(pre.cod);$("swAnio").value=String(pre.anio||"2030");sessionStorage.removeItem(\'pvWiJugada\');run();}else{sessionStorage.removeItem(\'pvWiJugada\');}}',
]


def export_vivo() -> str:
    conn = conectar()
    cur = conn.cursor()
    o = cur.var(str, 65_000_000)
    cur.execute(
        "DECLARE l apex_t_export_files; BEGIN l := apex_export.get_application(p_application_id => 215); :o := l(1).contents; END;",
        o=o,
    )
    texto = o.getvalue()
    conn.close()
    return texto


def elems_del_array(cuerpo: str) -> list[str]:
    """Parsea los elementos '...' del array SQL (escapes '' -> '). Devuelve el
    contenido REAL de cada elemento (puede ser trozo de línea si fue partida).

    Scan con conciencia de comillas: cada elemento va entre comillas simples
    y separado por comas/espacios/nuevas líneas; dentro del elemento, dos
    comillas seguidas significan UNA comilla."
    """
    elems: list[str] = []
    i, n = 0, len(cuerpo)
    while i < n:
        while i < n and (cuerpo[i] in " \t\r\n," or cuerpo[i] == "/"):
            i += 1
        if i >= n:
            break
        if cuerpo[i] != "'":
            # contenido fuera de comillas (fino): avanzamos
            i += 1
            continue
        i += 1
        buf: list[str] = []
        while i < n:
            c = cuerpo[i]
            if c == "'":
                if i + 1 < n and cuerpo[i + 1] == "'":
                    buf.append("'")
                    i += 2
                    continue
                i += 1
                break
            buf.append(c)
            i += 1
        elems.append("".join(buf))
    return elems


def region_source_raw(texto: str) -> str:
    """Saca el source de la región de la pág. 10 DES-ESCAPADO del export.

    Soporta las dos formas del export:
      - array:  p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(...))
      - clob:   p_plug_source=>'BEGIN HTP.P(...'
    """
    i_a = texto.index("p_plug_name=>'Simulador What-If'")
    i_ini = texto.index(",p_plug_source=>", i_a)
    i_fin = texto.index(",p_plug_source_type=>", i_ini)
    bloque = texto[i_ini:i_fin]

    # 1) formato array: wwv_flow_string.join(wwv_flow_t_varchar2(...))
    #    OJO: apex_export parte los elementos largos a ~250 chars — un elemento
    #    puede ser un trozo MEDIO de una línea; hay que ensamblar por CHUNKS y
    #    no tratar cada elemento como una línea (bug que rompió el JS del WI).
    m_join = re.search(r"wwv_flow_string\.join\(wwv_flow_t_varchar2\((.*?)\)\)\s*$", bloque, re.S)
    if m_join:
        cuerpo = m_join.group(1)
        elems = elems_del_array(cuerpo)
        # sentido del corte: un elemento de longitud == CHUNK es la cabeza de
        # una línea partida; el siguiente elemento la continúa. Elemento corto
        # = fin natural de línea del source.
        chunk = max(len(e) for e in elems) if elems else 0
        lineas: list[str] = []
        buffer = ""
        for e in elems:
            buffer += e
            if len(e) < chunk:
                lineas.append(buffer)
                buffer = ""
        if buffer:
            lineas.append(buffer)
        return "\n".join(lineas)

    # 2) formato clob: p_plug_source=>'...' (multilínea, dobladas)
    m_clob = re.search(r",p_plug_source=>'(.*?)',\s*\n", bloque, re.S)
    if m_clob:
        return m_clob.group(1).replace("''", "'")

    raise ValueError("formato de p_plug_source no reconocido")


def main() -> None:
    if len(sys.argv) > 1:
        texto = Path(sys.argv[1]).read_text(encoding="utf-8")
        print(f"[front] fuente: fichero {sys.argv[1]}")
    else:
        texto = export_vivo()
        print(f"[front] fuente: export vivo ({len(texto):,} chars)")

    fuente = region_source_raw(texto)

    # las dos cadenas q'~...~' del source EJECUTABLE
    mq = "q'~"
    q1 = fuente.index(mq) + len(mq)
    q1e = fuente.index("~'", q1)
    cabecera = fuente[q1:q1e]
    q2 = fuente.index(mq, q1e) + len(mq)
    q2e = fuente.index("~'", q2)
    front_ej = fuente[q2:q2e]
    print(f"[front] cabecera={len(cabecera):,} chars | front={len(front_ej):,} chars")

    # sanitidad: el front des-escapado NO debe contener dobles apostrofes
    for nombre, s in (("CABECERA", cabecera), ("FRONT", front_ej)):
        dobles = s.count("''")
        if dobles:
            print(f"[front] AVISO {nombre}: {dobles} dobles apostrofe(s) residuales")

    # parche (textura: la ancla debe existir EXACTAMENTE una vez)
    assert front_ej.count(ANCLA_DATOS) == 1, "ancla DATOS no es única"
    parche = ANCLA_DATOS + "\n" + "\n".join(AUTO)
    front = front_ej.replace(ANCLA_DATOS, parche, 1)
    print("[front] parche de auto-jugada aplicado (pvWiJugada)")

    # el literal no puede contener el delimitador """
    for s, n in (("CABECERA", cabecera), ("FRONT", front)):
        assert s.count('"""') == 0, f"{s} contiene \"\"\""

    OUT.write_text(
        '"""Front de la página 10 — Simulador What-If (dos fases).\n\n'
        'Texto EJECUTABLE (comillas simples; el export las dobla — este fichero\n'
        'hace el des-escape). Canonizado del estado vivo (menú de descarga/import\n'
        'incluido) + parche AUTO-JUGADA desde el Mapa: si sessionStorage trae\n'
        '"pvWiJugada" ({cod, anio}), la pág. 10 preselecciona el municipio (tras\n'
        'rellenar el select con DATOS) y ejecuta la FASE 1 (SIMULAR con sliders\n'
        'a 0) sin interacción. La clave se limpia después (refresh no re-juega).\n\n'
        'CABECERA_SIM -> primer HTP.P (estilos .t-Header del Simulador)\n'
        'FRONT_SIM    -> segundo HTP.P (CSS + HTML + JS del Simulador)\n'
        'Aplicar con: python web/actualizar_front_simulador.py\n'
        '"""\n\n'
        'from pathlib import Path\n\n'
        f'CABECERA_SIM = r"""{cabecera}"""\n\n'
        f'FRONT_SIM = r"""{front}"""\n'
        f'# (referencia para herramientas futuras)\n'
        'LIMITE_PATH = Path(__file__).resolve().parents[1] / "web" / "limite_madrid.json"\n',
        encoding="utf-8",
    )
    print(f"[front] escrito {OUT}")


if __name__ == "__main__":
    main()
