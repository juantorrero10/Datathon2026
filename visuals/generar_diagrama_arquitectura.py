"""Diagramas de arquitectura de la implementación (2 PNG en visuals/):

    18_diagrama_arquitectura.png   Detallado: 8 etapas en serpentina (construcción + ejecución en vivo)
    19_diagrama_simple.png         Visión general: 5 cajas (estilo minimal)

Decisiones declaradas:
  * Los modelos viven DENTRO de Oracle (PREDICTION() en SQL): no hay servidor externo
    (FastAPI/ngrok del borrador antiguo quedó retirado).
  * La integración con APEX es su capa de servicios nativa: proceso AJAX «SIMULAR»
    → package PL/SQL PV_SIMULA_PKG → CLOB JSON → JavaScript pinta.
  * El comparador de municipios y el mapa están EN DESARROLLO: se etiquetan como tal.

Solo lectura del resto del repositorio. Ejecutar: python scripts/generar_diagrama_arquitectura.py
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

GRIS_TXT = "#374151"
FLECHA = "#374151"


def caja(ax, x, y, w, h, color, titulo, lineas, num=None, dashed=False):
    """Caja redondeada estilo: borde grueso de color, relleno blanco, título en color."""
    box = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                         boxstyle="round,pad=0.15,rounding_size=0.9",
                         fc="white", ec=color, lw=2.8,
                         linestyle=(0, (5, 3)) if dashed else "solid", zorder=3)
    ax.add_patch(box)
    yy = y + h / 2 - 2.6
    ax.text(x, yy, titulo, ha="center", va="center", fontsize=11.5,
            fontweight="bold", color=color, zorder=4)
    yy -= 3.1
    for linea in lineas:
        color_linea = GRIS_TXT
        estilo = "normal"
        if linea.startswith("*"):
            color_linea, linea, estilo = "#b45309", linea[1:].strip(), "italic"
        ax.text(x, yy, linea, ha="center", va="center", fontsize=8.8,
                color=color_linea, zorder=4, fontstyle=estilo)
        yy -= 2.55
    if num is not None:
        ax.text(x - w / 2 + 1.5, y + h / 2 - 1.5, str(num), ha="center", va="center",
                fontsize=9, fontweight="bold", color="white",
                bbox=dict(boxstyle="circle,pad=0.28", fc=color, ec="none"), zorder=5)


def flecha(ax, x0, y0, x1, y1, doble=False, curva=0.0, lw=2.2):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                                 arrowstyle="<|-|>" if doble else "-|>",
                                 mutation_scale=16, lw=lw, color=FLECHA,
                                 connectionstyle=f"arc3,rad={curva}", zorder=2))


def etiqueta(ax, x, y, texto, color=GRIS_TXT, fs=7.8):
    ax.text(x, y, texto, ha="center", va="center", fontsize=fs, color=color,
            style="italic", zorder=4,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9))


# ═══════════════════════════════════════════════════════════════════════════
# 18 · Diagrama detallado (serpentina 2×4)
# ═══════════════════════════════════════════════════════════════════════════

def diagrama_detallado():
    fig, ax = plt.subplots(figsize=(17, 9.2), constrained_layout=True)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 54)
    ax.axis("off")

    W, H = 19.5, 14.5
    xs = [12.5, 37.5, 62.5, 87.5]
    y1, y2 = 38.5, 13.0

    ax.text(2.8, 51.5, "FABRICACIÓN DE LOS MODELOS  ·  se ejecuta una vez", fontsize=9.5,
            fontweight="bold", color="#6b7280", va="center")
    ax.text(2.8, 26.0, "EJECUCIÓN EN VIVO  ·  SIMULADOR  ·  cada pulsación", fontsize=9.5,
            fontweight="bold", color="#6b7280", va="center")

    # Fila 1 (izquierda → derecha)
    caja(ax, xs[0], y1, W, H, "#6b7280", "FUENTES",
         ["INE · IEM/CM · Catastro", "CRTM · IGN", "datos oficiales 2010-2025"], num=1)
    caja(ax, xs[1], y1, W, H, "#0e7490", "DATASET",
         ["dataset_155_municipios", "55 variables · 155 pueblos", "16 años · Diccionario + Fuentes"], num=2)
    caja(ax, xs[2], y1, W, H, "#1d4ed8", "PYTHON · N1",
         ["scikit-learn: features M3 (16)", "y M4 (14) · entrenamiento", "fichas JSON · semilla 2026"], num=3)
    caja(ax, xs[3], y1, W, H, "#7c3aed", "EXPORT ONNX",
         ["6 ficheros: m3_demografia", "+ m4_capacidad × 5 dims", "validación ONNX↔sklearn < 1e-5"], num=4)

    # Fila 2 (derecha → izquierda)
    caja(ax, xs[3], y2, W, H, "#d97706", "ORACLE 23ai · N2",
         ["LOAD_ONNX_MODEL + tablas PV_*", "PREDICTION() en SQL", "el modelo vive en la base"], num=5)
    caja(ax, xs[2], y2, W, H, "#dc2626", "PV_SIMULA_PKG",
         ["M3 → choque → ratios → M4", "índice + factor limitante", "JSON antes/después (efímero)"], num=6)
    caja(ax, xs[1], y2, W, H, "#16a34a", "APEX · N3 (app 215)",
         ["formulario → AJAX «SIMULAR»", "barras + semáforo + mapa", "descarga JSON / CSV"], num=7)
    caja(ax, xs[0], y2, W, H, "#15803d", "USUARIO",
         ["ciudadano y gestor", "descarga de resultados", "*comparador de municipios: en desarrollo"], num=8)

    # Flechas fila 1
    for i in range(3):
        flecha(ax, xs[i] + W / 2 + 0.4, y1, xs[i + 1] - W / 2 - 0.4, y1)
    # Bajada 4 → 5
    flecha(ax, xs[3], y1 - H / 2 - 0.3, xs[3], y2 + H / 2 + 0.3)
    etiqueta(ax, xs[3] + 7.2, (y1 - H / 2 + y2 + H / 2) / 2, "carga de\nmodelos")
    # Flechas fila 2 (izquierda ← derecha): API en tiempo real, doble sentido
    flecha(ax, xs[3] - W / 2 - 0.4, y2, xs[2] + W / 2 + 0.4, y2, doble=True)
    flecha(ax, xs[2] - W / 2 - 0.4, y2, xs[1] + W / 2 + 0.4, y2, doble=True)
    flecha(ax, xs[1] - W / 2 - 0.4, y2, xs[0] + W / 2 + 0.4, y2, doble=True)
    etiqueta(ax, (xs[3] + xs[2]) / 2, y2 - H / 2 - 1.6, "PREDICTION()")
    etiqueta(ax, (xs[2] + xs[1]) / 2, y2 - H / 2 - 1.6, "apex.server.process «SIMULAR» → CLOB JSON")
    etiqueta(ax, (xs[1] + xs[0]) / 2, y2 - H / 2 - 1.6, "render en JavaScript")

    # Nota de desarrollo
    nb = FancyBboxPatch((xs[0] - W / 2 + 0.4, 1.2), W * 2 + 4.0, 3.6,
                        boxstyle="round,pad=0.15,rounding_size=0.8",
                        fc="#fffbeb", ec="#b45309", lw=1.6, linestyle=(0, (5, 3)), zorder=3)
    ax.add_patch(nb)
    ax.text((xs[0] + xs[1]) / 2, 3.0, "EN DESARROLLO: mapa + comparador de municipios\n"
            "(etiquetado honestamente: aún no está en la app)",
            ha="center", va="center", fontsize=8.2, color="#b45309", style="italic", zorder=4)

    fig.suptitle("Pueblos con vida · Arquitectura de la implementación", fontsize=15.5, fontweight="bold")
    ax.text(1, -0.5, "— construcción (flujo continuo)   ↔  llamada API en tiempo real (petición/respuesta JSON, efímera: nada se persiste)   ·   "
                     "Fuente: scripts/generar_diagrama_arquitectura.py · 28-10-2026",
            fontsize=7.8, color="#666666", ha="left")
    fig.savefig(DIR_SALIDA / "18_diagrama_arquitectura.png")
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════
# 19 · Diagrama simple (5 cajas)
# ═══════════════════════════════════════════════════════════════════════════

def diagrama_simple():
    fig, ax = plt.subplots(figsize=(17, 4.4), constrained_layout=True)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 24)
    ax.axis("off")

    W, H = 17.0, 14.0
    xs = [10.8, 30.4, 50.0, 69.6, 89.2]
    y = 12.5

    caja(ax, xs[0], y, W, H, "#6b7280", "FUENTES",
         ["INE · CAM · Catastro", "CRTM · IGN · 2010-2025"])
    caja(ax, xs[1], y, W, H, "#1d4ed8", "PYTHON · N1",
         ["Ingesta, limpieza,", "M3 + M4 · Export ONNX"])
    caja(ax, xs[2], y, W, H, "#d97706", "ORACLE 23ai · N2",
         ["Carga de modelos ONNX", "PREDICTION() en SQL"])
    caja(ax, xs[3], y, W, H, "#dc2626", "PV_SIMULA_PKG",
         ["Escenario + regla dura", "JSON antes/después"])
    caja(ax, xs[4], y, W, H, "#16a34a", "APEX · N3",
         ["Mapa, semáforo, what-if", "Ciudadano y gestor"])

    for i in range(4):
        flecha(ax, xs[i] + W / 2 + 0.4, y, xs[i + 1] - W / 2 - 0.4, y)

    fig.suptitle("Pueblos con vida · Arquitectura (visión general)", fontsize=15, fontweight="bold")
    ax.text(1, 0.2, "Versión detallada: visuals/18_diagrama_arquitectura.png   ·   Fuente: scripts/generar_diagrama_arquitectura.py · 28-10-2026",
            fontsize=7.8, color="#666666", ha="left")
    fig.savefig(DIR_SALIDA / "19_diagrama_simple.png")
    plt.close(fig)


if __name__ == "__main__":
    DIR_SALIDA.mkdir(exist_ok=True)
    diagrama_detallado()
    diagrama_simple()
    print("OK ->", DIR_SALIDA / "18_diagrama_arquitectura.png")
    print("OK ->", DIR_SALIDA / "19_diagrama_simple.png")
