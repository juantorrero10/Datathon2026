"""M7 · Stocks — features para proyectar los stocks congelados del mapa/WI.

Motivo: hasta ahora el mapa y el WI trataban viviendas, centros de salud,
paradas y escuelas como stocks FIJOS (solo cambiaba la población al
denominador), así que esas capas "empeoraban" mecánicamente. M7 añade la
pieza que faltaba: cuánto stock se predeciría que se CONSTRUIRÍA en cada
municipio hasta el año objetivo.

Modelos (una dimensión ∴ un modelo ∴ un fichero .onnx):
  Crecimiento (esquema M3): muestra = (municipio, año base t, horizonte h 1..5).
    Features conocidas en t; target log(stock(t+h)/stock(t)) en escala log1p;
    el consumidor aplica EXP(factor).
      · M7_VIVIENDAS: stock = unidades_urbanas_residencial (serie completa;
        despliegue t=2025)
      · M7_SALUD:     stock = centros_de_salud + consultorios_locales
        (sanidad ausente en 2014 y 2025; despliegue t=2024)
      · M7_PARADAS:   stock = paradas autobús + metro + cercanías
        (transporte ausente 2024-2025; despliegue t=2023)
    Para h>5 el consumidor compone geométricamente:
    factor(h) = EXP(pred(5))**(h/5) (patrón ya usado por PV_MAPA para M3/M6).
  Cross-sectional (sin serie temporal): M7_ESCUELAS.
    La escuela solo existe como UN corte (centros_educativos_alta, estático,
    23 municipios con 0) — no hay señal temporal honesta para una tasa de
    construcción. El modelo aprende "cuántas escuelas esperadas tiene un
    municipio de tamaño X" en la cohorte; el pronóstico usa la POBLACIÓN
    PROYECTADA del M3 como feature para que el stock responda al crecimiento
    previsto. Declarado así en la ficha.

Paridad de despliegue: features almacenadas en PV_BASE_M3_M4 con prefijo
VIV_/SAL_/PAR_: {P}_LOG_POB, {P}_LOG_ST, {P}_CAGR_1/3/5/10, {P}_VOL_5,
{P}_P1000, {P}_POB_CAGR_5. La escala LOG_ST es el log1p del stock — idéntica
a la del entrenamiento (log1p permite stocks 0 con CAGRs finitos).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

STOCKS = ["viv", "sal", "par"]

MODELOS_SERIE = {
    "viv": {"nombre": "viviendas", "cols": ["unidades_urbanas_residencial"], "t_dep": 2025},
    "sal": {"nombre": "salud", "cols": ["centros_de_salud", "consultorios_locales"], "t_dep": 2024},
    "par": {"nombre": "paradas", "cols": ["paradas_autobus", "estaciones_metro", "estaciones_cercanias"], "t_dep": 2023},
}

# Features de los tres modelos de crecimiento, en el ORDEN EXACTO que consumirá
# el ONNX. Los nombres van SIN prefijo; el deployment los prefija (VIV_/SAL_/PAR_).
FEATURES_M7 = [
    "log_st",
    "st_cagr_1",
    "st_cagr_3",
    "st_cagr_5",
    "st_cagr_10",
    "st_vol_5",
    "st_p1000",
    "log_pob",
    "pob_cagr_5",
    "horizonte",
]
TARGET_M7 = "log_factor"
HORIZONTE_MAX_M7 = 5
ANIO_MIN_POB_5 = 2015   # pob_cagr_5 exige pob(t-5) en la serie completa

FEATURES_M7_ESC = [
    "log_pob",
    "edad_media",
    "pct_menor_15",
    "pct_65mas",
    "distancia_sol_km",
    "tiempo_centro_min",
]
TARGET_M7_ESC = "centros_educativos_alta"


def serie_pob(panel: pd.DataFrame) -> pd.DataFrame:
    """Serie de población completa (municipio × año)."""
    return (panel.pivot(index="cod_ine", columns="anio", values="poblacion_total")
            .sort_index().sort_index(axis=1))


def series_stocks(panel: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Series de stock: viv (completa), sal y par (con NaN en 2014/2024-25)."""
    piv = lambda col: (panel.pivot(index="cod_ine", columns="anio", values=col)
                       .sort_index().sort_index(axis=1))
    sal_cnt = piv("centros_de_salud")
    par_cnt = piv("paradas_autobus")
    sal = sal_cnt + piv("consultorios_locales")
    par = par_cnt + piv("estaciones_metro") + piv("estaciones_cercanias")
    # los años ENTEROS sin dato quedan NaN (no 0): no son "cero real"
    sal = sal.where(sal_cnt.notna())
    par = par.where(par_cnt.notna())
    return {"viv": piv("unidades_urbanas_residencial"), "sal": sal, "par": par}


