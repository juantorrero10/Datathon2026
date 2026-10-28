"""Carga los modelos ONNX en Oracle y valida paridad con onnxruntime.

Modelos creados:
    M1_DEMOGRAFIA           (1 salida: log de crecimiento — aplicar EXP())
    M2_CAPACIDAD_DEM/VIV/SER/ACC/EMP (5 ficheros de una salida, por dimensión)

Por qué M2 son 5 ficheros: IMPORT_ONNX_MODEL exige tensor de salida de
tamaño 1 para regresión (ORA-54431 con salida multi-dimension).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import onnxruntime as ort

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from src.common.dataset import cargar_municipios, cargar_panel  # noqa: E402
from src.common.oracle import conectar  # noqa: E402

DIR = REPO / "oracle_db" / "models"
FICHA_M3 = json.loads((DIR / "m1_demografia.json").read_text(encoding="utf-8"))
FICHA_M4 = json.loads((DIR / "m2_capacidad.json").read_text(encoding="utf-8"))

FEATS_M3 = FICHA_M3["features"]
FEATS_M2 = FICHA_M4["features"]
FICHA_M3V = json.loads((DIR / "m3_valor.json").read_text(encoding="utf-8"))
FEATS_M3V = FICHA_M3V["features"]

# M4: los tres de crecimiento comparten FEATURES_M4; escuelas es cross-sectional
FICHA_M4S = {}
for m in ("viviendas", "salud", "paradas", "escuelas"):
    FICHA_M4S[m] = json.loads((DIR / f"m4_{m}.json").read_text(encoding="utf-8"))
FEATS_M2S = FICHA_M4S["viviendas"]["features"]          # idéntico para los tres
FEATS_M2S_ESC = FICHA_M4S["escuelas"]["features"]

MODELOS_M4 = [
    ("M4_VIVIENDAS", "m4_viviendas.onnx", FEATS_M2S),
    ("M4_SALUD", "m4_salud.onnx", FEATS_M2S),
    ("M4_PARADAS", "m4_paradas.onnx", FEATS_M2S),
    ("M4_ESCUELAS", "m4_escuelas.onnx", FEATS_M2S_ESC),
]

SALIDAS_M2 = {k: v.upper() for k, v in FICHA_M4["modelos_oracle"].items()}

MODELOS = []
for nombre, fichero, feats in ([("M1_DEMOGRAFIA", "m1_demografia.onnx", FEATS_M3)]
                               + [(n, f"{n.lower()}.onnx", FEATS_M2) for n in SALIDAS_M2.values()]
                               + [("M3_VALOR", "m3_valor.onnx", FEATS_M3V)]
                               + [(n, f, feats) for n, f, feats in MODELOS_M4]):
    meta = json.dumps(
        {
            "function": "regression",
            "regressionOutput": "variable",
            "input": {"input": [f.upper() for f in feats]},
        }
    )
    p = DIR / fichero
    MODELOS.append(
        {
            "nombre": nombre,
            "fichero": p,
            "bytes": p.read_bytes(),
            "metadata": meta,
            "feats": feats,
        }
    )


def _importar(cur, m: dict) -> None:
    try:
        cur.execute(f"BEGIN dbms_data_mining.drop_model('{m['nombre']}'); END;")
    except Exception:
        pass
    cur.execute(
        "BEGIN dbms_data_mining.import_onnx_model(:n, :b, JSON(:m)); END;",
        n=m["nombre"], b=m["bytes"], m=m["metadata"],
    )


def main() -> None:
    conn = conectar()

    # limpieza de los nombres antiguos de la base (enumeración M3/M4/M6/M7)
    VIEJOS = ["M3_DEMOGRAFIA", "M4_CAPACIDAD_DEM", "M4_CAPACIDAD_VIV", "M4_CAPACIDAD_SER",
              "M4_CAPACIDAD_ACC", "M4_CAPACIDAD_EMP", "M6_VALOR",
              "M7_VIVIENDAS", "M7_SALUD", "M7_PARADAS", "M7_ESCUELAS"]
    with conn.cursor() as c:
        for viejo in VIEJOS:
            try:
                c.execute(f"BEGIN dbms_data_mining.drop_model('{viejo}'); END;")
                print(f"[cargar] DROP {viejo} (nombre antiguo limpiado)")
            except Exception:
                pass
        conn.commit()

    def q(sql: str, args: dict | None = None):
        """Nueva cursor por consulta (los context manager cierran el cursor)."""
        with conn.cursor() as c:
            c.execute(sql, args or {})
            return c.fetchall()

    cur = conn.cursor()
    for m in MODELOS:
        print(f"[cargar] importando {m['nombre']} ({len(m['bytes']):,} bytes) ...")
        _importar(cur, m)
    conn.commit()
    cur.close()
    print(f"[cargar] los {len(MODELOS)} modelos importados OK")

    # ─── Paridad: PREDICTION en base vs onnxruntime con el mismo vector ───
    # Estado 2025 del municipio 28001 (Acebeda, La) como lo tiene PV_BASE_MODELOS.
    with conn.cursor() as c:
        c.execute("SELECT * FROM PV_BASE_MODELOS WHERE COD_INE = '28001'")
        cols = [d[0].lower() for d in c.description]
        fila = dict(zip(cols, c.fetchone()))

    # M1: features + horizonte 5. Los binds entran por nombre de feature.
    v3 = {f.upper(): (fila.get(f.lower()) or 0.0) for f in FEATS_M3[:-1]}
    v3["HORIZONTE"] = 5.0
    usando = ", ".join(f":{k} AS {k}" for k in v3)
    db = q(f"SELECT PREDICTION(M1_DEMOGRAFIA USING {usando}) FROM dual", v3)[0][0]
    db = float(db)
    sess = ort.InferenceSession(str(DIR / "m1_demografia.onnx"), providers=["CPUExecutionProvider"])
    rt = float(
        sess.run(None, {sess.get_inputs()[0].name: np.array([[v3[f.upper()] for f in FEATS_M3]], dtype=np.float32)})[0].ravel()[0]
    )
    print(f"[paridad M1] log(factor)  db={db:.6f}  runtime={rt:.6f}  diff={abs(db - rt):.2e}")
    assert abs(db - rt) < 1e-5

    # M2: los 5 sub-modelos con un vector ficticio de estado municipal
    v4 = {
        "LOG_POB": 7.5, "SALUD_10K": 4.0, "ESCUELAS_1000": 0.8, "PARADAS_1000": 5.0,
        "TELEFONO_1000": 30.0, "VIV_1000": 600.0, "CREC_10Y_PCT": 0.005,
        "PCT_MENOR_15": 15.0, "PCT_65MAS": 18.0, "REEMPLAZAMIENTO": 0.3,
        "PARO_100": 6.0, "VAR_PARO": -2.0, "TIEMPO_CENTRO_MIN": 25.0, "DISTANCIA_SOL_KM": 30.0,
    }
    usando4 = ", ".join(f":{k} AS {k}" for k in v4)
    for fichero, nombre in zip(
        ["m2_capacidad_dem.onnx", "m2_capacidad_viv.onnx", "m2_capacidad_ser.onnx", "m2_capacidad_acc.onnx", "m2_capacidad_emp.onnx"],
        ["M2_CAPACIDAD_DEM", "M2_CAPACIDAD_VIV", "M2_CAPACIDAD_SER", "M2_CAPACIDAD_ACC", "M2_CAPACIDAD_EMP"],
    ):
        db = q(f"SELECT PREDICTION({nombre} USING {usando4}) FROM dual", v4)[0][0]
        db = float(db)
        sess = ort.InferenceSession(str(DIR / fichero), providers=["CPUExecutionProvider"])
        rt = float(sess.run(None, {sess.get_inputs()[0].name: np.array([[v4[f.upper()] for f in FEATS_M2]], dtype=np.float32)})[0].ravel()[0])
        print(f"[paridad {nombre}] db={db:.4f}  runtime={rt:.4f}  diff={abs(db - rt):.2e}")
        assert abs(db - rt) < 1e-5

    # M3: vector real del dataset de entrenamiento (municipio 28001, t=2024, h=1)
    from src.m3_valor.features import construir_dataset_m3
    d3v = construir_dataset_m3(cargar_panel(), cargar_municipios())
    fila3v = d3v[(d3v["cod_ine"] == "28001") & (d3v["anio_base"] == 2024) & (d3v["horizonte"] == 1)].iloc[0]
    v4v = {f.upper(): float(fila3v[f]) for f in FEATS_M3V}
    usando4v = ", ".join(f":{k} AS {k}" for k in v4v)
    db4 = q(f"SELECT PREDICTION(M3_VALOR USING {usando4v}) FROM dual", v4v)[0][0]
    db4 = float(db4)
    sess4v = ort.InferenceSession(str(DIR / "m3_valor.onnx"), providers=["CPUExecutionProvider"])
    rt4 = float(sess4v.run(None, {sess4v.get_inputs()[0].name: np.array([[v4v[f.upper()] for f in FEATS_M3V]], dtype=np.float32)})[0].ravel()[0])
    print(f"[paridad M3_VALOR] log(factor)  db={db4:.6f}  runtime={rt4:.6f}  diff={abs(db4 - rt4):.2e}")
    assert abs(db4 - rt4) < 1e-5

    # ─── M4 · paridad contra el vector de despliegue REAL de PV_BASE_MODELOS ───
    m4_map_feat = {
        "LOG_ST": "LOG_ST", "ST_CAGR_1": "CAGR_1", "ST_CAGR_3": "CAGR_3",
        "ST_CAGR_5": "CAGR_5", "ST_CAGR_10": "CAGR_10", "ST_VOL_5": "VOL_5",
        "ST_P1000": "P1000", "LOG_POB": "LOG_POB", "POB_CAGR_5": "POB_CAGR_5",
    }
    pre = {"M4_VIVIENDAS": "VIV", "M4_SALUD": "SAL", "M4_PARADAS": "PAR"}
    for nombre, fichero, feats in MODELOS_M4:
        if nombre == "M4_ESCUELAS":
            continue
        v4v = {}
        for f in feats:
            if f == "horizonte":
                v4v["HORIZONTE"] = 5.0
                continue
            src = m4_map_feat[f.upper()]
            v4v[f.upper()] = float(fila[f"{pre[nombre]}_{src}".lower()] or 0.0)
        usando4v = ", ".join(f":{k} AS {k}" for k in v4v)
        db4 = float(q(f"SELECT PREDICTION({nombre} USING {usando4v}) FROM dual", v4v)[0][0])
        sess4v = ort.InferenceSession(str(DIR / fichero), providers=["CPUExecutionProvider"])
        rt4 = float(sess4v.run(None, {sess4v.get_inputs()[0].name: np.array([[v4v[f.upper()] for f in feats]], dtype=np.float32)})[0].ravel()[0])
        print(f"[paridad {nombre}] log(factor)  db={db4:.6f}  runtime={rt4:.6f}  diff={abs(db4 - rt4):.2e}")
        assert abs(db4 - rt4) < 1e-5

    # M4_ESCUELAS: cross-sectional sobre la fila base 28001
    v4ve = {f.upper(): float(fila.get(f.lower()) or 0.0) for f in FEATS_M2S_ESC}
    usando4ve = ", ".join(f":{k} AS {k}" for k in v4ve)
    db4e = float(q("SELECT PREDICTION(M4_ESCUELAS USING " + usando4ve + ") FROM dual", v4ve)[0][0])
    sess4ve = ort.InferenceSession(str(DIR / "m4_escuelas.onnx"), providers=["CPUExecutionProvider"])
    rt4e = float(sess4ve.run(None, {sess4ve.get_inputs()[0].name: np.array([[v4ve[f.upper()] for f in FEATS_M2S_ESC]], dtype=np.float32)})[0].ravel()[0])
    print(f"[paridad M4_ESCUELAS] escuelas esperadas  db={db4e:.6f}  runtime={rt4e:.6f}  diff={abs(db4e - rt4e):.2e}")
    assert abs(db4e - rt4e) < 1e-5

    print("[cargar] PARIDAD OK — lo que predice Oracle coincide con local")


if __name__ == "__main__":
    main()
