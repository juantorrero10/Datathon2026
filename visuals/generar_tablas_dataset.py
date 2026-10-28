"""Tablas del dataset para la presentación (NIVEL descriptivo, sin algoritmos).

Genera 4 PNG en visuals/ (solo imágenes):

    14_inventario_variables_panel.png      28 variables del panel, agrupadas en 7 bloques
    15_inventario_variables_municipios.png 27 variables estáticas de la hoja Municipios
    16_matriz_correlacion.png              Spearman 18 variables clave (corte 2023, n=155)
                                           + Top 10 pares con mayor |rho|
    17_calidad_y_normalizacion.png         Nulos, huecos por año, rango 2025 y transformación
                                           aplicada en el pipeline, para las 55 variables

Decisiones declaradas:
  * Bloques (7): amplia la taxonomía nativa del Diccionario (VIV/DEM/SRV/EMP/AMB) separando
    SRV en Sanidad / Educación / Transporte y conectividad. Empleo se mantiene (paro).
  * Correlaciones: Spearman (monótona, robusta a la cola de población), corte transversal
    2023 (n=155, última cohorte completa del índice) y NO panel apilado.
  * Heatmap = 14 features de M4 en crudo + edad_media, EUR/vivienda, densidad y área.

Solo lectura del resto del repositorio. Ejecutar: python scripts/generar_tablas_dataset.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import generar_ejemplos_visuales as gv  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

DIR_SALIDA = gv.DIR_SALIDA

BLOQUES = ["Demografía", "Sanidad", "Educación", "Vivienda", "Transporte y conectividad", "Empleo", "Territorio y ambiente"]
BLOCK_COLORS = {
    "Demografía": "#4C78A8",
    "Sanidad": "#E45756",
    "Educación": "#54A24B",
    "Vivienda": "#F58518",
    "Transporte y conectividad": "#B279A2",
    "Empleo": "#EDC948",
    "Territorio y ambiente": "#9D755D",
}


def texto_banda(color: str) -> str:
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    return "#222222" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "white"


def fmt_num(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    a = abs(v)
    if a >= 1e6:
        s = f"{v / 1e6:.1f}M"
    elif a >= 1e5:
        s = f"{v / 1e3:.0f}k"
    elif a >= 1e4:
        s = f"{v / 1e3:.1f}k"
    elif a >= 100:
        s = f"{v:.0f}"
    elif a >= 10:
        s = f"{v:.1f}"
    else:
        s = f"{v:.2f}"
    return s.replace(".", ",")


def comprimir_anios(anios) -> str:
    anios = sorted(set(int(a) for a in anios))
    grupos, ini, prev = [], anios[0], anios[0]
    for a in anios[1:]:
        if a == prev + 1:
            prev = a
            continue
        grupos.append((ini, prev))
        ini = prev = a
    grupos.append((ini, prev))
    return " · ".join(f"{a}" if a == b else f"{a}-{str(b)[2:]}" for a, b in grupos)


def render_tabla(ax, header, filas, col_x, fontsize=7.2, row_h=None):
    """filas: lista de ("banda", texto, color) | ("fila", [celdas]). col_x: fracciones (n+1)."""
    n = len(filas) + 1
    row_h = row_h or 1 / (n + 0.5)
    top = 1.0
    # header
    y = top - row_h * 0.9
    ax.add_patch(plt.Rectangle((0, y - row_h * 0.5), 1, row_h, fc="#2f3b4c", ec="none"))
    for i, h in enumerate(header):
        ax.text(col_x[i] + 0.006, y, h, fontsize=fontsize + 0.4, fontweight="bold",
                color="white", va="center", ha="left")
    y_act = y - row_h
    zebra = False
    for kind, *rest in filas:
        if kind == "banda":
            texto, color = rest
            ax.add_patch(plt.Rectangle((0, y_act - row_h * 0.5), 1, row_h, fc=color, ec="none"))
            ax.text(0.006, y_act, texto.upper(), fontsize=fontsize + 0.2, fontweight="bold",
                    color=texto_banda(color), va="center")
            zebra = False
        else:
            celdas = rest[0]
            if zebra:
                ax.add_patch(plt.Rectangle((0, y_act - row_h * 0.5), 1, row_h, fc="#eef1f5", ec="none"))
            for i, celda in enumerate(celdas):
                mono = i == 0
                ax.text(col_x[i] + 0.006, y_act, celda, fontsize=fontsize - (0.3 if mono else 0),
                        va="center", ha="left", family="Consolas" if mono else None, color="#222222")
            zebra = not zebra
        y_act -= row_h
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


# ─────────────────────────────────────────────────────────────────────────────
# Definición de variables (bloque, descripción, unidad, fuente, uso)
# ─────────────────────────────────────────────────────────────────────────────

PANEL_DEF = {
    # variable: (bloque, descripción, unidad, fuente, uso)
    "poblacion_total": ("Demografía", "Población total empadronada", "habitantes", "INE/IEM", "M3 · M4 · índice"),
    "poblacion_hombres": ("Demografía", "Población de hombres", "habitantes", "INE/IEM", "contexto"),
    "poblacion_mujeres": ("Demografía", "Población de mujeres", "habitantes", "INE/IEM", "contexto"),
    "densidad_hab_km2": ("Demografía", "Habitantes por km²", "hab/km²", "INE/IEM", "contexto"),
    "crecimiento_relativo_poblacion": ("Demografía", "Variación relativa anual de población", "%", "INE/IEM", "contexto (M3 usa su propio CAGR)"),
    "edad_media": ("Demografía", "Edad media de la población", "años", "INE/IEM", "M3"),
    "proporcion_dependencia": ("Demografía", "Dependencia (IEM)", "ratio", "INE/IEM", "contexto"),
    "proporcion_reemplazamiento": ("Demografía", "Recambio generacional (IEM)", "ratio", "INE/IEM", "M3 · M4 · índice"),
    "razon_progresividad": ("Demografía", "Jóvenes frente a adultos (IEM)", "ratio", "INE/IEM", "contexto"),
    "tasa_feminidad": ("Demografía", "Mujeres por 100 hombres", "ratio", "INE/IEM", "contexto"),
    "tasa_fecundidad": ("Demografía", "Fecundidad (IEM)", "tasa", "INE/IEM", "contexto"),
    "tasa_migracion": ("Demografía", "Tasa de migración total", "tasa", "INE/IEM", "M3 (media 3 años)"),
    "tasa_migracion_extranjero": ("Demografía", "Migración con el extranjero", "tasa", "INE/IEM", "contexto"),
    "tasa_migracion_ccaa": ("Demografía", "Migración con otras CCAA", "tasa", "INE/IEM", "contexto"),
    "pct_poblacion_menor_15": ("Demografía", "% de población menor de 15 años", "%", "INE/IEM", "M3 · M4 · índice"),
    "pct_poblacion_65_mas": ("Demografía", "% de población de 65+ años", "%", "INE/IEM", "M3 · M4 · índice"),
    "paro_registrado_total": ("Empleo", "Paro registrado total", "personas", "IEM/CM", "contexto"),
    "paro_por_100_hab": ("Empleo", "Paro registrado por 100 habitantes", "paros/100 hab", "IEM/CM", "M3 · M4 · índice"),
    "variacion_relativa_paro": ("Empleo", "Variación relativa del paro", "%", "IEM/CM", "M3 · M4 · índice"),
    "centros_de_salud": ("Sanidad", "Centros de salud", "centros", "IEM/CM", "M4 · índice"),
    "consultorios_locales": ("Sanidad", "Consultorios locales", "consultorios", "IEM/CM", "M4 · índice"),
    "paradas_autobus": ("Transporte y conectividad", "Paradas de autobús", "paradas", "IEM/CM", "M4 · índice"),
    "estaciones_metro": ("Transporte y conectividad", "Estaciones de metro", "estaciones", "IEM/CM", "M4 · índice"),
    "estaciones_cercanias": ("Transporte y conectividad", "Estaciones de cercanías", "estaciones", "IEM/CM", "M4 · índice"),
    "lineas_telefonicas_baf": ("Transporte y conectividad", "Líneas telefónicas de banda ancha fija", "líneas", "IEM/CM", "M4 · índice"),
    "lineas_telefonicas_atf": ("Transporte y conectividad", "Líneas telefónicas ATF", "líneas", "IEM/CM", "M4 · índice"),
    "unidades_urbanas_residencial": ("Vivienda", "Viviendas catastrales de uso residencial", "unidades", "Catastro·CM", "M4 · índice"),
    "valor_catastral_residencial_miles_eur": ("Vivienda", "Valor catastral residencial total", "miles EUR", "Catastro·CM", "descriptiva (fig. 12-13)"),
}

MUN_DEF = {
    "poblacion_1ene_2025": ("Demografía", "Población a 1 de enero de 2025", "habitantes", "INE", "contexto"),
    "area_km2": ("Territorio y ambiente", "Superficie del término municipal", "km²", "IGN", "contexto"),
    "centroide_lat": ("Territorio y ambiente", "Latitud del centroide", "grados", "IGN", "mapas"),
    "centroide_lon": ("Territorio y ambiente", "Longitud del centroide", "grados", "IGN", "mapas"),
    "distancia_centro_km": ("Territorio y ambiente", "Km a la Puerta del Sol", "km", "IGN (calc.)", "M3 · M4 · índice"),
    "paradas_interurbano": ("Transporte y conectividad", "Paradas de interurbanos (CRTM)", "paradas", "CRTM", "insumo de tiempos"),
    "lineas_interurbano": ("Transporte y conectividad", "Líneas de interurbanos", "líneas", "CRTM", "contexto"),
    "viajes_interurbano": ("Transporte y conectividad", "Viajes/día de interurbanos", "viajes", "CRTM", "contexto"),
    "tiempo_centro_interurbano_min": ("Transporte y conectividad", "Min a Madrid en interurbano", "min", "CRTM", "insumo de tiempo_centro_min"),
    "paradas_cercanias": ("Transporte y conectividad", "Paradas de cercanías", "paradas", "CRTM", "insumo"),
    "lineas_cercanias": ("Transporte y conectividad", "Líneas de cercanías", "líneas", "CRTM", "contexto"),
    "viajes_cercanias": ("Transporte y conectividad", "Viajes/día de cercanías", "viajes", "CRTM", "contexto"),
    "tiempo_centro_cercanias_min": ("Transporte y conectividad", "Min a Madrid en cercanías", "min", "CRTM", "insumo"),
    "paradas_metro": ("Transporte y conectividad", "Paradas de metro", "paradas", "CRTM", "insumo"),
    "lineas_metro": ("Transporte y conectividad", "Líneas de metro", "líneas", "CRTM", "contexto"),
    "viajes_metro": ("Transporte y conectividad", "Viajes/día de metro", "viajes", "CRTM", "contexto"),
    "tiempo_centro_metro_min": ("Transporte y conectividad", "Min a Madrid en metro", "min", "CRTM", "insumo"),
    "paradas_metro_ligero": ("Transporte y conectividad", "Paradas de metro ligero", "paradas", "CRTM", "insumo"),
    "lineas_metro_ligero": ("Transporte y conectividad", "Líneas de metro ligero", "líneas", "CRTM", "contexto"),
    "viajes_metro_ligero": ("Transporte y conectividad", "Viajes/día de metro ligero", "viajes", "CRTM", "contexto"),
    "tiempo_centro_metro_ligero_min": ("Transporte y conectividad", "Min a Madrid en metro ligero", "min", "CRTM", "insumo"),
    "tiempo_centro_min": ("Transporte y conectividad", "Min a Madrid en el modo más rápido", "min", "CRTM", "M3 · M4 · índice"),
    "modo_mas_rapido": ("Transporte y conectividad", "Modo de transporte más rápido", "modo", "CRTM", "contexto"),
    "modos_con_parada": ("Transporte y conectividad", "Nº de modos con parada en el municipio", "nº", "CRTM", "contexto"),
    "paradas_total": ("Transporte y conectividad", "Paradas de transporte totales", "paradas", "CRTM", "contexto"),
    "centros_educativos_alta": ("Educación", "Centros educativos en funcionamiento", "centros", "CM·Educación", "M4 · índice"),
    "estaciones_calidad_aire": ("Territorio y ambiente", "Estaciones de calidad del aire", "estaciones", "CM·Aire", "contexto"),
}

TRANSFORMACION = {
    "poblacion_total": "log (M3/M4) + denominador per cápita",
    "poblacion_hombres": "sin transformar",
    "poblacion_mujeres": "sin transformar",
    "densidad_hab_km2": "sin transformar",
    "crecimiento_relativo_poblacion": "derivada: CAGR propio en M3",
    "edad_media": "sin transformar",
    "proporcion_dependencia": "sin transformar",
    "proporcion_reemplazamiento": "sin transformar (target: percent-rank)",
    "razon_progresividad": "sin transformar",
    "tasa_feminidad": "sin transformar",
    "tasa_fecundidad": "sin transformar",
    "tasa_migracion": "media móvil 3 años (M3)",
    "tasa_migracion_extranjero": "sin transformar",
    "tasa_migracion_ccaa": "sin transformar",
    "pct_poblacion_menor_15": "sin transformar (target: percent-rank)",
    "pct_poblacion_65_mas": "sin transformar (target: percent-rank)",
    "paro_registrado_total": "contexto",
    "paro_por_100_hab": "sin transformar (target: percent-rank)",
    "variacion_relativa_paro": "sin transformar (target: percent-rank)",
    "centros_de_salud": "per 10.000 hab (salud_10k)",
    "consultorios_locales": "per 10.000 hab (salud_10k)",
    "paradas_autobus": "per 1.000 hab (paradas_1000)",
    "estaciones_metro": "per 1.000 hab (paradas_1000)",
    "estaciones_cercanias": "per 1.000 hab (paradas_1000)",
    "lineas_telefonicas_baf": "per 1.000 hab (telefono_1000)",
    "lineas_telefonicas_atf": "per 1.000 hab (telefono_1000)",
    "unidades_urbanas_residencial": "per 1.000 hab (viv_1000)",
    "valor_catastral_residencial_miles_eur": "EUR/vivienda (capa descriptiva)",
    "poblacion_1ene_2025": "sin transformar",
    "area_km2": "sin transformar",
    "centroide_lat": "sin transformar",
    "centroide_lon": "sin transformar",
    "distancia_centro_km": "sin transformar",
    "paradas_interurbano": "insumo de tiempos y paradas",
    "lineas_interurbano": "sin transformar",
    "viajes_interurbano": "sin transformar",
    "tiempo_centro_interurbano_min": "candidato a tiempo_centro_min",
    "paradas_cercanias": "insumo",
    "lineas_cercanias": "sin transformar",
    "viajes_cercanias": "sin transformar",
    "tiempo_centro_cercanias_min": "candidato a tiempo_centro_min",
    "paradas_metro": "insumo",
    "lineas_metro": "sin transformar",
    "viajes_metro": "sin transformar",
    "tiempo_centro_metro_min": "candidato a tiempo_centro_min",
    "paradas_metro_ligero": "insumo",
    "lineas_metro_ligero": "sin transformar",
    "viajes_metro_ligero": "sin transformar",
    "tiempo_centro_metro_ligero_min": "candidato a tiempo_centro_min",
    "tiempo_centro_min": "imputación lineal en 99 pueblos",
    "modo_mas_rapido": "sin transformar",
    "modos_con_parada": "sin transformar",
    "paradas_total": "sin transformar",
    "centros_educativos_alta": "per 1.000 hab (escuelas_1000)",
    "estaciones_calidad_aire": "sin transformar",
}


def filas_inventario(df_datos: pd.DataFrame, defs: dict, estatico: bool) -> list:
    filas = []
    for bloque in BLOQUES:
        vars_bloque = [v for v, d in defs.items() if d[0] == bloque]
        if not vars_bloque:
            continue
        filas.append(("banda", f"{bloque}  ({len(vars_bloque)} variables)", BLOCK_COLORS[bloque]))
        for v in vars_bloque:
            _, desc, unidad, fuente, uso = defs[v]
            if estatico:
                anios = "estático (2025)"
            else:
                anios = comprimir_anios(df_datos.loc[df_datos[v].notna(), "anio"].unique())
            filas.append(("fila", [v, desc, unidad, fuente, anios, uso]))
    return filas


def fig14_15_inventarios(panel: pd.DataFrame, mun: pd.DataFrame):
    COLS = ["Variable", "Descripción", "Unidad", "Fuente", "Años disponibles", "¿Dónde se usa?"]
    COL_X = [0.0, 0.185, 0.55, 0.665, 0.755, 0.885, 1.0]

    for num, nombre, df_datos, defs, estatico in [
        (14, "14_inventario_variables_panel.png", panel, PANEL_DEF, False),
        (15, "15_inventario_variables_municipios.png", mun, MUN_DEF, True),
    ]:
        titulo = ("Inventario de variables · Panel 2010-2025" if num == 14
                  else "Inventario de variables · Municipios, estáticas")
        filas = filas_inventario(df_datos, defs, estatico)
        fig, ax = plt.subplots(figsize=(16.5, 10.8), constrained_layout=True)
        render_tabla(ax, COLS, filas, COL_X, fontsize=7.4)
        n_vars = len(defs)
        fig.suptitle(f"{titulo} ({n_vars} variables en 7 bloques)", fontsize=13.5, fontweight="bold")
        gv.footer(fig, gv.FOOTER_BASE +
                  " · «Años disponibles» calculado sobre los nulos reales del dataset · "
                  "«¿Dónde se usa?»: features de M3/M4, percent-ranks del índice SQL o contexto · "
                  "bloques = taxonomía declarada en el script (amplía el bloque VIV/DEM/SRV/EMP/AMB del Diccionario)")
        fig.savefig(DIR_SALIDA / f"{num:02d}_inventario_variables_{'panel' if num == 14 else 'municipios'}.png")
        plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 16 · Correlaciones
# ─────────────────────────────────────────────────────────────────────────────

HEAT_BLOQUES = [
    ("Demografía", ["log_pob", "crec_10y", "pct<15", "pct65+", "reempl", "edad_med", "densidad"]),
    ("Sanidad", ["salud_10k"]),
    ("Educación", ["escuelas"]),
    ("Vivienda", ["viv_1000", "eur_viv"]),
    ("Transporte y conectividad", ["paradas", "telf_1000", "t_centro", "dist_km"]),
    ("Empleo", ["paro_100", "var_paro"]),
    ("Territorio y ambiente", ["area_km2"]),
]
ABREV = {"Demografía": "DEM", "Sanidad": "SAN", "Educación": "EDU", "Vivienda": "VIV",
         "Transporte y conectividad": "TRA", "Empleo": "EMP", "Territorio y ambiente": "TERR"}
HEAT_VARS = [v for _, vs in HEAT_BLOQUES for v in vs]
VAR_BLOQUE = {v: b for b, vs in HEAT_BLOQUES for v in vs}


def matriz_correlacion(data: pd.DataFrame, panel: pd.DataFrame, mun: pd.DataFrame) -> pd.DataFrame:
    """18 variables en el corte 2023 (n=155)."""
    corte = data[data["anio"] == 2023].set_index("cod_ine")
    p23 = panel[panel["anio"] == 2023].set_index("cod_ine")
    X = pd.DataFrame(index=corte.index)
    X["log_pob"] = corte["log_pob"]
    X["crec_10y"] = corte["crec_10y_pct"]
    X["pct<15"] = corte["pct_menor_15"]
    X["pct65+"] = corte["pct_65mas"]
    X["reempl"] = corte["reemplazamiento"]
    X["edad_med"] = p23["edad_media"]
    X["densidad"] = p23["densidad_hab_km2"]
    X["salud_10k"] = corte["salud_10k"]
    X["escuelas"] = corte["escuelas_1000"]
    X["viv_1000"] = corte["viv_1000"]
    X["eur_viv"] = p23["valor_catastral_residencial_miles_eur"] * 1000 / p23["unidades_urbanas_residencial"]
    X["paradas"] = corte["paradas_1000"]
    X["telf_1000"] = corte["telefono_1000"]
    X["t_centro"] = corte["tiempo_centro_min"]
    X["dist_km"] = corte["distancia_sol_km"]
    X["paro_100"] = corte["paro_100"]
    X["var_paro"] = corte["var_paro"]
    X["area_km2"] = mun.set_index("cod_ine")["area_km2"]
    return X[HEAT_VARS]


def fig16_correlacion(X: pd.DataFrame):
    corr = X.corr(method="spearman")
    n = len(HEAT_VARS)

    fig = plt.figure(figsize=(17, 10.6), constrained_layout=True)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.9, 1])
    ax = fig.add_subplot(gs[0, 0])
    axp = fig.add_subplot(gs[0, 1])

    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(n), HEAT_VARS, rotation=45, ha="right", fontsize=7.5, family="Consolas")
    ax.set_yticks(range(n), HEAT_VARS, fontsize=7.5, family="Consolas")
    for i in range(n):
        for j in range(n):
            v = corr.values[i, j]
            ax.text(j, i, f"{v:.2f}".replace("0.", ".").replace("-0", "-"), ha="center", va="center",
                    fontsize=6.1, color="white" if abs(v) > 0.55 else "#222222")
    # franjas de bloque + separadores
    pos = 0
    for bloque, vars_b in HEAT_BLOQUES:
        color = BLOCK_COLORS[bloque]
        ax.add_patch(plt.Rectangle((-1.6, pos - 0.5), 1.4, len(vars_b), fc=color, ec="white", clip_on=False))
        ax.text(-0.9, pos + len(vars_b) / 2 - 0.5, ABREV[bloque],
                rotation=90, ha="center", va="center", fontsize=7.2, fontweight="bold",
                color=gvTextoBanda(color))
        pos += len(vars_b)
        if pos < n:
            ax.axhline(pos - 0.5, color="#333333", lw=1.2)
            ax.axvline(pos - 0.5, color="#333333", lw=1.2)
    cb = plt.colorbar(im, ax=ax, shrink=0.75, pad=0.02)
    cb.set_label("Spearman ρ", fontsize=9)
    ax.set_title("Spearman ρ · corte 2023, n=155 municipios (variables agrupadas por bloque)",
                 fontsize=11, fontweight="bold", pad=26)

    # Top 10 pares |rho|
    pares = []
    for i in range(n):
        for j in range(i + 1, n):
            pares.append((HEAT_VARS[i], HEAT_VARS[j], corr.values[i, j]))
    pares.sort(key=lambda t: -abs(t[2]))
    axp.axis("off")
    axp.set_title("Las 10 relaciones más fuertes (|ρ|)", fontsize=11, fontweight="bold", pad=10)
    filas = []
    for a, b, r in pares[:10]:
        filas.append(("fila", [f"{a}  ↔  {b}", f"{r:+.2f}".replace(".", ","),
                               f"{VAR_BLOQUE[a].split()[0]} ↔ {VAR_BLOQUE[b].split()[0]}"]))
    render_tabla(axp, ["Par de variables", "ρ", "Bloques"], filas,
                 [0.0, 0.62, 0.78, 1.0], fontsize=8.0, row_h=1 / 11)
    axp.text(0, 0.02, "Misma zona del heatmap = variables del mismo bloque; el orden del heatmap\n"
                      "hace visible qué bloques se mueven juntos (p.ej. tamaño ↔ vivienda).",
             fontsize=8, color="#555555", va="bottom")

    fig.suptitle("¿Qué variables se mueven juntas? Correlaciones Spearman entre variables clave",
                 fontsize=13.5, fontweight="bold")
    gv.footer(fig, gv.FOOTER_BASE +
              " · corte transversal 2023 (última cohorte completa, n=155); NO panel apilado · "
              "Spearman por rangos, robusto a la cola de población · las 14 features de M4 en crudo "
              "+ edad media, EUR/vivienda catastral, densidad y área")
    fig.savefig(DIR_SALIDA / "16_matriz_correlacion.png")
    plt.close(fig)


def gvTextoBanda(color: str) -> str:
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    return "#222222" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "white"


# ─────────────────────────────────────────────────────────────────────────────
# 17 · Calidad: nulos, huecos, rango y normalización
# ─────────────────────────────────────────────────────────────────────────────

def fig17_calidad(panel: pd.DataFrame, mun: pd.DataFrame):
    panel_vars = [v for v in PANEL_DEF]
    mun_vars = [v for v in MUN_DEF]

    def filas(df_datos, defs, estatico):
        filas = []
        for bloque in BLOQUES:
            vars_bloque = [v for v, d in defs.items() if d[0] == bloque]
            if not vars_bloque:
                continue
            filas.append(("banda", f"{bloque}  ({len(vars_bloque)})", BLOCK_COLORS[bloque]))
            for v in vars_bloque:
                serie = df_datos[v]
                nulos = int(serie.isna().sum())
                pct = 100 * (1 - nulos / len(serie))
                if estatico:
                    huecos = "—" if nulos == 0 else f"{nulos} sin dato"
                else:
                    anios_hueco = sorted(set(df_datos["anio"]) - set(df_datos.loc[serie.notna(), "anio"]))
                    huecos = comprimir_anios(anios_hueco) if anios_hueco else "ninguno"
                ref = serie.dropna()
                if pd.api.types.is_numeric_dtype(ref):
                    rango = f"{fmt_num(ref.min())} · {fmt_num(ref.median())} · {fmt_num(ref.max())}"
                else:
                    top = ref.value_counts().index[0] if len(ref) else "—"
                    rango = f"categórica ({top})"
                filas.append(("fila", [v, str(nulos), f"{pct:.0f}%", huecos, rango, TRANSFORMACION[v]]))
        return filas

    COLS = ["Variable", "Nulos", "%compl.", "Años con hueco", "Rango 2025 (min · med · max)", "Transformación en el pipeline"]
    COL_X = [0.0, 0.20, 0.245, 0.30, 0.435, 0.66, 1.0]

    fig, axes = plt.subplots(1, 2, figsize=(20, 12.5), constrained_layout=True)
    render_tabla(axes[0], COLS, filas(panel, PANEL_DEF, False), COL_X, fontsize=6.9)
    render_tabla(axes[1], COLS, filas(mun, MUN_DEF, True), COL_X, fontsize=6.9)
    axes[0].set_title("Panel 2010-2025 · 28 variables (2.480 filas municipio-año)", fontsize=10.5, fontweight="bold", pad=8)
    axes[1].set_title("Municipios · estáticos · 27 variables (155 filas)", fontsize=10.5, fontweight="bold", pad=8)
    fig.suptitle("Control de nulos y normalización · 55 variables del dataset", fontsize=13.5, fontweight="bold")
    gv.footer(fig, gv.FOOTER_BASE +
              " · nulos contados sobre 2.480 filas (panel) y 155 filas (estáticos) · huecos del panel: telefonía "
              "2010-11, sanidad 2014 y 2025, transporte 2024-25, migración 2022-25 → por eso el corte del índice "
              "es 2023 · «Rango 2025» usa el último dato no nulo de cada variable · transformaciones = las que "
              "aplican los pipelines M3/M4 y el índice SQL")
    fig.savefig(DIR_SALIDA / "17_calidad_y_normalizacion.png")
    plt.close(fig)


def main():
    DIR_SALIDA.mkdir(exist_ok=True)
    print("[1/4] Cargando dataset...")
    panel = gv.cargar_panel()
    mun = gv.cargar_municipios()

    print("[2/4] Figuras 14 y 15: inventarios de variables...")
    fig14_15_inventarios(panel, mun)

    print("[3/4] Figura 16: matriz de correlación (corte 2023)...")
    _, _, data, _, _, _ = gv.preparar_datos()
    X = matriz_correlacion(data, panel, mun)
    fig16_correlacion(X)

    print("[4/4] Figura 17: calidad de datos y normalización...")
    fig17_calidad(panel, mun)

    print("\n=== RESUMEN ===")
    nulos_resumen = panel[panel["anio"] == 2023].isna().sum()
    print(f"Corte 2023: nulos por variable > 0: {dict(nulos_resumen[nulos_resumen > 0])}" if (nulos_resumen > 0).any()
          else "Corte 2023: sin nulos en las 28 variables del panel (cohorte completa) ✓")
    print("Figuras generadas:")
    for f in sorted(DIR_SALIDA.glob("1[4567]_*.png")):
        print("  ·", f.name)


if __name__ == "__main__":
    main()
