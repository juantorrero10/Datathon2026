"""Mapa descriptivo del valor catastral residencial (NIVEL 1 · sin algoritmo).

Genera 2 PNG en visuals/ (solo imágenes):

    12_mapa_y_ranking_valor_catastral.png
        Panel A: mapa del valor catastral medio por vivienda, 2025 (EUR).
        Panel B: ranking Top 10 / Bottom 10 de EUR por vivienda (línea = mediana regional).
    13_asequibilidad_vs_vitalidad.png
        Dispersión EUR/vivienda (2025) vs índice de vitalidad real (2023),
        con 4 cuadrantes definidos por las medianas.

Reglas declaradas:
  * valor_catastral_residencial_miles_eur = valor total municipal del stock residencial
    en miles de EUR (Catastro Inmobiliario vía IEM/Comunidad de Madrid). Esta columna está
    completa para los 155 municipios en TODOS los años 2010-2025.
  * valor medio por vivienda = valor total x 1000 / unidades_urbanas_residencial.
  * Es un dato administrativo: NO es precio de mercado y NO es una predicción.
  * El índice de vitalidad usado en el cruce es el real de la cohorte 2023
    (última cohorte completa, igual que las figuras 01-05).

Solo lectura del resto del repositorio. Ejecutar: python scripts/generar_mapa_valor_catastral.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import generar_ejemplos_visuales as gv  # noqa: E402  (estilo y helpers compartidos)
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

DIR_SALIDA = gv.DIR_SALIDA


def cargar_catastro_2025(panel: pd.DataFrame) -> pd.DataFrame:
    """EUR por vivienda y por habitante, corte 2025 (columna completa todos los años)."""
    p25 = panel[panel["anio"] == 2025].set_index("cod_ine")
    d = pd.DataFrame({
        "cod_ine": p25.index,
        "nombre": p25["municipio"].values,
        "poblacion": p25["poblacion_total"].values,
        "eur_vivienda": p25["valor_catastral_residencial_miles_eur"].values * 1000 / p25["unidades_urbanas_residencial"].values,
        "eur_hab": p25["valor_catastral_residencial_miles_eur"].values * 1000 / p25["poblacion_total"].values,
    }).reset_index(drop=True)
    return d


def formato_k(v: float) -> str:
    return f"{v / 1000:.0f} k\u20ac"


def fig12_mapa_y_ranking(cat: pd.DataFrame, showcase: dict, mediana: float):
    fig = plt.figure(figsize=(17, 8.6), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.35, 1, 1])
    ax_map = fig.add_subplot(gs[0, 0])
    ax_top = fig.add_subplot(gs[0, 1])
    ax_bot = fig.add_subplot(gs[0, 2])

    # Panel A: mapa del nivel (barato = verde, caro = rojo; escala p5-p95)
    vmin, vmax = np.quantile(cat["eur_vivienda"], [0.05, 0.95])
    gv.pie_mapa(ax_map, cat, cat["eur_vivienda"],
                "Valor catastral medio por vivienda · 2025",
                cmap="RdYlGn_r", vmin=vmin, vmax=vmax,
                cbar_label="EUR por vivienda (catastral)")
    etiquetas = set(showcase.keys())
    extremos = pd.concat([cat.nlargest(1, "eur_vivienda"), cat.nsmallest(1, "eur_vivienda")])
    for _, fila in extremos.iterrows():
        etiquetas.add(fila["nombre"])
    for nombre in etiquetas:
        try:
            fila = gv.buscar_municipio(cat, nombre)
        except KeyError:
            continue
        ax_map.annotate(nombre, (fila["centroide_lon"], fila["centroide_lat"]),
                        xytext=(0, 9), textcoords="offset points", fontsize=6.4,
                        ha="center", color="#222222",
                        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#999999", alpha=0.75))

    # Paneles B/C: ranking
    for ax, sub, titulo in [
        (ax_top, cat.nlargest(10, "eur_vivienda").iloc[::-1], "Top 10 · más caros (catastral)"),
        (ax_bot, cat.nsmallest(10, "eur_vivienda").iloc[::-1], "Top 10 · más baratos (catastral)"),
    ]:
        ax.barh(sub["nombre"], sub["eur_vivienda"], color="#3b6fb6", height=0.66)
        ax.axvline(mediana, color="#b42318", ls="--", lw=1.1)
        for nombre, v in zip(sub["nombre"], sub["eur_vivienda"]):
            ax.annotate(formato_k(v), (v, nombre), xytext=(4, 0), textcoords="offset points",
                        va="center", fontsize=7.6, color="#333333")
        ax.axvline(mediana, color="#b42318", ls="--", lw=1.1,
                   label=f"mediana regional {formato_k(mediana)}")
        ax.set_title(titulo, fontsize=10.5, fontweight="bold")
        ax.tick_params(axis="y", labelsize=8.5)
        ax.set_xlabel("EUR por vivienda (catastral)", fontsize=9)
        ax.set_xlim(0, sub["eur_vivienda"].max() * 1.22)
        ax.legend(loc="lower right", fontsize=7.6, framealpha=0.95)

    fig.suptitle("Nivel 1 · Valor catastral residencial por vivienda · dato administrativo, NO es precio de mercado ni predicción",
                 fontsize=13, fontweight="bold")
    gv.footer(fig, gv.FOOTER_BASE +
              " · valor = valor_catastral_residencial_miles_eur x 1000 / unidades_urbanas_residencial (columna completa 2010-2025) · "
              "etiquetas: municipios showcase y extremos")
    fig.savefig(DIR_SALIDA / "12_mapa_y_ranking_valor_catastral.png")
    plt.close(fig)


def fig13_asequibilidad(c: pd.DataFrame, cat: pd.DataFrame, showcase: dict):
    d = c.set_index("cod_ine").join(cat.set_index("cod_ine")[["eur_vivienda"]]).reset_index()
    med_x = float(d["eur_vivienda"].median())
    med_y = float(d["indice"].median())

    def cuadrante(fila) -> tuple[str, str]:
        caro = fila["eur_vivienda"] > med_x
        vivo = fila["indice"] > med_y
        if not caro and vivo:
            return "barato_vivo", "barato y vivo"
        if not caro and not vivo:
            return "barato_apagado", "barato y apagado"
        if caro and vivo:
            return "caro_vivo", "caro y vivo"
        return "caro_apagado", "caro y apagado"

    colores = {"barato_vivo": "#54a24b", "barato_apagado": "#9aa5b1",
               "caro_vivo": "#f58518", "caro_apagado": "#b42318"}
    d[["clave", "cuadrante"]] = d.apply(cuadrante, axis=1, result_type="expand")

    fig, ax = plt.subplots(figsize=(13, 8.6), constrained_layout=True)
    for clave, sub in d.groupby("clave"):
        ax.scatter(sub["eur_vivienda"], sub["indice"], s=12 + np.sqrt(sub["poblacion"]) * 0.9,
                   c=colores[clave], alpha=0.85, edgecolor="#333333", linewidth=0.35, zorder=3,
                   label=f"{sub['cuadrante'].iloc[0]} ({len(sub)})")
    ax.axvline(med_x, color="#555555", ls="--", lw=1)
    ax.axhline(med_y, color="#555555", ls="--", lw=1)
    ax.annotate(f"mediana {formato_k(med_x)}", (med_x, ax.get_ylim()[1]), xytext=(5, -14),
                textcoords="offset points", fontsize=8, color="#555555")
    ax.annotate(f"mediana índice {med_y:.1f}", (ax.get_xlim()[0], med_y), xytext=(5, 4),
                textcoords="offset points", fontsize=8, color="#555555")

    # etiquetas: showcase + extremos de precio
    etiquetas = set(showcase.keys())
    extremos = pd.concat([d.nlargest(1, "eur_vivienda"), d.nsmallest(1, "eur_vivienda"),
                          d.nlargest(1, "indice"), d.nsmallest(1, "indice")])
    for _, fila in extremos.iterrows():
        etiquetas.add(fila["nombre"])
    for nombre in etiquetas:
        try:
            fila = gv.buscar_municipio(d, nombre)
        except KeyError:
            continue
        ax.annotate(nombre, (fila["eur_vivienda"], fila["indice"]),
                    xytext=(0, 9), textcoords="offset points", fontsize=6.6, ha="center",
                    color="#222222", bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#999999", alpha=0.75))

    ax.set_xlabel("Valor catastral medio por vivienda, 2025 (EUR)")
    ax.set_ylabel("Índice de vitalidad real, 2023 (0-100)")
    ax.set_title("Asequibilidad vs vitalidad: ¿dónde se puede vivir barato y con vida?",
                 fontsize=13, fontweight="bold", pad=12)
    ax.legend(loc="upper right", fontsize=9, title="cuadrantes (mediana en cada eje)", framealpha=0.95)
    gv.footer(fig, gv.FOOTER_BASE +
              " · x: valor catastral 2025 (dato administrativo, NO precio de mercado ni predicción) · "
              "y: índice real de la cohorte 2023 (última cohorte completa) · tamaño = población · "
              "cuadrantes = medianas de cada eje")
    fig.savefig(DIR_SALIDA / "13_asequibilidad_vs_vitalidad.png")
    plt.close(fig)
    return d


def main():
    DIR_SALIDA.mkdir(exist_ok=True)
    print("[1/4] Cargando dataset, índice real 2023 y valor catastral 2025...")
    panel, mun, data, c, corte, serie = gv.preparar_datos()
    cat = cargar_catastro_2025(panel)
    mediana = float(cat["eur_vivienda"].median())
    print(f"      mediana regional: {formato_k(mediana)} · min {formato_k(cat['eur_vivienda'].min())} "
          f"({cat.loc[cat['eur_vivienda'].idxmin(), 'nombre']}) · max {formato_k(cat['eur_vivienda'].max())} "
          f"({cat.loc[cat['eur_vivienda'].idxmax(), 'nombre']})")

    print("[2/4] Figura 12: mapa del nivel + ranking...")
    mun_coords = mun.set_index("cod_ine")[["centroide_lat", "centroide_lon"]]
    cat = cat.merge(mun_coords, on="cod_ine", how="left")
    showcase = gv.nombres_showcase(c)
    fig12_mapa_y_ranking(cat, showcase, mediana)

    print("[3/4] Figura 13: asequibilidad vs vitalidad...")
    d = fig13_asequibilidad(c, cat, showcase)

    print("[4/4] Resumen:")
    print("Top 5 más caros:", ", ".join(f"{r.nombre} ({formato_k(r.eur_vivienda)})" for r in cat.nlargest(5, 'eur_vivienda').itertuples()))
    print("Top 5 más baratos:", ", ".join(f"{r.nombre} ({formato_k(r.eur_vivienda)})" for r in cat.nsmallest(5, 'eur_vivienda').itertuples()))
    oro = d[(d["clave"] == "barato_vivo")].nlargest(5, "indice")
    print("Zona dorada (barato y vivo), top 5 por índice:",
          ", ".join(f"{r.nombre} ({r.indice:.1f} / {formato_k(r.eur_vivienda)})" for r in oro.itertuples()))
    for f in sorted(DIR_SALIDA.glob("1[23]_*.png")):
        print("  ·", f.name)


if __name__ == "__main__":
    main()