def g_log(s: pd.Series) -> pd.Series:
    """Escala del stock: ln(1 + stock). Permite stocks 0 con CAGRs finitos."""
    return np.log1p(s.astype(float).clip(lower=0))


def _back_cagr(g: pd.Series, t: int, k: int) -> float | None:
    """CAGR anualizado hacia atrás sobre g: t′ = último año disponible ≤ t−k;
    d = span real (t − t′); devueñe (g[t] − g[t′]) / d. None si no hay t′."""
    ref = None
    for y in g.index[g.index < t]:
        if y <= t - k:
            ref = y
    if ref is None:
        return None
    d = t - ref
    if d <= 0:
        return None
    return float((g[t] - g[ref]) / d)


def features_en_t(stock: pd.Series, pob: pd.Series, t: int) -> dict | None:
    """Features de UN stock en el año base t; None si el año no es utilizable."""
    if t not in stock.index or pd.isna(stock[t]) or float(stock[t]) < 0:
        return None
    if t not in pob.index or pd.isna(pob[t]) or float(pob[t]) <= 0:
        return None
    if t < ANIO_MIN_POB_5 or pd.isna(pob.get(t - 5)):
        return None

    g = g_log(stock[stock.notna()])     # años disponibles del stock
    if t not in g.index:
        return None
    c1, c3, c5, c10 = (_back_cagr(g, t, k) for k in (1, 3, 5, 10))
    if None in (c1, c3, c5, c10):
        return None
    diffs = g[g.index <= t].diff().dropna().values[-5:]
    vol5 = float(np.std(diffs, ddof=1)) if len(diffs) >= 2 else 0.0

    # CAGR poblacional 5 años en t (la serie de población está completa)
    c5p = float((float(pob[t]) / float(pob[t - 5])) ** (1 / 5) - 1)

    f = float(stock[t])
    return {
        "log_st": float(np.log(f + 1.0)),
        "st_cagr_1": c1,
        "st_cagr_3": c3,
        "st_cagr_5": c5,
        "st_cagr_10": c10,
        "st_vol_5": vol5,
        "st_p1000": f / float(pob[t]) * 1000.0,
        "log_pob": float(np.log(float(pob[t]))),
        "pob_cagr_5": c5p,
    }


def construir_dataset_m7(panel: pd.DataFrame) -> pd.DataFrame:
    """Filas (municipio, stock, t, h) para M7_VIVIENDAS / M7_SALUD / M7_PARADAS."""
    stocky = series_stocks(panel)
    pob = serie_pob(panel)
    filas: list[dict] = []
    for clave in STOCKS:
        stock = stocky[clave]
        for cod in stock.index:
            st, pb = stock.loc[cod], pob.loc[cod]
            for t in [int(y) for y in st.index if not pd.isna(st[y])]:
                f = features_en_t(st, pb, t)
                if f is None:
                    continue
                g = g_log(st)
                for h in range(1, (HORIZONTE_MAX_M7 + 1)):
                    destino = t + h
                    if destino not in st.index or pd.isna(st[destino]):
                        continue
                    fila = dict(f)
                    fila.update({
                        "cod_ine": cod,
                        "stock": clave,
                        "anio_base": int(t),
                        "horizonte": int(h),
                        TARGET_M7: float(g[destino] - g[t]),
                    })
                    filas.append(fila)
    df = pd.DataFrame(filas)
    return df.dropna(subset=FEATURES_M7 + [TARGET_M7]).reset_index(drop=True)


