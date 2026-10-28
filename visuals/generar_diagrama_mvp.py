"""Diagramas estilo «MVP Pipeline» (Concepto B): timeline con círculos numerados,
carriles BUILD ONCE / RUN EVERY TIME, acento único indigo/teal, chips de tecnología.

    20_diagrama_mvp_pipeline.png   Detallado: 8 etapas en 2 carriles
    21_diagrama_mvp_simple.png     Simple: 5 etapas en una línea

Solo lectura del resto del repositorio. Ejecutar: python scripts/generar_diagrama_mvp.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch  # noqa: E402

DIR_SALIDA = REPO / "visuals"

INK = "#0f172a"
GRIS = "#64748b"
BORDE = "#e2e8f0"
INDIGO = "#4f46e5"
INDIGO_BANDA = "#eef2ff"
TEAL = "#0d9488"
TEAL_BANDA = "#ecfdf5"
AMBAR = "#b45309"


def tarjeta(ax, x, y_arriba, w, h, titulo, lineas, tech, acento):
    """Tarjeta blanca con sombra suave; y_arriba = borde superior."""
    y = y_arriba - h
    ax.add_patch(FancyBboxPatch((x - w / 2 + 0.55, y - 0.55), w, h,
                                boxstyle="round,pad=0.12,rounding_size=0.7",
                                fc="#0f172a", ec="none", alpha=0.07, zorder=2))
    ax.add_patch(FancyBboxPatch((x - w / 2, y), w, h,
                                boxstyle="round,pad=0.12,rounding_size=0.7",
                                fc="white", ec=BORDE, lw=1.3, zorder=3))
    ax.add_patch(plt.Rectangle((x - w / 2, y + h - 0.55), 0.28, 0.55, fc=acento, ec="none", zorder=4))
    yy = y + h - 2.1
    ax.text(x, yy, titulo, ha="center", va="center", fontsize=10.3,
            fontweight="bold", color=INK, zorder=5)
    yy -= 2.2
    for linea in lineas:
        ax.text(x, yy, linea, ha="center", va="center", fontsize=8.2, color="#334155", zorder=5)
        yy -= 1.95
    ax.text(x, yy - 0.15, tech, ha="center", va="center", fontsize=7.1,
            family="Consolas", color=acento, zorder=5)


def linea_progreso(ax, xs, y, acento, numeros, doble=False):
    ax.plot([xs[0], xs[-1]], [y, y], color=acento, lw=2.4, zorder=2, solid_capstyle="round")
    for i, x in enumerate(xs):
        ax.add_patch(Circle((x, y), 2.35, fc=acento, ec="white", lw=2.2, zorder=4))
        ax.text(x, y, numeros[i], ha="center", va="center", fontsize=9.6,
                fontweight="bold", color="white", zorder=5)
        if i < len(xs) - 1:
            ax.add_patch(FancyArrowPatch((x + 2.6, y), (xs[i + 1] - 2.6, y),
                                         arrowstyle="<|-|>" if doble else "-|>",
                                         mutation_scale=13, lw=1.8, color=acento, zorder=3))


def chip(ax, x, y, texto, color):
    ax.add_patch(FancyBboxPatch((x - len(texto) * 0.62 - 1, y - 1.35), len(texto) * 1.24 + 2, 2.7,
                                boxstyle="round,pad=0.1,rounding_size=1.2",
                                fc=color, ec="none", zorder=4))
    ax.text(x, y, texto, ha="center", va="center", fontsize=9.2,
            fontweight="bold", color="white", zorder=5)


# ═══════════════════════════════════════════════════════════════════════════
# 20 · Detallado: 8 etapas, 2 carriles
# ═══════════════════════════════════════════════════════════════════════════

def diagrama_mvp_pipeline():
    fig, ax = plt.subplots(figsize=(18, 10.4), constrained_layout=True)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 58)
    ax.axis("off")

    xs = [11, 37, 63, 89]

    # Carril BUILD ONCE
    ax.add_patch(FancyBboxPatch((0.8, 29.5), 98.4, 26.5,
                                boxstyle="round,pad=0.1,rounding_size=1.4",
                                fc=INDIGO_BANDA, ec="none", zorder=1))
    chip(ax, 2.2 + 5.5, 52.6, "BUILD ONCE", INDIGO)
    ax.text(97.2, 52.6, "se ejecuta una vez", ha="right", va="center",
            fontsize=8.5, color=GRIS, style="italic", zorder=4)
    linea_progreso(ax, xs, 46.5, INDIGO, ["01", "02", "03", "04"])
    tarjetas1 = [
        ("FUENTES", ["INE · IEM/CM · Catastro", "CRTM · IGN · 2010-2025"], "5 fuentes públicas"),
        ("DATASET", ["dataset_155_municipios.xlsx", "55 variables · 155 pueblos · 16 años"], "pandas · openpyxl"),
        ("ENTRENAMIENTO N1", ["features M3 (16) y M4 (14)", "fichas JSON · semilla 2026"], "scikit-learn · skl2onnx"),
        ("EXPORT ONNX", ["6 ficheros: m3 + m4 × 5 dims", "validación ONNX↔sklearn < 1e-5"], "onnx · onnxruntime"),
    ]
    for x, (t, ls, tech) in zip(xs, tarjetas1):
        tarjeta(ax, x, 43.0, 21.5, 11.8, t, ls, tech, INDIGO)

    # Conector 04 → 05
    ax.add_patch(FancyArrowPatch((89, 44.0), (89, 19.4), arrowstyle="-|>",
                                 mutation_scale=16, lw=2.4, color="#334155", zorder=5))
    ax.text(96.4, 31.7, "carga de modelos", ha="center", va="center", rotation=90,
            fontsize=7.6, color="#334155", style="italic", zorder=5,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.85))

    # Carril RUN EVERY TIME
    ax.add_patch(FancyBboxPatch((0.8, 1.5), 98.4, 26.0,
                                boxstyle="round,pad=0.1,rounding_size=1.4",
                                fc=TEAL_BANDA, ec="none", zorder=1))
    chip(ax, 2.2 + 6.9, 24.7, "RUN EVERY TIME", TEAL)
    ax.text(97.2, 24.7, "en cada pulsación de «Simular»", ha="right", va="center",
            fontsize=8.5, color=GRIS, style="italic", zorder=4)
    linea_progreso(ax, xs, 17.0, TEAL, ["05", "06", "07", "08"], doble=True)
    tarjetas2 = [
        ("ORACLE 23ai", ["LOAD_ONNX_MODEL + tablas PV_*", "PREDICTION() en SQL"], "el modelo vive en la base"),
        ("PV_SIMULA_PKG", ["M3 → choque → ratios → M4", "índice + factor limitante"], "PL/SQL · JSON efímero"),
        ("APEX · N3 (app 215)", ["formulario → AJAX «SIMULAR»", "barras · semáforo · descarga JSON/CSV"], "APEX 215 · JavaScript"),
        ("USUARIO", ["ciudadano y gestor", "descarga de resultados"], "comparador: EN DESARROLLO"),
    ]
    for x, (t, ls, tech) in zip(xs, tarjetas2):
        color_tech = AMBAR if "DESARROLLO" in tech else TEAL
        tarjeta(ax, x, 15.6, 21.5, 11.3, t, ls, tech, color_tech)

    fig.suptitle("Pueblos con vida · Arquitectura del MVP", fontsize=15.5, fontweight="bold", color=INK)
    ax.text(1, -0.6, "BUILD ONCE = entrenamiento y export de los 6 modelos ONNX   ·   RUN EVERY TIME = llamada API en tiempo real "
                     "(APEX → PV_SIMULA_PKG → PREDICTION(), respuesta JSON efímera)   ·   28-10-2026",
            fontsize=7.8, color="#666666", ha="left")
    fig.savefig(DIR_SALIDA / "20_diagrama_mvp_pipeline.png")
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════
# 21 · Simple: 5 etapas en una línea
# ═══════════════════════════════════════════════════════════════════════════

def diagrama_mvp_simple():
    fig, ax = plt.subplots(figsize=(18, 6.6), constrained_layout=True)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 31)
    ax.axis("off")

    xs = [10, 30, 50, 70, 90]

    linea_progreso(ax, xs, 21.5, INDIGO, ["01", "02", "03", "04", "05"])
    tarjetas = [
        ("FUENTES", ["INE · IEM/CM · Catastro", "CRTM · IGN · 2010-2025"], "5 fuentes públicas"),
        ("PYTHON · N1", ["features M3 + M4 · entrenamiento", "export ONNX"], "scikit-learn · skl2onnx"),
        ("ORACLE 23ai · N2", ["carga de los 6 modelos", "PREDICTION() en SQL"], "el modelo vive en la base"),
        ("PV_SIMULA_PKG", ["escenario what-if", "JSON antes/después"], "PL/SQL · efímero"),
        ("APEX · N3", ["barras · semáforo · mapa", "ciudadano y gestor"], "APEX 215 · JS"),
    ]
    for x, (t, ls, tech) in zip(xs, tarjetas):
        tarjeta(ax, x, 16.2, 17.8, 11.6, t, ls, tech, INDIGO)

    chip(ax, 20, 27.6, "BUILD ONCE", INDIGO)
    chip(ax, 70, 27.6, "RUN EVERY TIME", TEAL)
    ax.plot([40, 40], [15.4, 26.2], color="#cbd5e1", lw=1.4, ls=(0, (4, 3)), zorder=1)

    fig.suptitle("Pueblos con vida · Arquitectura del MVP (visión general)",
                 fontsize=15, fontweight="bold", color=INK)
    ax.text(1, -0.4, "Versión detallada: visuals/20_diagrama_mvp_pipeline.png   ·   28-10-2026",
            fontsize=7.8, color="#666666", ha="left")
    fig.savefig(DIR_SALIDA / "21_diagrama_mvp_simple.png")
    plt.close(fig)


if __name__ == "__main__":
    DIR_SALIDA.mkdir(exist_ok=True)
    diagrama_mvp_pipeline()
    diagrama_mvp_simple()
    print("OK ->", DIR_SALIDA / "20_diagrama_mvp_pipeline.png")
    print("OK ->", DIR_SALIDA / "21_diagrama_mvp_simple.png")
