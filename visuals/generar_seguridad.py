"""Diapositiva «Seguridad y gobernanza» del MVP (Executive Slate).

    24_seguridad_gobernanza.png

Todo lo que afirma la diapositiva está VERIFICADO sobre el repositorio (28-10-2026):
  * 0 credenciales hardcodeadas en oracle_db/ (búsqueda: IDENTIFIED BY/PASSWORD/SECRET/TOKEN)
  * 0 EXECUTE IMMEDIATE en oracle_db/sql (sin SQL dinámico → sin inyección)
  * wallet/ y .env fuera del repositorio (.gitignore)
  * dataset = solo datos públicos agregados (sin datos personales)

Solo lectura del resto del repositorio. Ejecutar: python scripts/generar_seguridad.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

DIR_SALIDA = REPO / "visuals"

ACCENT = "#1e40af"
INK = "#0f172a"
BODY = "#334155"
BORDE = "#cbd5e1"
VERDE = "#047857"


def tarjeta(ax, cx, y_arriba, w, h, num, titulo, lineas, tag):
    y = y_arriba - h
    ax.add_patch(FancyBboxPatch((cx - w / 2, y), w, h,
                                boxstyle="round,pad=0.1,rounding_size=0.9",
                                fc="white", ec=BORDE, lw=1.4, zorder=3))
    ax.add_patch(FancyBboxPatch((cx - w / 2 + 1.4, y_arriba - 3.6), 2.7, 2.7,
                                boxstyle="round,pad=0.08,rounding_size=0.5",
                                fc=ACCENT, ec="none", zorder=4))
    ax.text(cx - w / 2 + 2.75, y_arriba - 2.25, str(num), ha="center", va="center",
            fontsize=9.2, fontweight="bold", color="white", zorder=5)
    ax.text(cx - w / 2 + 4.9, y_arriba - 2.25, titulo, ha="left", va="center",
            fontsize=10.2, fontweight="bold", color=INK, zorder=5)
    yy = y_arriba - 6.2
    for linea in lineas:
        ax.text(cx, yy, linea, ha="center", va="center", fontsize=8.2, color=BODY, zorder=5)
        yy -= 2.1
    ax.text(cx, yy - 0.2, "✓ " + tag, ha="center", va="center", fontsize=7.6,
            color=VERDE, zorder=5)


def main():
    fig, ax = plt.subplots(figsize=(16, 9.4), constrained_layout=True)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Franja de verificación
    ax.add_patch(FancyBboxPatch((2, 84), 96, 12,
                                boxstyle="round,pad=0.1,rounding_size=1.4",
                                fc="#f8fafc", ec=BORDE, lw=1.2, zorder=2))
    ax.text(50, 92.2, "Verificado sobre el repositorio · 28-10-2026", ha="center",
            va="center", fontsize=9.6, fontweight="bold", color=INK, zorder=4)
    ax.text(50, 87.4, "✓ 0 credenciales hardcodeadas en oracle_db/ (IDENTIFIED BY · PASSWORD · SECRET · TOKEN: ninguna)      "
                      "✓ 0 EXECUTE IMMEDIATE en PV_SIMULA      ✓ wallet/ y .env fuera del repo",
            ha="center", va="center", fontsize=8.0, color=ACCENT, zorder=4)

    # Fila 1: 3 pilares
    pilares_f1 = [
        (17.5, "Privacidad por diseño",
         ["Solo datos públicos agregados", "(INE, IEM, Catastro, CRTM, IGN).", "Cero datos personales:"],
         "compatible RGPD por diseño"),
        (50.0, "Superficie mínima",
         ["Los modelos viven dentro de Oracle.", "Sin APIs externas, sin túneles,", "sin puertos extra: nada que abrir."],
         "0 endpoints externos"),
        (82.5, "Cero secretos en el código",
         ["Wallet y credenciales fuera", "del repositorio (.gitignore):", "nunca se versionan."],
         "verificado: 0 secretos"),
    ]
    for cx, t, ls, tag in pilares_f1:
        tarjeta(ax, cx, 78, 30.5, 22.5, pilares_f1.index((cx, t, ls, tag)) + 1, t, ls, tag)

    # Fila 2: 2 pilares
    pilares_f2 = [
        (33.75, "Sin inyección SQL",
         ["PV_SIMULA_PKG no usa SQL dinámico", "(0 EXECUTE IMMEDIATE):", "los parámetros van como binds."],
         "0 superficie de inyección"),
        (66.25, "Trazabilidad total",
         ["Ficha técnica + sha256 del dataset", "+ semilla 2026: modelos", "reproducibles y auditables."],
         "sin ficha no se sube modelo"),
    ]
    for cx, t, ls, tag in pilares_f2:
        tarjeta(ax, cx, 49, 30.5, 22.5, pilares_f2.index((cx, t, ls, tag)) + 4, t, ls, tag)

    # Cierre
    ax.add_patch(FancyBboxPatch((14, 2), 72, 8.5,
                                boxstyle="round,pad=0.1,rounding_size=1.2",
                                fc="#eff6ff", ec=BORDE, lw=1.2, zorder=2))
    ax.text(50, 7.6, "La seguridad del MVP no es una capa añadida: es consecuencia de la arquitectura.",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color=ACCENT, zorder=4)
    ax.text(50, 4.2, "datos públicos + inferencia dentro de la base + simulación efímera + trazabilidad total",
            ha="center", va="center", fontsize=8.4, color=BODY, style="italic", zorder=4)

    fig.suptitle("Seguridad y gobernanza del MVP", fontsize=15.5, fontweight="bold", color=INK)
    ax.text(1, -0.8, "Verificación reproducible: buscar «IDENTIFIED BY|PASSWORD|SECRET|TOKEN» y «EXECUTE IMMEDIATE» en oracle_db/ · "
                     "wallet/ y .env en .gitignore · 28-10-2026",
            fontsize=7.8, color="#666666", ha="left")
    fig.savefig(DIR_SALIDA / "24_seguridad_gobernanza.png")
    plt.close(fig)
    print("OK ->", DIR_SALIDA / "24_seguridad_gobernanza.png")


if __name__ == "__main__":
    main()
