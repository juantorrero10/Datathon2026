"""Helper de mutación del export para la entrada 'Comparador' (menú lateral).

Idéntico en espíritu a `menu_mapa.py`: quita la entrada de la barra de
navegación si estuviera mal colocada y la inserta en el Navigation Menu
compartido (secuencia 35: Inicio, Simulador, Mapa, Comparador, Datos).
"""

from __future__ import annotations

ITEM_COMPARADOR = ("wwv_flow_imp_shared.create_list_item(\n"
                   " p_id=>wwv_flow_imp.id(8900550584000053)\n"
                   ",p_list_item_display_sequence=>35\n"
                   ",p_list_item_link_text=>'Comparador'\n"
                   ",p_static_id=>'comparador'\n"
                   ",p_list_item_link_target=>'f?p=&APP_ID.:50:&APP_SESSION.::&DEBUG.:::'\n"
                   ",p_list_item_icon=>'fa-balance-scale'\n"
                   ",p_list_item_current_type=>'TARGET_PAGE'\n"
                   ");\n")


def coloca_entrada_comparador(texto: str) -> tuple[str, str]:
    """Coloca la entrada 'Comparador' en su sitio. Devuelve (texto, detalle)."""
    ls = texto.splitlines(keepends=False)
    seccion = None
    out: list[str] = []
    quitadas = 0
    i, n = 0, len(ls)
    while i < n:
        ln = ls[i]
        if ln.startswith("prompt --application/"):
            seccion = ln
        if (seccion is not None and "navigation_bar" in seccion
                and "wwv_flow_imp_shared.create_list_item(" in ln):
            j = i
            while j < n and not ls[j].rstrip().endswith(");"):
                j += 1
            bloque = ls[i:j + 1]
            if any("p_list_item_link_text=>'Comparador'" in b for b in bloque):
                quitadas += 1
                i = j + 1
                continue
        out.append(ln)
        i += 1
    texto = "\n".join(out) + ("\n" if ls else "")

    pos_menu = texto.index("p_name=>'Navigation Menu'")
    pos_sig = texto.find("--application/", pos_menu)
    rango = texto[pos_menu:pos_sig if pos_sig != -1 else len(texto)]
    esta_en_menu = "p_list_item_link_text=>'Comparador'" in rango

    detalle = []
    if quitadas:
        detalle.append(f"quitada de la barra ({quitadas})")
    if not esta_en_menu:
        i_m = texto.index("p_name=>'Navigation Menu'")
        i_fin = texto.index("\n);\n", i_m) + len("\n);\n")
        texto = texto[:i_fin] + ITEM_COMPARADOR + texto[i_fin:]
        detalle.append("insertada en Navigation Menu (secuencia 35, icono fa-balance-scale)")
    if not detalle:
        detalle.append("nada")
    return texto, " + ".join(detalle)