def construir_dataset_esc(panel: pd.DataFrame, municipios: pd.DataFrame) -> pd.DataFrame:
    """Cohorte cross-sectional para M7_ESCUELAS (una fila por municipio)."""
    pob = panel.sort_values(["cod_ine", "anio"]).groupby("cod_ine").tail(1)
    est = municipios.rename(columns={"distancia_centro_km": "distancia_sol_km"})
    df = est.merge(
        pob[["cod_ine", "poblacion_total", "edad_media", "pct_poblacion_menor_15",
             "pct_poblacion_65_mas", "paro_por_100_hab"]],
        on="cod_ine", how="left",
    )
    df["log_pob"] = np.log(df["poblacion_total"].astype(float).clip(lower=1))
    return df[["cod_ine", TARGET_M7_ESC] + FEATURES_M7_ESC].dropna().reset_index(drop=True)


PREFIJO_M7 = {"viv": "VIV", "sal": "SAL", "par": "PAR"}


def features_despliegue_series(panel: pd.DataFrame) -> pd.DataFrame:
    """Features de DESPLIEGUE: una fila por municipio con las columnas prefijadas.

    Por stock se evalua en su t_dep (último año con dato del stock: 2025 viv,
    2024 salud, 2023 paradas); si el año faltara se usa el último disponible
    y {P}_T_DEPLOY lo declara. Columns:
        {P}_LOG_POB {P}_LOG_ST {P}_CAGR_1 {P}_CAGR_3 {P}_CAGR_5 {P}_CAGR_10
        {P}_VOL_5 {P}_P1000 {P}_POB_CAGR_5 {P}_T_DEPLOY
    (el orden consumo en SQL se combina con FEATURES_M7).
    """
    stocky = series_stocks(panel)
    pob = serie_pob(panel)
    filas: list[dict] = []
    for cod in sorted(stocky["viv"].index):
        fila: dict = {"cod_ine": cod}
        for clave in STOCKS:
            stock = stocky[clave].loc[cod]
            pb = pob.loc[cod]
            disponibles = [int(y) for y in stock.index if not pd.isna(stock[y])]
            if not disponibles:
                continue
            t_dep = MODELOS_SERIE[clave]["t_dep"]
            t_uso = max(disponibles) if t_dep not in disponibles else t_dep
            f = features_en_t(stock, pb, t_uso)
            if f is None:
                continue
            pref = PREFIJO_M7[clave]
            fila.update({
                f"{pref}_LOG_POB": f["log_pob"],
                f"{pref}_LOG_ST": f["log_st"],
                f"{pref}_CAGR_1": f["st_cagr_1"],
                f"{pref}_CAGR_3": f["st_cagr_3"],
                f"{pref}_CAGR_5": f["st_cagr_5"],
                f"{pref}_CAGR_10": f["st_cagr_10"],
                f"{pref}_VOL_5": f["st_vol_5"],
                f"{pref}_P1000": f["st_p1000"],
                f"{pref}_POB_CAGR_5": f["pob_cagr_5"],
                f"{pref}_T_DEPLOY": t_uso,
            })
        filas.append(fila)
    return pd.DataFrame(filas)


def X_y(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Par (features, target) del modelo de crecimiento."""
    return df[FEATURES_M7].astype(float), df[TARGET_M7].astype(float)


def X_esc_y(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Par (features, target) de M7_ESCUELAS."""
    return df[FEATURES_M7_ESC].astype(float), df[TARGET_M7_ESC].astype(float)
