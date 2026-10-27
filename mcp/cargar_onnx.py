"""Carga los modelos ONNX en Oracle y valida paridad con onnxruntime.

Modelos creados:
    M3_DEMOGRAFIA           (1 salida: log de crecimiento — aplicar EXP())
    M4_CAPACIDAD_DEM/VIV/SER/ACC/EMP (5 ficheros de una salida, por dimensión)

Por qué M4 son 5 ficheros: IMPORT_ONNX_MODEL exige tensor de salida de
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
from src.common.oracle import conectar  # noqa: E402

DIR = REPO / "oracle_db" / "models"
FICHA_M3 = json.loads((DIR / "m3_demografia.json").read_text(encoding="utf-8"))
FICHA_M4 = json.loads((DIR / "m4_capacidad.json").read_text(encoding="utf-8"))

FEATS_M3 = FICHA_M3["features"]
FEATS_M4 = FICHA_M4["features"]

SALIDAS_M4 = {k: v.upper() for k, v in FICHA_M4["modelos_oracle"].items()}

MODELOS = []
for nombre in ["M3_DEMOGRAFIA"] + list(SALIDAS_M4.values()):
    mt = "m3" if nombre == "M3_DEMOGRAFIA" else "m4"
    feats = FEATS_M3 if mt == "m3" else FEATS_M4
    fichero = f"{nombre.lower()}.onnx"
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
    print("[cargar] los 6 modelos importados OK")

    # ─── Paridad: PREDICTION en base vs onnxruntime con el mismo vector ───
    # Estado 2025 del municipio 28001 (Acebeda, La) como lo tiene PV_BASE_M3_M4.
    with conn.cursor() as c:
        c.execute("SELECT * FROM PV_BASE_M3_M4 WHERE COD_INE = '28001'")
        cols = [d[0].lower() for d in c.description]
        fila = dict(zip(cols, c.fetchone()))

    # M3: features + horizonte 5. Los binds entran por nombre de feature.
    v3 = {f.upper(): (fila.get(f.lower()) or 0.0) for f in FEATS_M3[:-1]}
    v3["HORIZONTE"] = 5.0
    usando = ", ".join(f":{k} AS {k}" for k in v3)
    db = q(f"SELECT PREDICTION(M3_DEMOGRAFIA USING {usando}) FROM dual", v3)[0][0]
    db = float(db)
    sess = ort.InferenceSession(str(DIR / "m3_demografia.onnx"), providers=["CPUExecutionProvider"])
    rt = float(
        sess.run(None, {sess.get_inputs()[0].name: np.array([[v3[f.upper()] for f in FEATS_M3]], dtype=np.float32)})[0].ravel()[0]
    )
    print(f"[paridad M3] log(factor)  db={db:.6f}  runtime={rt:.6f}  diff={abs(db - rt):.2e}")
    assert abs(db - rt) < 1e-5

    # M4: los 5 sub-modelos con un vector ficticio de estado municipal
    v4 = {
        "LOG_POB": 7.5, "SALUD_10K": 4.0, "ESCUELAS_1000": 0.8, "PARADAS_1000": 5.0,
        "TELEFONO_1000": 30.0, "VIV_1000": 600.0, "CREC_10Y_PCT": 0.005,
        "PCT_MENOR_15": 15.0, "PCT_65MAS": 18.0, "REEMPLAZAMIENTO": 0.3,
        "PARO_100": 6.0, "VAR_PARO": -2.0, "TIEMPO_CENTRO_MIN": 25.0, "DISTANCIA_SOL_KM": 30.0,
    }
    usando4 = ", ".join(f":{k} AS {k}" for k in v4)
    for fichero, nombre in zip(
        ["m4_capacidad_dem.onnx", "m4_capacidad_viv.onnx", "m4_capacidad_ser.onnx", "m4_capacidad_acc.onnx", "m4_capacidad_emp.onnx"],
        ["M4_CAPACIDAD_DEM", "M4_CAPACIDAD_VIV", "M4_CAPACIDAD_SER", "M4_CAPACIDAD_ACC", "M4_CAPACIDAD_EMP"],
    ):
        db = q(f"SELECT PREDICTION({nombre} USING {usando4}) FROM dual", v4)[0][0]
        db = float(db)
        sess = ort.InferenceSession(str(DIR / fichero), providers=["CPUExecutionProvider"])
        rt = float(sess.run(None, {sess.get_inputs()[0].name: np.array([[v4[f.upper()] for f in FEATS_M4]], dtype=np.float32)})[0].ravel()[0])
        print(f"[paridad {nombre}] db={db:.4f}  runtime={rt:.4f}  diff={abs(db - rt):.2e}")
        assert abs(db - rt) < 1e-5

    print("[cargar] PARIDAD OK — lo que predice Oracle coincide con local")


if __name__ == "__main__":
    main()
