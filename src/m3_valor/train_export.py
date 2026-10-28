"""M3 · Valor catastral proyectado — entrenamiento, export ONNX y validación.

Salida:
    oracle_db/models/m3_valor.onnx
    oracle_db/models/m3_valor.json        (ficha del modelo)
    doc/modelos/m3_valor.json             (copia para el jurado)

Contrato del modelo:
    ENTRADA  (18 floats, FEATURES_M3, en ese orden)
    SALIDA   1 float = log( valor(t+h) / valor(t) )
             El consumidor aplica EXP() para obtener el factor de valor.
"""

from __future__ import annotations

import datetime as dt
import json

import numpy as np
import onnxruntime as ort
import sklearn
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GroupShuffleSplit

from src.common.dataset import (
    DIR_DOC,
    DIR_MODELOS,
    XLSX,
    cargar_municipios,
    cargar_panel,
    sha256_archivo,
)
from src.m3_valor.features import FEATURES_M3, construir_dataset_m3, X_y

MODELO = "m3_valor"
ONNX_PATH = DIR_MODELOS / f"{MODELO}.onnx"
TARGET_OPSET = 17


def _export_onnx(model, n_features: int) -> bytes:
    """Export con initial_types explícitos y ValueInfo de salida (N,1)."""
    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import FloatTensorType
    import onnx

    onx = convert_sklearn(
        model,
        initial_types=[("input", FloatTensorType([None, n_features]))],
        target_opset=TARGET_OPSET,
    )
    salida = onx.graph.output[0]
    tipo = salida.type.tensor_type
    del tipo.shape.dim[:]
    origen = tipo.shape.dim.add()
    origen.dim_param = "N"
    destino = tipo.shape.dim.add()
    destino.dim_value = 1
    aux = ONNX_PATH.parent / f"{MODELO}.tmp.onnx"
    aux.write_bytes(onx.SerializeToString())
    data = aux.read_bytes()
    aux.unlink()
    return data


def entrenar() -> dict:
    panel = cargar_panel()
    municipios = cargar_municipios()
    data = construir_dataset_m3(panel, municipios)

    X, y = X_y(data)
    grupos = data["cod_ine"].values

    # Hold-out por MUNICIPIO (el municipio nunca puede estar en train y test)
    tr, te = next(
        GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=2026).split(X, y, grupos)
    )
    Xtr, ytr, Xte, yte = X.iloc[tr], y.iloc[tr], X.iloc[te], y.iloc[te]

    model = GradientBoostingRegressor(
        n_estimators=400,
        learning_rate=0.05,
        max_depth=3,
        subsample=0.9,
        random_state=2026,
    )
    model.fit(Xtr, ytr)

    def errores(X_, y_):
        pred = model.predict(X_)
        factor_real = np.exp(y_.values)
        factor_sim = np.exp(pred)
        return pred - y_.values, (factor_sim - factor_real) / factor_real * 100

    err_te_log, err_te_pct = errores(Xte, yte)
    err_tr_log, err_tr_pct = errores(Xtr, ytr)

    # Export + validación ONNX <-> sklearn
    X_all = X.values.astype(np.float32)
    onx_bytes = _export_onnx(model, len(FEATURES_M3))
    DIR_MODELOS.mkdir(parents=True, exist_ok=True)
    ONNX_PATH.write_bytes(onx_bytes)

    sess = ort.InferenceSession(str(ONNX_PATH), providers=["CPUExecutionProvider"])
    pred_onnx = sess.run(None, {sess.get_inputs()[0].name: X_all})[0].ravel()
    pred_skl = model.predict(X_all)
    max_diff = float(np.max(np.abs(pred_onnx - pred_skl)))
    assert np.allclose(pred_onnx, pred_skl, rtol=1e-5, atol=1e-7), (
        f"ONNX difiere del modelo sklearn: max_diff={max_diff:.2e}"
    )

    # Error mediano del factor por horizonte (para la banda del mapa)
    te_ = data.iloc[te]
    factor_real, factor_sim = np.exp(yte.values), np.exp(model.predict(Xte))
    err_pct_h = {}
    for h in sorted(te_["horizonte"].unique()):
        mask = te_["horizonte"].values == h
        err_pct_h[int(h)] = float(
            np.median(np.abs((factor_sim[mask] - factor_real[mask]) / factor_real[mask]) * 100)
        )

    ficha = {
        "modelo": MODELO,
        "fecha": dt.datetime.now().isoformat(timespec="seconds"),
        "version_sklearn": sklearn.__version__,
        "dataset": {
            "fichero": XLSX.name,
            "sha256": sha256_archivo(XLSX),
            "filas_entrenamiento": int(len(Xtr)),
            "filas_test": int(len(Xte)),
            "split": "GroupShuffleSplit por municipio (test 20 %, semilla 2026)",
        },
        "tarea": "Factor de crecimiento del VALOR CATASTRAL RESIDENCIAL a horizonte h",
        "contrato_salida": "log(factor); el consumidor aplica EXP()",
        "features": FEATURES_M3,
        "orden_features": "posicional",
        "parametros": model.get_params(),
        "metricas": {
            "mae_log_test": float(np.abs(err_te_log).mean()),
            "error_absoluto_mediano_pct_test": float(np.median(np.abs(err_te_pct))),
            "mae_log_train": float(np.abs(err_tr_log).mean()),
            "error_absoluto_mediano_pct_por_horizonte": err_pct_h,
        },
        "validacion_onnx": {"max_abs_diff": max_diff},
        "declaraciones": [
            "El valor catastral es un proxy oficial del valor de la vivienda; NO es el precio de mercado",
            "Su crecimiento combina revision catastral (saltos) y mercado (tendencia)",
            "tiempo_centro_min con la misma imputacion lineal distancia-tiempo que M2 (99 municipios)",
            "Solo hay labels observadas hasta 2025; horizontes > 5 son extrapolacion declarada",
        ],
    }

    DIR_MODELOS.mkdir(parents=True, exist_ok=True)
    (DIR_MODELOS / f"{MODELO}.json").write_text(
        json.dumps(ficha, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    dir_doc = DIR_DOC / "modelos"
    dir_doc.mkdir(parents=True, exist_ok=True)
    (dir_doc / f"{MODELO}.json").write_text(
        json.dumps(ficha, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"[M3] muestras={len(X)} (train={len(Xtr)}, test={len(Xte)})")
    print(f"[M3] MAE log test = {ficha['metricas']['mae_log_test']:.4f} "
          f"| error mediano del factor (test) = {ficha['metricas']['error_absoluto_mediano_pct_test']:.2f} %")
    print(f"[M3] ONNX generado y validado: {ONNX_PATH}")
    return ficha


if __name__ == "__main__":
    entrenar()
