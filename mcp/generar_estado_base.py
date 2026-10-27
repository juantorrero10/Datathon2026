"""Genera y carga en Oracle la tabla de ESTADO BASE (corte 2025) que alimenta
PV_SIMULA v2: los features EXACTOS que consumen M3 y M4, calculados con el
mismo código del entrenamiento (paridad garantizada Python/SQL).

  - Genera:  oracle/sql/01_estado_base_m3_m4.sql   (DDL + INSERTs, referencia)
  - Ejecuta: DDL + INSERTs en la base (conexión local por wallet)

Columnas de PV_BASE_M3_M4:
  cod_ine, nombre, poblacion_2025,
  -- M3 (estado del año base 2025; el horizonte lo decide la consulta):
  log_pob, cagr_1, cagr_3, cagr_5, cagr_10, vol_5,
  edad_media, pct_menor_15, pct_65mas, reemplazamiento, paro_100, var_paro,
  migracion_3y, distancia_sol_km, tiempo_centro,
  -- M4 (ingredientes del estado; los ratios los forma PV_SIMULA al aplicar
  -- el choque del usuario y normalizar por población simulada):
  crec_10y_base (CAGR real ventana-invertida hasta 2025),
  centros_salud_num (centros + consultorios), consul...,
  escuelas (centros_educativos_alta), paradas_base (autobus+metro+cercanias),
  telefono (baf + atf), viv_stock (unidades_urbanas_residencial)
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import numpy as np

from src.common.dataset import cargar_panel, cargar_municipios
from src.common.oracle import conectar
from src.m4_capacidad.features import _estatica  # regla de imputación idéntica

SQL_OUT = REPO / "oracle_db" / "sql" / "01_estado_base_m3_m4.sql"

DDL = """
CREATE TABLE PV_BASE_M3_M4 (
    COD_INE            VARCHAR2(5) NOT NULL PRIMARY KEY,
    NOMBRE             VARCHAR2(120),
    POBLACION_2025     NUMBER,
    LOG_POB            NUMBER,
    CAGR_1             NUMBER,
    CAGR_3             NUMBER,
    CAGR_5             NUMBER,
    CAGR_10            NUMBER,
    VOL_5              NUMBER,
    EDAD_MEDIA         NUMBER,
    PCT_MENOR_15       NUMBER,
    PCT_65MAS          NUMBER,
    REEMPLAZAMIENTO    NUMBER,
    PARO_100           NUMBER,
    VAR_PARO           NUMBER,
    MIGRACION_3Y       NUMBER,
    DISTANCIA_SOL_KM   NUMBER,
    TIEMPO_CENTRO      NUMBER,
    CREC_10Y_BASE      NUMBER,
    CENTROS_SALUD_NUM  NUMBER,
    ESCUELAS           NUMBER,
    PARADAS_BASE       NUMBER,
    TELEFONO           NUMBER,
    VIV_STOCK          NUMBER
)
"""


def main(ejecutar: bool = True) -> None:
    panel = cargar_panel()
    municipios = cargar_municipios()

    estatica, imp = _estatica(municipios)
    estatica = estatica.set_index("cod_ine")

    serie = (
        panel.pivot(index="cod_ine", columns="anio", values="poblacion_total")
        .sort_index()
        .sort_index(axis=1)
    )
    anios = list(serie.columns)          # 2010..2025
    p25 = panel[panel["anio"] == 2025].set_index("cod_ine")

    filas = []
    def nz(x):
        try:
            xf = float(x)
            return 0.0 if xf != xf else xf
        except (TypeError, ValueError):
            return 0.0

    for cod, pob in serie.iterrows():
        crec = pob.pct_change()
        f = p25.loc[cod]
        pob25 = float(pob[2025])
        est = estatica.loc[cod]

        def cagr(w: int) -> float:
            return float((pob25 / pob[2025 - w]) ** (1 / w) - 1)

        migr = panel[(panel["cod_ine"] == cod) & (panel["anio"].between(2023, 2025))]["tasa_migracion"].mean()
        vol = crec.loc[2021:2025].std(ddof=1)

        # ── ÚLTIMO DATO DISPONIBLE por indicador de stock de servicios ──
        # El panel deja años enteros vacíos (sanidad: 2014 y 2025; transporte:
        # 2024-2025; telefonía: 2010-2011). Para el estado base 2025 tomamos
        # cada stock del último año observado (2024 salud, 2023 transporte,
        # 2025 telefonía), declarado en el fichero .sql de referencia.
        fila_salud = panel[(panel["cod_ine"] == cod) & (panel["anio"] == 2024)].iloc[0]
        fila_paradas = panel[(panel["cod_ine"] == cod) & (panel["anio"] == 2023)].iloc[0]
        fila_telefono = panel[(panel["cod_ine"] == cod) & (panel["anio"] == 2025)].iloc[0]

        migr_serie = panel[panel["cod_ine"] == cod].dropna(subset=["tasa_migracion"])["tasa_migracion"]
        migr = migr_serie.tail(3).mean()
        vol = crec.loc[2021:2025].std(ddof=1)

        filas.append(
            {
                "cod_ine": cod,
                "nombre": str(f["municipio"]),
                "poblacion_2025": pob25,
                "log_pob": float(np.log(pob25)),
                "cagr_1": cagr(1),
                "cagr_3": cagr(3),
                "cagr_5": cagr(5),
                "cagr_10": cagr(10),
                "vol_5": float(vol) if vol == vol else None,
                "edad_media": float(f["edad_media"]),
                "pct_menor_15": float(f["pct_poblacion_menor_15"]),
                "pct_65mas": float(f["pct_poblacion_65_mas"]),
                "reemplazamiento": float(f["proporcion_reemplazamiento"]),
                "paro_100": float(f["paro_por_100_hab"]),
                "var_paro": float(f["variacion_relativa_paro"]) if f["variacion_relativa_paro"] == f["variacion_relativa_paro"] else 0.0,
                "migracion_3y": float(migr) if migr == migr else 0.0,
                "distancia_sol_km": float(est["distancia_sol_km"]),
                "tiempo_centro": float(est["tiempo_centro_min"]),
                "crec_10y_base": cagr(min(10, 2025 - anios[0])),
                "centros_salud_num": nz(fila_salud["centros_de_salud"]) + nz(fila_salud["consultorios_locales"]),
                "escuelas": float(est["centros_educativos_alta"]),
                "paradas_base": nz(fila_paradas["paradas_autobus"]) + nz(fila_paradas["estaciones_metro"]) + nz(fila_paradas["estaciones_cercanias"]),
                "telefono": nz(fila_telefono["lineas_telefonicas_baf"]) + nz(fila_telefono["lineas_telefonicas_atf"]),
                "viv_stock": nz(f["unidades_urbanas_residencial"]),
            }
        )

    COLS = [k for k in filas[0]]

    # ── Fichero de referencia ──
    lineas = [f"-- Estado base 2025 para PV_SIMULA v2 (generado: {Path(__file__).name})", DDL]
    for f_ in filas:
        vals = ", ".join(
            ("NULL" if v is None or v != v else repr(float(v))) if k != "nombre"
            else "'" + str(v).replace("'", "''") + "'"
            for k, v in f_.items()
        )
        lineas.append(f"INSERT INTO PV_BASE_M3_M4 ({', '.join(COLS)}) VALUES ({vals});")
    SQL_OUT.parent.mkdir(parents=True, exist_ok=True)
    SQL_OUT.write_text("\n".join(lineas) + "\nCOMMIT;\n", encoding="utf-8")

    if not ejecutar:
        print(f"[base] generado {SQL_OUT} con {len(filas)} municipios (sin ejecutar)")
        return

    # ── Ejecución contra la base ──
    conn = conectar()
    with conn.cursor() as cur:
        try:
            cur.execute("DROP TABLE PV_BASE_M3_M4 PURGE")
        except Exception:
            pass
        cur.execute(DDL)
        bind = []
        for row in filas:
            b = {}
            for k, v in row.items():
                if isinstance(v, float) and v != v:
                    v = None
                b["c_" + k] = v
            bind.append(b)
        cur.executemany(
            "INSERT INTO PV_BASE_M3_M4 (" + ", ".join(COLS) + ") VALUES ("
            + ", ".join(":c_" + c for c in COLS) + ")",
            bind,
        )
        conn.commit()
    print(f"[base] PV_BASE_M3_M4 cargada: {len(filas)} municipios | imputación tiempo: {imp['n_imputados']} municipios")


if __name__ == "__main__":
    main(ejecutar=True)
