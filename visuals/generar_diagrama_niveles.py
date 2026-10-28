"""Diagramas «Executive Slate» (Concepto A): arquitectura por niveles, flujo vertical.

    22_diagrama_niveles.png        Detallado: 4 bandas (N0 DATOS → N1 PYTHON → N2 ORACLE → N3 APEX+USUARIO)
    23_diagrama_niveles_simple.png Simple: 5 niveles, una tarjeta por nivel

Disciplina visual: un solo acento (azul #1e40af), tarjetas blancas con borde fino,
chips de tecnología en mono, ámbar reservado exclusivamente al tag «en desarrollo».

Solo lectura del resto del repositorio. Ejecutar: python scripts/generar_diagrama_niveles.py
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
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

DIR_SALIDA = REPO / "visuals"

ACCENT = "#1e40af"
INK = "#0f172a"
BODY = "#334155"
BORDE = "#cbd5e1"
GRIS = "#64748b"
AMBAR = "#b45309"


def banda(ax, y0, y1, tint, chip_texto):
    ax.add_patch(FancyBboxPatch((1, y0), 98, y1 - y0,
                                boxstyle="round,pad=0.1,rounding_size=1.6",
                                fc=tint, ec="none", zorder=1))
    ax.add_patch(FancyBboxPatch((2.6, (y0 + y1) / 2 - 2.0), 15.5, 4.0,
                                boxstyle="round,pad=0.1,rounding_size=0.9",
                                fc=ACCENT, ec="none", zorder=3))
    ax.text(10.35, (y0 + y1) / 2, chip_texto, ha="center", va="center",
            fontsize=8.6, fontweight="bold", color="white", zorder=4)


def tarjeta(ax, cx, cy, w, h, num, titulo, lineas, tech):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.1,rounding_size=0.9",
                                fc="white", ec=BORDE, lw=1.4, zorder=3))
    ax.add_patch(FancyBboxPatch((cx - w / 2 + 1.6, cy + h / 2 - 4.0), 2.9, 2.9,
                                boxstyle="round,pad=0.08,rounding_size=0.55",
                                fc=ACCENT, ec="none", zorder=4))
    ax.text(cx - w / 2 + 3.05, cy + h / 2 - 2.55, num, ha="center", va="center",
            fontsize=9.4, fontweight="bold", color="white", zorder=5)
    ax.text(cx - w / 2 + 5.4, cy + h / 2 - 2.55, titulo, ha="left", va="center",
            fontsize=10.6, fontweight="bold", color=INK, zorder=5)
    yy = cy + h / 2 - 6.6
    for linea in lineas:
        ax.text(cx, yy, linea, ha="center", va="center", fontsize=8.4, color=BODY, zorder=5)
        yy -= 2.5
    ax.text(cx, yy - 0.1, tech, ha="center", va="center", fontsize=7.3,
            family="Consolas", color=ACCENT, zorder=5)


def flecha_v(ax, x, y0, y1, etiqueta=None):
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="-|>",
                                 mutation_scale=15, lw=2.0, color=ACCENT, zorder=5))
    if etiqueta:
        ax.text(x + 1.2, (y0 + y1) / 2, etiqueta, ha="left", va="center",
                fontsize=7.4, color=GRIS, style="italic", zorder=5)


def flecha_h(ax, x0, x1, y):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>",
                                 mutation_scale=15, lw=2.0, color=ACCENT, zorder=5))


# ═══════════════════════════════════════════════════════════════════════════
# 22 · Detallado: 4 bandas × 2 tarjetas, flujo vertical
# ═══════════════════════════════════════════════════════════════════════════

def diagrama_niveles():
    fig, ax = plt.subplots(figsize=(15.8, 12.6), constrained_layout=True)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    bandas = [
        (75.0, 98.5, "#f8fafc", "N0 · DATOS"),
        (50.0, 73.5, "#eff6ff", "N1 · PYTHON"),
        (25.0, 48.5, "#fffbeb", "N2 · ORACLE 23ai"),
        (0.5, 23.5, "#f0fdf4", "N3 · APEX + USUARIO"),
    ]
    for y0, y1, tint, chip in bandas:
        banda(ax, y0, y1, tint, chip)

    cy = {k: (y0 + y1) / 2 for k, (y0, y1, _, _) in zip([4, 3, 2, 1], reversed(bandas))}
    cy1, cy2, cy3, cy4 = cy[1], cy[2], cy[3], cy[4]

    # Banda 1 (N0): ① izquierda → ② derecha
    tarjeta(ax, 38, cy1, 36, 15.0, "01", "FUENTES",
            ["INE · IEM/CM · Catastro", "CRTM · IGN · 2010-2025"], "5 fuentes públicas")
    tarjeta(ax, 80, cy1, 36, 15.0, "02", "DATASET",
            ["dataset_155_municipios.xlsx", "55 variables · 155 pueblos · 16 años"], "pandas · openpyxl")
    flecha_h(ax, 56.8, 61.2, cy1)

    # Banda 2 (N1): ③ derecha → ④ izquierda
    tarjeta(ax, 38, cy2, 36, 15.0, "04", "EXPORT ONNX",
            ["6 ficheros: m3 + m4 × 5 dims", "validación ONNX↔sklearn < 1e-5"], "onnx · onnxruntime")
    tarjeta(ax, 80, cy2, 36, 15.0, "03", "ENTRENAMIENTO · N1",
            ["features M3 (16) y M4 (14)", "fichas JSON · semilla 2026"], "scikit-learn · skl2onnx")
    flecha_h(ax, 61.2, 56.8, cy2)

    # Banda 3 (N2): ⑤ izquierda → ⑥ derecha
    tarjeta(ax, 38, cy3, 36, 15.0, "05", "ORACLE 23ai",
            ["LOAD_ONNX_MODEL + tablas PV_*", "PREDICTION() en SQL"], "el modelo vive en la base")
    tarjeta(ax, 80, cy3, 36, 15.0, "06", "PV_SIMULA_PKG",
            ["M3 → choque → ratios → M4", "índice + factor limitante"], "PL/SQL · JSON efímero")
    flecha_h(ax, 56.8, 61.2, cy3)

    # Banda 4 (N3): ⑦ derecha → ⑧ izquierda
    tarjeta(ax, 38, cy4, 36, 15.0, "08", "USUARIO",
            ["ciudadano y gestor", "descarga de resultados", "*comparador de municipios: EN DESARROLLO"], "consumidor del simulador")
    tarjeta(ax, 80, cy4, 36, 15.0, "07", "APEX · N3 (app 215)",
            ["formulario → AJAX «SIMULAR»", "barras · semáforo · descarga JSON/CSV"], "APEX 215 · JavaScript")
    flecha_h(ax, 61.2, 56.8, cy4)

    # Conectores verticales entre bandas
    flecha_v(ax, 80, 75.0, 73.5, "dataset listo")
    flecha_v(ax, 38, 50.0, 48.5, "carga de modelos")
    flecha_v(ax, 80, 25.0, 23.5, "apex.server.process «SIMULAR» → CLOB JSON")

    fig.suptitle("Pueblos con vida · Arquitectura por niveles", fontsize=15.5,
                 fontweight="bold", color=INK)
    ax.text(1, -0.7, "Flujo vertical: los datos oficiales entran por arriba (N0) y la decisión sale por abajo (N3)   ·   "
                     "etiqueta ámbar = en desarrollo   ·   la simulación es efímera: nada se persiste   ·   28-10-2026",
            fontsize=7.9, color="#666666", ha="left")
    fig.savefig(DIR_SALIDA / "22_diagrama_niveles.png")
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════
# 23 · Simple: 5 niveles, una tarjeta por nivel
# ═══════════════════════════════════════════════════════════════════════════

def diagrama_niveles_simple():
    fig, ax = plt.subplots(figsize=(15, 12.8), constrained_layout=True)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    niveles = [
        (79.0, 98.0, "#f8fafc", "N0 · DATOS", "01", "FUENTES",
         "INE · IEM/CM · Catastro · CRTM · IGN · series 2010-2025", "5 fuentes públicas"),
        (59.5, 77.5, "#eff6ff", "N1 · PYTHON", "02", "PYTHON · N1",
         "ingesta y limpieza · entrenamiento M3 + M4 · export ONNX", "scikit-learn · skl2onnx"),
        (40.0, 58.0, "#fffbeb", "N2 · ORACLE 23ai", "03", "ORACLE 23ai",
         "carga de los 6 modelos · PREDICTION() en SQL", "el modelo vive en la base"),
        (20.5, 38.5, "#fffbeb", "N2 · SERVICIOS", "04", "PV_SIMULA_PKG",
         "escenario what-if · índice + factor limitante · JSON antes/después", "PL/SQL · efímero"),
        (1.0, 19.0, "#f0fdf4", "N3 · APEX", "05", "APEX · N3 (app 215)",
         "barras · semáforo · mapa · descarga JSON/CSV · ciudadano y gestor", "APEX 215 · JavaScript"),
    ]
    centros = []
    for y0, y1, tint, chip, num, titulo, linea, tech in niveles:
        banda(ax, y0, y1, tint, chip)
        cy = (y0 + y1) / 2
        centros.append(cy)
        tarjeta(ax, 57, cy, 66, 13.2, num, titulo, [linea], tech)

    for i in range(4):
        flecha_v(ax, 57, centros[i] - 6.9, centros[i + 1] + 6.9)

    fig.suptitle("Pueblos con vida · Arquitectura por niveles (visión general)",
                 fontsize=15, fontweight="bold", color=INK)
    ax.text(1, -0.7, "Versión detallada: visuals/22_diagrama_niveles.png   ·   los datos entran por arriba (N0), "
                     "la decisión sale por abajo (N3)   ·   28-10-2026",
            fontsize=7.9, color="#666666", ha="left")
    fig.savefig(DIR_SALIDA / "23_diagrama_niveles_simple.png")
    plt.close(fig)


if __name__ == "__main__":
    DIR_SALIDA.mkdir(exist_ok=True)
    diagrama_niveles()
    diagrama_niveles_simple()
    print("OK ->", DIR_SALIDA / "22_diagrama_niveles.png")
    print("OK ->", DIR_SALIDA / "23_diagrama_niveles_simple.png")
