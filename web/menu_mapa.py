"""Helper de mutación del export para la entrada de menú 'Mapa'.

La entrada 'p_list_item_link_text=>'Mapa'' puede existir en el export en dos
listas distintas:
  - `navigation_bar` (la lista de arriba-derecha: usuario/logout) — sitio
    ERRÓNEO donde la insertó el ancla antigua, y por eso nunca se veía en el
    lateral.
  - `navigation_menu` (menu lateral compartido por las páginas) — sitio
    CORRECTO (secuencia 30: Inicio, Simulador, Mapa, Datos).
Este módulo provee `coloca_entrada_mapa(texto)`:
  1) borra la entrada de la barra si está ahí,
  2) la inserta en el Navigation Menu si no está ya (idempotente).
"""

from __future__ import annotations

ITEM_MAPA = ("wwv_flow_imp_shared.create_list_item(\n"
             " p_id=>wwv_flow_imp.id(8900550584000023)\n"
             ",p_list_item_display_sequence=>30\n"
             ",p_list_item_link_text=>'Mapa'\n"
             ",p_static_id=>'mapa'\n"
             ",p_list_item_link_target=>'f?p=&APP_ID.:40:&APP_SESSION.::&DEBUG.:::'\n"
             ",p_list_item_icon=>'fa-map'\n"
             ",p_list_item_current_type=>'TARGET_PAGE'\n"
             ");\n")


def coloca_entrada_mapa(texto: str) -> tuple[str, str]:
    """Sanea la colocación de la entrada 'Mapa'. Devuelve (texto, detalle).

    `detalle` resume lo Hecho: 'nada', 'quitada de la barra' o
    'quitada de la barra + insertada en Navigation Menu', etc.
    """
    # 1) líneas / sección en curso
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
            if any("p_list_item_link_text=>'Mapa'" in b for b in bloque):
                quitadas += 1
                i = j + 1
                continue
        out.append(ln)
        i += 1
    texto = "\n".join(out) + ("\n" if ls else "")

    # 2) ¿ya está en el Navigation Menu? (section: lists/navigation_menu)
    #    Buscamos el create_list correcto y su cierre; entre create_list y su
    #    primer create_list_item delante está bien; usamos un corte de sección:
    pos_menu = texto.index("p_name=>'Navigation Menu'")
    pos_sig = texto.find("--application/", pos_menu)
    rango = texto[pos_menu:pos_sig if pos_sig != -1 else len(texto)]
    esta_en_menu = "p_list_item_link_text=>'Mapa'" in rango

    detalle = []
    if quitadas:
        detalle.append(f"quitada de la barra ({quitadas})")
    if not esta_en_menu:
        i_m = texto.index("p_name=>'Navigation Menu'")
        i_fin = texto.index("\n);\n", i_m) + len("\n);\n")
        texto = texto[:i_fin] + ITEM_MAPA + texto[i_fin:]
        detalle.append("insertada en Navigation Menu (secuencia 30, icono fa-map)")
    if not detalle:
        detalle.append("nada")
    return texto, " + ".join(detalle)
