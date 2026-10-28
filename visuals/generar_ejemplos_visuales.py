"""Ejemplos visuales de los algoritmos del proyecto (M3 y M4) sobre el dataset real.

Genera 11 PNG en visuals/ (solo imágenes, sin documentación):

    01_mapa_calor_indice.png        Mapa de calor del índice de vitalidad (corte 2023, 155 mun.)
    02_mapas_5_dimensiones.png      Small multiples de las 5 dimensiones
    03_mapa_factor_limitante.png    Mapa categórico del factor limitante (argmin)
    04_ranking_top_bottom.png       Top 10 / Bottom 10 con desglose de dimensiones
    05_validacion_pred_vs_real.png  Prueba: ONNX predicho vs percent-rank real del dataset
    06_trayectorias_m3.png          Serie real 2010-2025 + proyección M3 2026-2035 (6 mun.)
    07_mapa_crecimiento_m3.png      Mapa del crecimiento previsto por M3 (h=5 y h=10)
    08_importancia_features.png     Importancias del RandomForest por dimensión
    09_dependencia_parcial.png      Curvas de dependencia parcial (RF y GBM)
    10_whatif_antes_despues.png     What-If: choque antes/después en 3 municipios
    11_rendimientos_decrecientes.png  Índice vs habitantes añadidos (saturación)

Reglas declaradas (idénticas o derivadas del pipeline existente):
  * Corte M4 = 2023, último año de la cohorte COMPLETA (sanidad 2025 y
    transporte 2024-25 están vacíos en el xlsx y el pipeline los excluye).
  * Índice = suma ponderada fija 0.20/0.15/0.25/0.25/0.15 (features.py / PV_SIMULA).
  * Factor limitante = argmin de las 5 dimensiones (regla SQL de la app).
  * Estado base what-if 2025: población, demografía y paro de 2025 (reales);
    servicios del último año observado (2023); telefonía 2025; stock 2025;
    estáticos de la hoja Municipios (con la imputación declarada de
    tiempo_centro_min para los 99 municipios sin modo registrado).
  * M3 solo se aplica a los 56 municipios con tiempo_centro_min real
    (con ellos fue entrenado). migracion_3y en 2025 = media 2019-2021
    (último trienio con dato, ventana 2023-25 vacía).
  * Los modelos se re-entrenan localmente SOLO para interpretabilidad
    (importancias / dependencia parcial) con los parámetros y semilla (2026)
    de las fichas; se verifica contra los ONNX reales.

Solo lectura del resto del repositorio. Ejecutar: python scripts/generar_ejemplos_visuales.py
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from src.common.dataset import cargar_municipios, cargar_panel  # noqa: E402
from src.m4_capacidad.features import (  # noqa: E402
    FEATURES_M4,
    PESOS,
    _estatica,
    construir_dataset_m4,
    indice,
)
from src.m3_demografia.features import FEATURES_M3  # noqa: E402

DIR_SALIDA = REPO / "visuals"
DIR_ONNX = REPO / "oracle_db" / "models"
SEMILLA = 2026

MADRID = (40.4168, -3.7038)  # referencia geográfica (km 0)

DIM_LABEL = {
    "dim_dem": "Demografía",
    "dim_viv": "Vivienda",
    "dim_ser": "Servicios",
    "dim_acc": "Accesibilidad",
    "dim_emp": "Empleo",
}
DIM_COLOR = {
    "dim_dem": "#4C78A8",
    "dim_viv": "#F58518",
    "dim_ser": "#54A24B",
    "dim_acc": "#B279A2",
    "dim_emp": "#E45756",
}
DIMS = list(DIM_LABEL)

# Municipios showcase (nombres tal cual el xlsx). 12, cubren zonas y limitantes.
SHOWCASE = [
    ("Ribatejada", "#1 del índice"),
    ("Valdeolmos-Alalpardo", "#2, vivienda limitante"),
    ("Horcajo de la Sierra-Aoslos", "vivienda alta / acceso bajo"),
    ("Arroyomolinos", "mayor crecimiento 2010-25"),
    ("Villalbilla", "crecimiento fuerte"),
    ("Rascafría", "mayor despoblación"),
    ("Acebeda, La", "diminuto envejecido"),
    ("Madarcos", "diminuto Sierra Norte"),
    ("Ciempozuelos", "servicios limitantes"),
    ("San Martín de Valdeiglesias", "último del ranking"),
    ("San Fernando de Henares", "corredor del Henares"),
    ("Colmenar de Oreja", "sureste, cola del ranking"),
]

# Choque what-if común (idéntico para los 3 municipios del ejemplo)
CHOQUE = {"hab": 400, "centros_salud": 1, "escuelas": 2, "paradas": 6}

FOOTER_BASE = (
    "Fuente: data/dataset_155_municipios_2010-2025.xlsx (INE/CM) · modelos ONNX de oracle_db/models · "
    f"generado {dt.date.today().isoformat()}"
)


def _norm(s: str) -> str:
    import unicodedata

    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().replace(",", " ").replace("-", " ").split()
    # lista de tokens


def _canon(s: str) -> list[str]:
    art = {"el", "la", "los", "las"}
    return [t for t in _norm(s) if t not in art]


def buscar_municipio(mun: pd.DataFrame, nombre: str) -> pd.Series:
    """Localiza un municipio tolerando acentos, comas y artículos ('La Acebeda' vs 'Acebeda, La')."""
    col = "municipio" if "municipio" in mun.columns else "nombre"
    q = _canon(nombre)
    hits = mun[mun[col].map(lambda m: _canon(m) == q)]
    if hits.empty:
        hits = mun[mun[col].map(lambda m: _canon(m) and q and " ".join(_canon(m)).startswith(" ".join(q)))]
    if hits.empty:
        raise KeyError(f"Municipio no encontrado: {nombre}")
    return hits.iloc[0]


# ─────────────────────────────────────────────────────────────────────────────
# Carga de datos y modelos
# ─────────────────────────────────────────────────────────────────────────────

def cargar_onnx_sessions():
    import onnxruntime as ort

    sess = {}
    for f in ["m3_demografia"] + [f"m4_capacidad_{k}" for k in ["dem", "viv", "ser", "acc", "emp"]]:
        s = ort.InferenceSession(str(DIR_ONNX / f"{f}.onnx"), providers=["CPUExecutionProvider"])
        sess[f] = s
    return sess


def onnx_predict(sess, X: np.ndarray) -> np.ndarray:
    s = sess.get_inputs()[0].name
    return sess.run(None, {s: X.astype(np.float32)})[0].ravel()


def m4_predict_dims(sessions, X: np.ndarray) -> np.ndarray:
    """(n,14) -> (n,5) columnas [dim_dem..dim_emp] con los 5 ONNX."""
    out = np.column_stack([onnx_predict(sessions[f"m4_capacidad_{k}"], X) for k in ["dem", "viv", "ser", "acc", "emp"]])
    return out


def m4_predict_index(sessions, X: np.ndarray) -> np.ndarray:
    dims = m4_predict_dims(sessions, X)
    w = np.array([PESOS[d] for d in DIMS])
    return dims @ w


def preparar_datos():
    panel = cargar_panel()
    mun = cargar_municipios()
    data = construir_dataset_m4(panel, mun)
    corte = data["anio"].max()
    c = data[data["anio"] == corte].copy()
    c["indice"] = indice(c)
    dims = c[DIMS].to_numpy()
    c["limitante"] = np.array(DIMS)[dims.argmin(axis=1)]
    c = c.merge(mun.set_index("cod_ine")[["centroide_lat", "centroide_lon"]], on="cod_ine", how="left")
    serie = panel.pivot(index="cod_ine", columns="anio", values="poblacion_total").sort_index().sort_index(axis=1)
    return panel, mun, data, c, corte, serie


def nombres_showcase(c: pd.DataFrame) -> dict[str, pd.Series]:
    out = {}
    for nombre, _ in SHOWCASE:
        fila = buscar_municipio(c, nombre)
        out[fila["nombre"]] = fila
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Estado municipal 2025 (what-if) — reglas declaradas en la cabecera
# ─────────────────────────────────────────────────────────────────────────────

def _valor_ultimo(panel: pd.DataFrame, cod: str, col: str, anio_limite: int) -> tuple[float, int]:
    g = panel[(panel["cod_ine"] == cod) & (panel["anio"] <= anio_limite) & panel[col].notna()]
    if g.empty:
        raise ValueError(f"Sin dato de {col} para {cod}")
    fila = g.sort_values("anio").iloc[-1]
    return float(fila[col]), int(fila["anio"])


def _crec_10y(serie_cod: pd.Series, t: int) -> float:
    start = max(serie_cod.index.min(), t - 10)
    ventana = [a for a in serie_cod.index if start <= a <= t]
    p0, p1 = serie_cod[ventana[0]], serie_cod[ventana[-1]]
    w = ventana[-1] - ventana[0]
    return (p1 / p0) ** (1 / w) - 1


def estado_m4(panel, mun_static, serie, cod: str, pob: float,
              d_salud: int = 0, d_escuelas: int = 0, d_paradas: int = 0) -> dict:
    """Estado M4 (14 features, orden FEATURES_M4) para pob y servicios dados."""
    st = mun_static.loc[cod]

    sal, anio_sal = _valor_ultimo(panel, cod, "centros_de_salud", 2025)
    con, _ = _valor_ultimo(panel, cod, "consultorios_locales", 2025)
    par, anio_par = _valor_ultimo(panel, cod, "paradas_autobus", 2025)
    met, _ = _valor_ultimo(panel, cod, "estaciones_metro", 2025)
    cer, _ = _valor_ultimo(panel, cod, "estaciones_cercanias", 2025)
    tel_baf, _ = _valor_ultimo(panel, cod, "lineas_telefonicas_baf", 2025)
    tel_atf, _ = _valor_ultimo(panel, cod, "lineas_telefonicas_atf", 2025)
    viv, _ = _valor_ultimo(panel, cod, "unidades_urbanas_residencial", 2025)

    ed, _ = _valor_ultimo(panel, cod, "edad_media", 2025)
    m15, _ = _valor_ultimo(panel, cod, "pct_poblacion_menor_15", 2025)
    p65, _ = _valor_ultimo(panel, cod, "pct_poblacion_65_mas", 2025)
    rep, _ = _valor_ultimo(panel, cod, "proporcion_reemplazamiento", 2025)
    paro, _ = _valor_ultimo(panel, cod, "paro_por_100_hab", 2025)
    vparo, _ = _valor_ultimo(panel, cod, "variacion_relativa_paro", 2025)

    return {
        "log_pob": float(np.log(pob)),
        "salud_10k": (sal + d_salud + con) / pob * 10_000,
        "escuelas_1000": (st["centros_educativos_alta"] + d_escuelas) / pob * 1_000,
        "paradas_1000": (par + d_paradas + met + cer) / pob * 1_000,
        "telefono_1000": (tel_baf + tel_atf) / pob * 1_000,
        "viv_1000": viv / pob * 1_000,
        "crec_10y_pct": _crec_10y(serie.loc[cod], 2025),
        "pct_menor_15": m15,
        "pct_65mas": p65,
        "reemplazamiento": rep,
        "paro_100": paro,
        "var_paro": vparo,
        "tiempo_centro_min": float(st["tiempo_imp"]),
        "distancia_sol_km": float(st["distancia_centro_km"]),
    }


def vector_m4(estado: dict) -> np.ndarray:
    return np.array([[estado[f] for f in FEATURES_M4]], dtype=float)


# ─────────────────────────────────────────────────────────────────────────────
# Features M3 en t=2025 (misma fórmula que features.py) y proyección
# ─────────────────────────────────────────────────────────────────────────────

def features_m3_2025(panel, mun_static, serie, cod: str, horizonte: int) -> dict:
    p = panel.set_index(["cod_ine", "anio"])
    pob = serie.loc[cod]
    crec = pob.pct_change()
    st = mun_static.loc[cod]
    if pd.isna(st["tiempo_centro_min"]):
        raise ValueError(f"M3 requiere tiempo_centro_min real; {cod} no lo tiene")
    migr = panel[(panel["cod_ine"] == cod) & (panel["anio"].between(2019, 2021))]["tasa_migracion"].mean()
    return {
        "log_pob": float(np.log(pob[2025])),
        "cagr_1": float(crec[2025]),
        "cagr_3": float((pob[2025] / pob[2022]) ** (1 / 3) - 1),
        "cagr_5": float((pob[2025] / pob[2020]) ** (1 / 5) - 1),
        "cagr_10": float((pob[2025] / pob[2015]) ** (1 / 10) - 1),
        "vol_5": float(crec.loc[2021:2025].std(ddof=1)),
        "edad_media": float(p.loc[(cod, 2025), "edad_media"]),
        "pct_menor_15": float(p.loc[(cod, 2025), "pct_poblacion_menor_15"]),
        "pct_65mas": float(p.loc[(cod, 2025), "pct_poblacion_65_mas"]),
        "reemplazamiento": float(p.loc[(cod, 2025), "proporcion_reemplazamiento"]),
        "paro_100": float(p.loc[(cod, 2025), "paro_por_100_hab"]),
        "var_paro": float(p.loc[(cod, 2025), "variacion_relativa_paro"]),
        "migracion_3y": float(migr),
        "distancia_sol_km": float(st["distancia_centro_km"]),
        "tiempo_centro_min": float(st["tiempo_imp"]),
        "horizonte": float(horizonte),
    }


def proyeccion_m3(sessions, panel, mun_static, serie, cod: str, anios: range) -> pd.Series:
    filas = [features_m3_2025(panel, mun_static, serie, cod, y - 2025) for y in anios]
    X = np.array([[f[k] for k in FEATURES_M3] for f in filas])
    log_factor = onnx_predict(sessions["m3_demografia"], X)
    return pd.Series(np.exp(log_factor), index=list(anios))  # factor vs 2025


# ─────────────────────────────────────────────────────────────────────────────
# Retrain local para interpretabilidad (parámetros/semilla de las fichas)
# ─────────────────────────────────────────────────────────────────────────────

def reentrenar_m4(data: pd.DataFrame):
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split

    X = data[FEATURES_M4].astype(float)
    y = data[DIMS].astype(float)
    idx = np.arange(len(X))
    tr, _ = train_test_split(idx, test_size=0.2, random_state=SEMILLA, shuffle=True)
    modelos = {}
    for d in DIMS:
        m = RandomForestRegressor(n_estimators=500, max_depth=18, min_samples_leaf=3,
                                  n_jobs=-1, random_state=SEMILLA)
        m.fit(X.iloc[tr], y.iloc[tr][d])
        modelos[d] = m
    return modelos, X, y


def reentrenar_m3():
    from src.m3_demografia.features import construir_dataset_m3, X_y as Xy_m3
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.model_selection import GroupShuffleSplit

    panel = cargar_panel()
    mun = cargar_municipios()
    d = construir_dataset_m3(panel, mun)
    X, y = Xy_m3(d)
    tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEMILLA)
                  .split(X, y, d["cod_ine"].values))
    m = GradientBoostingRegressor(n_estimators=400, learning_rate=0.05, max_depth=3,
                                  subsample=0.9, random_state=SEMILLA)
    m.fit(X.iloc[tr], y.iloc[tr])
    mae = float(np.abs(m.predict(X.iloc[te]) - y.iloc[te]).mean())
    return m, X, y, mae


def pdp_manual(modelo, X: pd.DataFrame, feature: str, grid_n: int = 40):
    """Dependencia parcial manual: media de predicciones sustituyendo la feature."""
    xs = np.quantile(X[feature], np.linspace(0.02, 0.98, grid_n))
    ys = []
    for v in xs:
        Xs = X.copy()
        Xs[feature] = v
        ys.append(modelo.predict(Xs).mean())
    return xs, np.array(ys)


# ─────────────────────────────────────────────────────────────────────────────
# Estética común
# ─────────────────────────────────────────────────────────────────────────────

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#fafafa",
    "axes.grid": True,
    "grid.color": "#dddddd",
    "grid.linewidth": 0.5,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
})


def footer(fig, texto: str):
    fig.text(0.01, -0.01, texto, fontsize=7, color="#666666", ha="left", va="top", wrap=True)


def pie_mapa(ax, c: pd.DataFrame, valores, titulo: str, cmap="RdYlGn", vmin=0, vmax=100,
             cbar_label: str = "", size_norm: float | None = None):
    tam = (np.sqrt(c["poblacion"]) if size_norm is None else np.sqrt(c["poblacion"]) / size_norm)
    sc = ax.scatter(c["centroide_lon"], c["centroide_lat"], c=valores, cmap=cmap,
                    vmin=vmin, vmax=vmax, s=12 + tam * 0.9, edgecolor="#333333",
                    linewidth=0.3, alpha=0.9, zorder=3)
    ax.scatter([MADRID[1]], [MADRID[0]], marker="*", s=220, c="#222222", zorder=4)
    ax.annotate("Madrid", (MADRID[1], MADRID[0]), xytext=(6, 6), textcoords="offset points",
                fontsize=8, color="#222222", zorder=4)
    ax.set_title(titulo, fontweight="bold")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_aspect("equal", adjustable="datalim")
    if cbar_label:
        cb = plt.colorbar(sc, ax=ax, shrink=0.85, pad=0.01)
        cb.set_label(cbar_label, fontsize=9)
    return sc


# ─────────────────────────────────────────────────────────────────────────────
# Figuras
# ─────────────────────────────────────────────────────────────────────────────

def fig01_mapa_indice(c: pd.DataFrame, corte: int, showcase: dict):
    fig, ax = plt.subplots(figsize=(11, 9), constrained_layout=True)
    pie_mapa(ax, c, c["indice"], f"Índice de vitalidad 2023 · 155 municipios <50k hab (Comunidad de Madrid)",
             cmap="RdYlGn", vmin=20, vmax=70, cbar_label="Índice 0-100 (percent-ranks, pesos 0.20/0.15/0.25/0.25/0.15)")
    for nombre, fila in showcase.items():
        ax.annotate(nombre, (fila["centroide_lon"], fila["centroide_lat"]),
                    xytext=(0, 9), textcoords="offset points", fontsize=6.6,
                    ha="center", color="#222222",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#999999", alpha=0.75))
    ax.scatter([], [], s=40, c="gray", label="tamaño ∝ población")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)
    footer(fig, FOOTER_BASE + " · índice = percent-ranks reales del dataset (targets del pipeline M4)")
    fig.savefig(DIR_SALIDA / "01_mapa_calor_indice.png")
    plt.close(fig)


def fig02_dimensiones(c: pd.DataFrame, corte: int):
    fig, axes = plt.subplots(2, 3, figsize=(14, 9.5), constrained_layout=True)
    for ax, dim in zip(axes.ravel(), DIMS):
        pie_mapa(ax, c, c[dim], f"{DIM_LABEL[dim]} · dim {dim.split('_')[1]} (0-100)", cmap="RdYlGn", vmin=0, vmax=100)
    axes.ravel()[-1].axis("off")
    footer(fig, FOOTER_BASE + f" · percent-rank dentro de la cohorte de {corte} (targets reales del dataset)")
    fig.savefig(DIR_SALIDA / "02_mapas_5_dimensiones.png")
    plt.close(fig)


def fig03_limitante(c: pd.DataFrame, corte: int):
    fig, ax = plt.subplots(figsize=(11, 9), constrained_layout=True)
    tam = np.sqrt(c["poblacion"])
    colores = [DIM_COLOR[d] for d in c["limitante"]]
    orden = sorted(c["limitante"].unique())
    for dim in DIMS:
        sub = c[c["limitante"] == dim]
        if sub.empty:
            continue
        ax.scatter(sub["centroide_lon"], sub["centroide_lat"], c=DIM_COLOR[dim],
                   s=12 + np.sqrt(sub["poblacion"]) * 0.9, edgecolor="#333333", linewidth=0.3,
                   alpha=0.9, zorder=3,
                   label=f"{DIM_LABEL[dim]} ({len(sub)})")
    ax.scatter([MADRID[1]], [MADRID[0]], marker="*", s=220, c="#222222", zorder=4)
    ax.annotate("Madrid", (MADRID[1], MADRID[0]), xytext=(6, 6), textcoords="offset points", fontsize=8)
    ax.set_title(f"¿Qué se rompe primero en cada zona? Factor limitante {corte} (argmin de las 5 dims)",
                 fontweight="bold")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_aspect("equal", adjustable="datalim")
    ax.legend(loc="lower left", fontsize=9, title="limitante (nº municipios)", framealpha=0.9)
    footer(fig, FOOTER_BASE + " · color = dimensión MÍNIMA del municipio; tamaño = población")
    fig.savefig(DIR_SALIDA / "03_mapa_factor_limitante.png")
    plt.close(fig)


def fig04_ranking(c: pd.DataFrame, sessions, corte: int):
    X = c[FEATURES_M4].to_numpy(float)
    c = c.copy()
    c["indice_pred"] = m4_predict_index(sessions, X)
    rho = c["indice"].corr(c["indice_pred"], method="spearman")

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 7), sharex=False, constrained_layout=False)
    for ax, (titulo, sub) in zip(axes, [
        (f"Top 10 · mejores índices {corte}", c.nlargest(10, "indice").iloc[::-1]),
        (f"Bottom 10 · índices más bajos {corte}", c.nsmallest(10, "indice")),
    ]):
        izquierda = np.zeros(len(sub))
        for dim in DIMS:
            ax.barh(sub["nombre"], sub[dim], left=izquierda, color=DIM_COLOR[dim],
                    label=DIM_LABEL[dim], height=0.68)
            izquierda += sub[dim].to_numpy()
        for nombre, i_real, i_pred in zip(sub["nombre"], sub["indice"], sub["indice_pred"]):
            ax.annotate(f"{i_real:.1f} (onnx {i_pred:.1f})",
                        (izquierda.max() * 1.02, nombre), xytext=(4, 0),
                        textcoords="offset points", va="center", fontsize=7.6, color="#333333")
        ax.set_title(titulo, fontweight="bold")
        ax.set_xlabel("suma de las 5 dimensiones (percent-ranks 0-100 cada una)")
        ax.tick_params(axis="y", labelsize=8.5)
        ax.set_xlim(0, izquierda.max() * 1.40)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.90), ncol=5,
               fontsize=9, frameon=False)
    fig.suptitle("¿Qué municipio es mejor? Desglose de las 5 dimensiones y prueba del modelo",
                 fontsize=13, fontweight="bold", y=0.965)
    fig.subplots_adjust(left=0.13, right=0.985, top=0.82, bottom=0.11, wspace=0.42)
    footer(fig, FOOTER_BASE + f" · barras = percent-ranks reales (dataset); texto = índice real (predicción ONNX de los 5 modelos) · Spearman(real, pred) = {rho:.3f}")
    fig.savefig(DIR_SALIDA / "04_ranking_top_bottom.png")
    plt.close(fig)


def fig05_validacion(c: pd.DataFrame, sessions, corte: int):
    from scipy.stats import spearmanr

    X = c[FEATURES_M4].to_numpy(float)
    pred = m4_predict_dims(sessions, X)
    real = c[DIMS].to_numpy(float)
    fig, axes = plt.subplots(2, 3, figsize=(14, 9), constrained_layout=True)
    paneles = list(zip(DIMS, range(5))) + [("indice", 5)]
    for ax, (nombre, k) in zip(axes.ravel(), paneles):
        if nombre == "indice":
            r = real @ np.array([PESOS[d] for d in DIMS])
            p = pred @ np.array([PESOS[d] for d in DIMS])
            etiqueta = "Índice ponderado"
        else:
            r, p = real[:, k], pred[:, k]
            etiqueta = f"{DIM_LABEL[nombre]} ({nombre})"
        sc = ax.scatter(r, p, s=26, c="#3b6fb6", alpha=0.75, edgecolor="white", linewidth=0.3)
        lim = [min(r.min(), p.min()) - 2, max(r.max(), p.max()) + 2]
        ax.plot(lim, lim, "--", c="#bb4444", lw=1, label="y = x")
        rho = spearmanr(r, p).statistic
        mae = float(np.abs(p - r).mean())
        ax.set_title(f"{etiqueta}\nSpearman={rho:.3f} · MAE={mae:.1f}", fontsize=10)
        ax.set_xlabel("real (percent-rank dataset)")
        ax.set_ylabel("predicho (ONNX)")
        ax.set_xlim(lim)
        ax.set_ylim(lim)
    fig.suptitle(f"Prueba en el corte {corte}: los 5 ONNX de M4 reproducen el percent-rank del dataset",
                 fontsize=13, fontweight="bold")
    footer(fig, FOOTER_BASE + " · métricas de test (backtest por filas) en doc/modelos/m4_capacidad.json")
    fig.savefig(DIR_SALIDA / "05_validacion_pred_vs_real.png")
    plt.close(fig)


def _elegir_trayectorias(c: pd.DataFrame, serie: pd.DataFrame, tiempo_raw: pd.Series) -> list[str]:
    """6 municipios con tiempo_centro_min REAL: 2 crecen, 2 decrecen, 1 top, 1 bottom."""
    con = c[c["cod_ine"].map(tiempo_raw).notna()].copy()
    cagr = ((serie.loc[con["cod_ine"], 2025] / serie.loc[con["cod_ine"], 2015]) ** (1 / 10) - 1)
    con["cagr_10"] = cagr.to_numpy()
    elegidos = []
    for cod in con.nlargest(2, "cagr_10")["cod_ine"]:
        elegidos.append(cod)
    for cod in con.nsmallest(2, "cagr_10")["cod_ine"]:
        if cod not in elegidos:
            elegidos.append(cod)
    top = con.nlargest(3, "indice")["cod_ine"]
    bot = con.nsmallest(3, "indice")["cod_ine"]
    for cand in list(top) + list(bot):
        if cand not in elegidos:
            elegidos.append(cand)
        if len(elegidos) == 6:
            break
    nombres = c.set_index("cod_ine").loc[elegidos, "nombre"].tolist()
    return nombres


def fig06_trayectorias(sessions, panel, mun_static, serie, c: pd.DataFrame, tiempo_raw: pd.Series):
    nombres = _elegir_trayectorias(c, serie, tiempo_raw)
    anios_proj = range(2026, 2036)
    fig, axes = plt.subplots(2, 3, figsize=(15, 8.5), constrained_layout=True)
    resumen = []
    for ax, nombre in zip(axes.ravel(), nombres):
        cod = buscar_municipio(c, nombre)["cod_ine"]
        real = serie.loc[cod]
        factor = proyeccion_m3(sessions, panel, mun_static, serie, cod, anios_proj)
        proj = factor * real[2025]
        ax.plot(real.index, real.values, "-o", c="#2a6fb0", ms=3.5, lw=1.8, label="población real (INE)")
        ax.plot(proj.index, proj.values, "--s", c="#d1495b", ms=3.5, lw=1.8, label="proyección M3 (ONNX)")
        ax.axvspan(2030.5, 2035.4, color="#f2c94c", alpha=0.18)
        ax.axvline(2025, color="#888888", lw=0.8, ls=":")
        cagr10 = (factor[2035] ** (1 / 10) - 1) * 100
        ax.set_title(f"{nombre}\nCAGR previsto 2025-2035: {cagr10:+.2f} %/año", fontsize=10, fontweight="bold")
        ax.set_xlabel("año")
        ax.set_ylabel("habitantes")
        resumen.append((nombre, real[2025], cagr10))
    handles, labels = axes.ravel()[0].get_legend_handles_labels()
    from matplotlib.patches import Patch

    handles += [Patch(fc="#f2c94c", alpha=0.25, label="h>5: extrapolación (fuera de entrenamiento)")]
    labels += ["h>5: extrapolación (fuera de entrenamiento)"]
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=9, frameon=False,
               bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("M3 · Demografía: trayectoria real 2010-2025 y proyección ONNX 2026-2035",
                 fontsize=13, fontweight="bold")
    footer(fig, FOOTER_BASE + " · features en t=2025 con la fórmula exacta de features.py; migracion_3y = media 2019-2021 (último trienio con dato); solo municipios con tiempo_centro_min real (56)")
    fig.savefig(DIR_SALIDA / "06_trayectorias_m3.png")
    plt.close(fig)
    return resumen


def fig07_mapa_crecimiento(sessions, panel, mun_static, serie, mun: pd.DataFrame):
    con = mun[mun["tiempo_centro_min"].notna()].copy()
    c = pd.DataFrame({"cod_ine": con["cod_ine"].values, "nombre": con["municipio"].values,
                      "centroide_lat": con["centroide_lat"].values, "centroide_lon": con["centroide_lon"].values,
                      "poblacion": serie.loc[con["cod_ine"], 2025].to_numpy()})
    for h, col in [(5, "crec_h5"), (10, "crec_h10")]:
        fac = [proyeccion_m3(sessions, panel, mun_static, serie, cod, range(2025 + h, 2025 + h + 1))[2025 + h] for cod in c["cod_ine"]]
        c[col] = (np.array(fac) - 1) * 100  # % total vs 2025

    fig, axes = plt.subplots(1, 2, figsize=(15, 7.6), constrained_layout=True)
    limite = float(np.nanmax(np.abs(c[["crec_h5", "crec_h10"]].to_numpy())))
    for ax, col, titulo in [
        (axes[0], "crec_h5", "Crecimiento previsto a 5 años (2030)"),
        (axes[1], "crec_h10", "Crecimiento previsto a 10 años (2035)"),
    ]:
        sc = ax.scatter(c["centroide_lon"], c["centroide_lat"], c=c[col], cmap="RdBu_r",
                        vmin=-limite, vmax=limite, s=55, edgecolor="#333333", linewidth=0.4, zorder=3)
        ax.scatter([MADRID[1]], [MADRID[0]], marker="*", s=200, c="#222222", zorder=4)
        ax.set_title(titulo, fontweight="bold")
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")
        ax.set_aspect("equal", adjustable="datalim")
        cb = plt.colorbar(sc, ax=ax, shrink=0.85, pad=0.01)
        cb.set_label("% vs 2025", fontsize=9)
    fig.suptitle("M3 · Geografía del crecimiento poblacional previsto (56 municipios con transporte registrado)",
                 fontsize=13, fontweight="bold")
    footer(fig, FOOTER_BASE + " · azul = pierde población, rojo = gana · solo municipios con tiempo_centro_min real (con ellos se entrenó M3)")
    fig.savefig(DIR_SALIDA / "07_mapa_crecimiento_m3.png")
    plt.close(fig)


def fig08_importancias(data: pd.DataFrame, modelos_m4, pesos_panel):
    fig, axes = plt.subplots(2, 3, figsize=(15, 8.5), constrained_layout=True)
    for ax, dim in zip(axes.ravel(), DIMS):
        imp = pd.Series(modelos_m4[dim].feature_importances_, index=FEATURES_M4).nlargest(8).iloc[::-1]
        ax.barh(imp.index, imp.values, color=DIM_COLOR[dim])
        ax.set_title(f"Importancia para {DIM_LABEL[dim]}", fontsize=10, fontweight="bold")
        ax.tick_params(axis="y", labelsize=8)
        ax.set_xlabel("importancia (impureza)")
    ax = axes.ravel()[5]
    ax.clear()
    ax.barh([DIM_LABEL[d] for d in DIMS], [pesos_panel[d] for d in DIMS],
            color=[DIM_COLOR[d] for d in DIMS])
    ax.set_title("Pesos fijos del índice (SQL)", fontsize=10, fontweight="bold")
    ax.set_xlabel("peso")
    fig.suptitle("M4 · ¿En qué se fija cada RandomForest? Importancia de features por dimensión",
                 fontsize=13, fontweight="bold")
    footer(fig, FOOTER_BASE + " · RandomForest re-entrenado con los parámetros y semilla (2026) de doc/modelos/m4_capacidad.json")
    fig.savefig(DIR_SALIDA / "08_importancia_features.png")
    plt.close(fig)


def fig09_dependencia(modelos_m4, X4, modelo_m3, X3, y3):
    panel_spec = [
        ("dim_ser", "salud_10k", "Servicios: centros de salud por 10k hab"),
        ("dim_ser", "escuelas_1000", "Servicios: escuelas por 1000 hab"),
        ("dim_acc", "tiempo_centro_min", "Accesibilidad: minutos a Madrid"),
        ("dim_viv", "viv_1000", "Vivienda: viviendas por 1000 hab"),
        ("dim_dem", "pct_65mas", "Demografía: % población 65+"),
        ("dim_emp", "paro_100", "Empleo: paro por 100 hab"),
    ]
    fig, axes = plt.subplots(2, 4, figsize=(16.5, 8), constrained_layout=True)
    for ax, (dim, feat, titulo) in zip(axes.ravel(), panel_spec):
        xs, ys = pdp_manual(modelos_m4[dim], X4, feat)
        ax.plot(xs, ys, "-o", ms=3, c=DIM_COLOR[dim], lw=1.8)
        ax.set_title(titulo, fontsize=9.5, fontweight="bold")
        ax.set_xlabel(feat)
        ax.set_ylabel("efecto parcial sobre la dim (0-100)")
    # M3: log-factor vs distancia y vs %65+ (efecto en % de crecimiento)
    for ax, feat, titulo in [
        (axes.ravel()[6], "distancia_sol_km", "M3: km a Madrid → crecimiento"),
        (axes.ravel()[7], "pct_65mas", "M3: % 65+ → crecimiento"),
    ]:
        xs, ys = pdp_manual(modelo_m3, X3, feat, grid_n=30)
        pct = (np.exp(ys) - 1) * 100  # efecto sobre el factor, en %
        ax.plot(xs, pct, "-o", ms=3, c="#8c564b", lw=1.8)
        ax.axhline(0, color="#888888", lw=0.8, ls=":")
        ax.set_title(titulo, fontsize=9.5, fontweight="bold")
        ax.set_xlabel(feat)
        ax.set_ylabel("efecto parcial sobre el factor (%)")
    fig.suptitle("Cómo piensan los algoritmos: curvas de dependencia parcial (media de predicciones moviendo una feature)",
                 fontsize=13, fontweight="bold")
    footer(fig, FOOTER_BASE + " · modelos re-entrenados con parámetros y semilla de las fichas (2026); M3 expresado en % del factor = exp(efecto)-1")
    fig.savefig(DIR_SALIDA / "09_dependencia_parcial.png")
    plt.close(fig)


def fig10_whatif(sessions, panel, mun_static, serie, c: pd.DataFrame):
    ejemplos = ["Ciempozuelos", "Ribatejada", "Arroyomolinos"]
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.6), sharey=True, constrained_layout=True)
    for ax, nombre in zip(axes, ejemplos):
        fila = buscar_municipio(c, nombre)
        cod = fila["cod_ine"]
        pob0 = float(serie.loc[cod, 2025])
        est0 = estado_m4(panel, mun_static, serie, cod, pob0)
        est1 = estado_m4(panel, mun_static, serie, cod, pob0 + CHOQUE["hab"],
                         d_salud=CHOQUE["centros_salud"], d_escuelas=CHOQUE["escuelas"],
                         d_paradas=CHOQUE["paradas"])
        d0 = m4_predict_dims(sessions, vector_m4(est0))[0]
        d1 = m4_predict_dims(sessions, vector_m4(est1))[0]
        i0, i1 = d0 @ np.array([PESOS[k] for k in DIMS]), d1 @ np.array([PESOS[k] for k in DIMS])
        lim0, lim1 = DIMS[int(d0.argmin())], DIMS[int(d1.argmin())]
        x = np.arange(5)
        ax.bar(x - 0.19, d0, width=0.38, color="#9aa5b1")
        ax.bar(x + 0.19, d1, width=0.38, color=[DIM_COLOR[k] for k in DIMS])
        for xi, (v0, v1) in enumerate(zip(d0, d1)):
            ax.annotate(f"{v1 - v0:+.1f}", (xi + 0.19, v1), xytext=(0, 3 if v1 >= v0 else -11),
                        textcoords="offset points", ha="center", fontsize=8,
                        color="#1a7f37" if v1 >= v0 else "#b42318", fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels([DIM_LABEL[k] for k in DIMS], fontsize=8.5, rotation=20)
        ax.set_title(f"{nombre} ({int(pob0):,} hab)".replace(",", "."),
                     fontsize=10.5, fontweight="bold")
        ax.text(0.02, 0.97, f"índice: {i0:.1f} → {i1:.1f}  ({i1 - i0:+.1f})\n"
                            f"limitante: {DIM_LABEL[lim0]} → {DIM_LABEL[lim1]}",
                transform=ax.transAxes, va="top", fontsize=8.6,
                bbox=dict(boxstyle="round", fc="white", ec="#cccccc", alpha=0.9))
        if ax is axes[0]:
            ax.set_ylabel("dimensión (0-100)")
    from matplotlib.patches import Patch

    proxies = [Patch(fc="#9aa5b1", label="antes"),
               Patch(fc="white", ec="#888888", label="después (color = dimensión)")]
    axes[0].legend(handles=proxies, loc="lower right", fontsize=8, framealpha=0.95)
    fig.suptitle("What-If (M3+M4 como en la app): +400 hab, +1 centro de salud, +2 escuelas, +6 paradas · estado base 2025",
                 fontsize=12.5, fontweight="bold")
    footer(fig, FOOTER_BASE + " · estado base: población/demografía/paro 2025 reales + servicios del último año observado (2023) + estáticos de la hoja Municipios · predicción efímera, igual que PV_SIMULA")
    fig.savefig(DIR_SALIDA / "10_whatif_antes_despues.png")
    plt.close(fig)


def fig11_rendimientos(sessions, panel, mun_static, serie, c: pd.DataFrame):
    ejemplos = ["Ciempozuelos", "Ribatejada"]
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.6), sharey=False, constrained_layout=True)
    hab = np.arange(0, 2001, 100)
    for ax, nombre in zip(axes, ejemplos):
        cod = buscar_municipio(c, nombre)["cod_ine"]
        pob0 = float(serie.loc[cod, 2025])
        idx_solo, idx_con = [], []
        for n in hab:
            e = estado_m4(panel, mun_static, serie, cod, pob0 + n)
            idx_solo.append(m4_predict_index(sessions, vector_m4(e))[0])
            # servicios crecen con la población: +1 escuela/500, +1 centro/1500, +3 paradas/500
            e2 = estado_m4(panel, mun_static, serie, cod, pob0 + n,
                           d_salud=int(round(n / 1500)), d_escuelas=int(round(n / 500)),
                           d_paradas=int(round(n / 500 * 3)))
            idx_con.append(m4_predict_index(sessions, vector_m4(e2))[0])
        ax.plot(hab, idx_solo, "-o", ms=3.5, c="#b42318", lw=1.8, label="solo llega población (servicios fijos)")
        ax.plot(hab, idx_con, "-o", ms=3.5, c="#1a7f37", lw=1.8, label="población + servicios proporcionales")
        i0 = idx_solo[0]
        ax.axhline(i0, color="#888888", lw=0.8, ls=":")
        ax.annotate(f"índice actual {i0:.1f}", (hab[0], i0), xytext=(4, 4), textcoords="offset points", fontsize=8, color="#555555")
        pico = int(hab[int(np.argmax(idx_solo))])
        texto = f"máximo con solo población: +{pico} hab\n(y después baja: saturación)"
        if pico <= 200:  # el pico está en el borde izquierdo: texto hacia la derecha
            ax.annotate(texto, (pico, max(idx_solo)), xytext=(8, 20), textcoords="offset points",
                        ha="left", fontsize=8, color="#b42318",
                        arrowprops=dict(arrowstyle="->", color="#b42318", lw=0.9))
        else:
            ax.annotate(texto, (pico, max(idx_solo)), xytext=(0, 22), textcoords="offset points",
                        ha="center", fontsize=8, color="#b42318",
                        arrowprops=dict(arrowstyle="->", color="#b42318", lw=0.9))
        ax.set_title(nombre, fontsize=11, fontweight="bold")
        ax.set_xlabel("habitantes añadidos al estado 2025")
        ax.set_ylim(min(idx_solo + idx_con) - 2, max(idx_solo + idx_con) + 6)
    axes[0].set_ylabel("índice de vitalidad simulado (M4)")
    axes[0].legend(loc="upper right", fontsize=8.5, framealpha=0.95)
    fig.suptitle("El algoritmo castiga la saturación: el mismo choque de población puede bajar el índice sin inversión",
                 fontsize=12.5, fontweight="bold")
    footer(fig, FOOTER_BASE + " · servicios proporcionales declarados: +1 escuela/500 hab, +1 centro de salud/1500 hab, +3 paradas/500 hab · predicción efímera")
    fig.savefig(DIR_SALIDA / "11_rendimientos_decrecientes.png")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────

def main():
    t0 = dt.datetime.now()
    DIR_SALIDA.mkdir(exist_ok=True)

    print("[1/6] Cargando dataset y construyendo estados M4...")
    panel, mun, data, c, corte, serie = preparar_datos()
    print(f"      corte={corte} · estados totales={len(data)} · municipios corte={len(c)}")

    print("[2/6] Cargando 6 modelos ONNX (m3_demografia + m4_capacidad_*)...")
    sessions = cargar_onnx_sessions()

    print("[3/6] Figuras M4 (mapas, ranking, validación)...")
    showcase = nombres_showcase(c)
    fig01_mapa_indice(c, corte, showcase)
    fig02_dimensiones(c, corte)
    fig03_limitante(c, corte)
    fig04_ranking(c, sessions, corte)
    fig05_validacion(c, sessions, corte)

    print("[4/6] Figuras M3 (trayectorias y mapa de crecimiento)...")
    mun_static = mun.set_index("cod_ine").copy()
    # tiempo_centro_min IMPUTADO (regla declarada de features.py/M4) para M4;
    # la cruda (con nulos) delimita qué municipios puede usar M3.
    est_imp, _ = _estatica(mun)
    mun_static["tiempo_imp"] = est_imp.set_index("cod_ine")["tiempo_centro_min"].reindex(mun_static.index)
    tiempo_raw = mun.set_index("cod_ine")["tiempo_centro_min"]
    resumen_tray = fig06_trayectorias(sessions, panel, mun_static, serie, c, tiempo_raw)
    fig07_mapa_crecimiento(sessions, panel, mun_static, serie, mun)

    print("[5/6] Re-entrenando localmente para interpretabilidad (semilla 2026)...")
    modelos_m4, X4, y4 = reentrenar_m4(data)
    modelo_m3, X3, y3, mae3 = reentrenar_m3()
    # Verificación contra los ONNX reales (los re-entrenados deben coincidir)
    Xall_df = data[FEATURES_M4].astype(float)
    Xall = Xall_df.to_numpy(float)
    diff = np.max(np.abs(m4_predict_dims(sessions, Xall) - np.column_stack([modelos_m4[d].predict(Xall_df) for d in DIMS])))
    print(f"      comprobación re-train vs ONNX (M4): max_diff={diff:.2e} · M3 MAE test={mae3:.4f} (ficha: 0.0174)")

    print("[6/6] Figuras de interpretabilidad y what-if...")
    fig08_importancias(data, modelos_m4, PESOS)
    fig09_dependencia(modelos_m4, X4, modelo_m3, X3, y3)
    fig10_whatif(sessions, panel, mun_static, serie, c)
    fig11_rendimientos(sessions, panel, mun_static, serie, c)

    print("\n=== RESUMEN ===")
    top1 = c.nlargest(1, "indice").iloc[0]
    bot1 = c.nsmallest(1, "indice").iloc[0]
    print(f"Corte usado: {corte} (último año completo de la cohorte M4)")
    print(f"Mejor municipio: {top1['nombre']} (índice {top1['indice']:.1f})")
    print(f"Peor municipio:  {bot1['nombre']} (índice {bot1['indice']:.1f})")
    print("Trayectorias M3 dibujadas:")
    for n, p, cg in resumen_tray:
        print(f"  - {n}: {int(p):,} hab (2025) · {cg:+.2f} %/año previsto".replace(",", "."))
    print("Figuras generadas en visuals/:")
    for f in sorted(DIR_SALIDA.glob("*.png")):
        print(f"  · {f.name}")
    print(f"Tiempo total: {(dt.datetime.now() - t0).total_seconds():.1f}s")


if __name__ == "__main__":
    main()
