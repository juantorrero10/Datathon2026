"""M6 · Valor catastral proyectado — construcción de features.

Consumidor: el mapa proyectado (diferenciales 2025 -> año objetivo, capa de
valor de la vivienda para el inversor). Mismo esquema que M3: cada muestra es
un "momento de decisión" (municipio, año base t, horizonte h) con features
SOLO a fecha t; el target es el crecimiento logarítmico observado del VALOR
CATASTRAL RESIDENCIAL hasta t+h.

Serie completa (0 nulos, 2010-2025). El valor catastral es un proxy oficial
del valor de la vivienda: se declara que su crecimiento combina revisión
catastral (saltos) y mercado (tendencia), y que NO es el precio de mercado.

Salida del modelo: log(factor); el consumidor aplica EXP().
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.m4_capacidad.features import _estatica  # imputación de tiempo_centro idéntica

# Features finales, en el ORDEN EXACTO en que consume el ONNX.
FEATURES_M6 = [
    "log_valor",
    "vcagr_1",
    "vcagr_3",
    "vcagr_5",
    "vcagr_10",
    "vvol_5",
    "log_pob",
    "cagr_5",
    "vol_5",
    "edad_media",
    "pct_65mas",
    "reemplazamiento",
    "paro_100",
    "var_paro",
    "migracion_3y",
    "distancia_sol_km",
    "tiempo_centro_min",
    "horizonte",
]

TARGET_M6 = "log_factor_valor"


def construir_dataset_m6(panel: pd.DataFrame, municipios: pd.DataFrame) -> pd.DataFrame:
    """Filas (municipio, t, h): features a t, target log(valor(t+h)/valor(t)).

    Ventanas: el historial de valor y población exige serie completa desde
    2010, por lo que t empieza en 2020; h llega hasta 2025.
    """
    anios_obs = list(range(2010, 2026))
    valor = (
        panel.pivot(index="cod_ine", columns="anio", values="valor_catastral_residencial_miles_eur")
        .sort_index().sort_index(axis=1).loc[:, anios_obs]
    )
    pop = (
        panel.pivot(index="cod_ine", columns="anio", values="poblacion_total")
        .sort_index().sort_index(axis=1).loc[:, anios_obs]
    )
    assert not valor.isna().any().any(), "la serie de valor no puede tener huecos"
    assert not pop.isna().any().any(), "la serie de población no puede tener huecos"

    estatica, _ = _estatica(municipios)
    estatica = estatica.set_index("cod_ine")
    panel_idx = panel.set_index(["cod_ine", "anio"])

    filas = []
    for cod in valor.index:
        v, p = valor.loc[cod], pop.loc[cod]
        lv, lp = np.log(v), np.log(p)
        gv, gp = v.pct_change(), p.pct_change()
        est = estatica.loc[cod]
        for t in range(2020, 2026):
            if t + 1 > 2025:
                break
            h_max = 2025 - t
            base = {
                "log_valor": float(lv[t]),
                "vcagr_1": float(gv[t]),
                "vcagr_3": float((v[t] / v[t - 3]) ** (1 / 3) - 1),
                "vcagr_5": float((v[t] / v[t - 5]) ** (1 / 5) - 1),
                "vcagr_10": float((v[t] / v[t - 10]) ** (1 / 10) - 1),
                "vvol_5": float(gv.loc[t - 4: t].std(ddof=1)),
                "log_pob": float(lp[t]),
                "cagr_5": float((p[t] / p[t - 5]) ** (1 / 5) - 1),
                "vol_5": float(gp.loc[t - 4: t].std(ddof=1)),
                "edad_media": float(panel_idx.loc[(cod, t), "edad_media"]),
                "pct_65mas": float(panel_idx.loc[(cod, t), "pct_poblacion_65_mas"]),
                "reemplazamiento": float(panel_idx.loc[(cod, t), "proporcion_reemplazamiento"]),
                "paro_100": float(panel_idx.loc[(cod, t), "paro_por_100_hab"]),
                "var_paro": float(panel_idx.loc[(cod, t), "variacion_relativa_paro"]),
                "migracion_3y": float(
                    panel[(panel["cod_ine"] == cod) & (panel["anio"].between(t - 2, t))]["tasa_migracion"].mean()
                ),
                "distancia_sol_km": float(est["distancia_sol_km"]),
                "tiempo_centro_min": float(est["tiempo_centro_min"]),  # con imputación (99 munis)
            }
            for h in range(1, h_max + 1):
                fila = dict(base)
                fila["horizonte"] = h
                fila["cod_ine"] = cod
                fila["anio_base"] = t
                fila["anio_destino"] = t + h
                fila[TARGET_M6] = float(lv[t + h] - lv[t])
                filas.append(fila)

    df = pd.DataFrame(filas)
    df["migracion_3y"] = df["migracion_3y"].fillna(0.0)   # sin dato = 0 (media de los disponibles)
    df["var_paro"] = df["var_paro"].fillna(0.0)
    df = df.dropna(subset=FEATURES_M6 + [TARGET_M6]).reset_index(drop=True)
    return df


def X_y(df: pd.DataFrame):
    return df[FEATURES_M6].astype(float), df[TARGET_M6].astype(float)
