"""M7 · Stocks — entrenamiento, export ONNX y validación (4 modelos).

Salidas:
    oracle_db/models/m7_viviendas.onnx + m7_viviendas.json   (ficha)
    oracle_db/models/m7_salud.onnx     + m7_salud.json
    oracle_db/models/m7_paradas.onnx   + m7_paradas.json
    oracle_db/models/m7_escuelas.onnx  + m7_escuelas.json
    (copias de las fichas en doc/modelos/)

Contrato:
    M7_VIVIENDAS / M7_SALUD / M7_PARADAS (crecimiento, esquema M3):
        ENTRADA  10 floats (FEATURES_M7, orden posicional)
        SALIDA   1 float = log_factor del stock en escala log1p:
                  log(stock(t+h)+1) - log(stock(t)+1). El consumidor aplica
                  EXP() y compone geometricamente para h > 5.
    M7_ESCUELAS (cross-sectional):
        ENTRADA  6 floats (FEATURES_M7_ESC)
        SALIDA   1 float = escuelas esperadas (conteo continuo).
"""

from __future__ import annotations

import datetime as dt
import json

import numpy as np
import onnxruntime as ort
import sklearn
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import GroupShuffleSplit

from src.common.dataset import (
    DIR_DOC,
    DIR_MODELOS,
    XLSX,
    cargar_municipios,
    cargar_panel,
    sha256_archivo,
)
from src.m7_stocks.features import (
    FEATURES_M7,
    FEATURES_M7_ESC,
    MODELOS_SERIE,
    construir_dataset_esc,
    construir_dataset_m7,
    X_esc_y,
    X_y,
)

TARGET_OPSET = 17


def _export_onnx(model, n_features: int) -> bytes:
    """Export skl2onnx conValueInfo (None, n) en entrada y (N,1) en salida."""
    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import FloatTensorType

    onx = convert_sklearn(
        model,
        initial_types=[("input", FloatTensorType([None, n_features]))],
        target_opset=TARGET_OPSET,
    )
    import onnx

    salida = onx.graph.output[0]
    tipo = salida.type.tensor_type
    del tipo.shape.dim[:]
    origen = tipo.shape.dim.add()
    origen.dim_param = "N"
    destino = tipo.shape.dim.add()
    destino.dim_value = 1
    return onx.SerializeToString()


def _ficha(model, name, tarea, contrato, fea, fea_despliegue, model_params,
           dataset_info, metas, extra) -> dict:
    return {
        "modelo": name,
        "fecha": dt.datetime.now().isoformat(timespec="seconds"),
        "version_sklearn": sklearn.__version__,
        "dataset": dataset_info,
        "tarea": tarea,
        "contrato_salida": contrato,
        "features": fea,
        "columnas_despliegue": fea_despliegue,
        "orden_features": "posicional",
        "parametros": model_params,
        "metricas": metas,
        "extra": extra,
        "hash_dataset": sha256_archivo(XLSX),
    }


def _validar_onnx(name, model, onnx_bytes, X_all) -> float:
    p_onnx = DIR_MODELOS / f"{name}.onnx"
    p_onnx.parent.mkdir(parents=True, exist_ok=True)
    p_onnx.write_bytes(onnx_bytes)
    sess = ort.InferenceSession(str(p_onnx), providers=["CPUExecutionProvider"])
    entrada = sess.get_inputs()[0].name
    pred_onnx = sess.run(None, {entrada: X_all.astype(np.float32)})[0].ravel()
    pred_skl = model.predict(X_all.astype(np.float32))
    diff = float(np.max(np.abs(pred_onnx - pred_skl)))
    escala = float(np.max(np.abs(pred_skl)))
    check = diff / (escala + 1e-12)
    assert check < 1e-5, f"{name}: ONNX difiere de sklearn rel={check:.2e}"
    return check


def entrenar_stocks() -> list[dict]:
    """M7_VIVIENDAS / M7_SALUD / M7_PARADAS (esquema M3, GB regressor)."""
    panel = cargar_panel()
    data = construir_dataset_m7(panel)
    fichero_hash = sha256_archivo(XLSX)
    fichas = []

    for clave in ("viv", "sal", "par"):
        d = data[data["stock"] == clave]
        name = f"m7_{MODELOS_SERIE[clave]['nombre']}"
        X, y = X_y(d)
        grupos = d["cod_ine"].values
        tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=2026).split(X, y, grupos))
        Xtr, ytr, Xte, yte = X.iloc[tr], y.iloc[tr], X.iloc[te], y.iloc[te]

        model = GradientBoostingRegressor(
            n_estimators=400, learning_rate=0.05, max_depth=3, subsample=0.9, random_state=2026,
        )
        model.fit(Xtr, ytr)

        pred_tr = model.predict(Xtr); pred_te = model.predict(Xte)
        fac_real_te = np.exp(yte.values); fac_sim_te = np.exp(pred_te)

        X_all = X.values.astype(np.float32)
        check_onnx = _validar_onnx(name, model, _export_onnx(model, len(FEATURES_M7)), X_all)

        # por horizonte: error mediano del factor predecido y sesgo (mediana del
        #   factor_S/fac_real - 1) — CVE es lo que el mapa compone
        por_h = {}
        dte = d.iloc[te]
        mask_h = dte["horizonte"].values
        for h in sorted(set(mask_h)):
            sel = mask_h == h
            err = np.abs(fac_sim_te[sel] - fac_real_te[sel]) / np.maximum(fac_real_te[sel], 1e-9) * 100
            sesgo = float(np.median(fac_sim_te[sel] / np.maximum(fac_real_te[sel], 1e-9) - 1))
            por_h[int(h)] = {
                "mediana_abs_pct": float(np.median(err)),
                "sesgo_absorber_pct": round(sesgo * 100, 4),
            }

        fea_despliegue = [
            f"{s}_{c}" for s in (clave.upper(),)
            for c in ("LOG_POB", "LOG_ST", "CAGR_1", "CAGR_3", "CAGR_5", "CAGR_10",
                      "VOL_5", "P1000", "POB_CAGR_5", "T_DEPLOY")
        ]
        ficha = _ficha(
            model, name,
            tarea=f"Factor de crecimiento del stock {MODELOS_SERIE[clave]['cols']} a horizonte h (1..5)",
            contrato="log_factor en escala log1p: EXP(pred) ** (h/h_model) recompone; h_model=5 max",
            fea=FEATURES_M7, fea_despliegue=fea_despliegue,
            model_params=model.get_params(),
            dataset_info={
                "fichero": XLSX.name, "sha256": fichero_hash,
                "col_stock": MODELOS_SERIE[clave]["cols"],
                "t_despliegue": MODELOS_SERIE[clave]["t_dep"],
                "filas_entrenamiento": int(len(Xtr)),
                "filas_test": int(len(Xte)),
                "anios_sampleados": sorted(d["anio_base"].unique().tolist()),
                "split": "GroupShuffleSplit por municipio (test 20 %, semilla 2026)",
            },
            metas={
                "mae_log_test": float(np.abs(pred_te - yte.values).mean()),
                "mae_log_train": float(np.abs(pred_tr - ytr.values).mean()),
                "error_absoluto_mediano_pct_test": float(np.median(np.abs((fac_sim_te - fac_real_te) / np.maximum(fac_real_te, 1e-9)) * 100)),
                "por_horizonte": por_h,
                "paridad_onnx_sklearn_rel": check_onnx,
            },
            extra={
                "semantica_stock": "log1p (ln(1+stock)): pemite stocks 0; el inverso es stock(t+h) = (1+stock_base)*EXP(pred)**(h/h_model) - 1",
                "keys_horizonte": "h_model = LEAST(h, 5); para h>5 el consumidor compone EXP(pred(5))**(h/5)",
            },
        )
        DIR_DOC.mkdir(parents=True, exist_ok=True)
        (DIR_MODELOS / f"{name}.json").write_text(json.dumps(ficha, indent=2, ensure_ascii=False), encoding="utf-8")
        (DIR_DOC / f"{name}.json").write_text(json.dumps(ficha, indent=2, ensure_ascii=False), encoding="utf-8")
        fichas.append(ficha)
        print(f"[m7] {name}: test mediana |err|% = "
              f"{ficha['metricas']['error_absoluto_mediano_pct_test']:.2f}% "
              f"| filas tr/te {len(Xtr)}/{len(Xte)}")

    return fichas


def entrenar_escuelas() -> dict:
    """M7_ESCUELAS: cross-sectional (sin serie temporal)."""
    panel = cargar_panel()
    municipios = cargar_municipios()
    data = construir_dataset_esc(panel, municipios)

    X, y = X_esc_y(data)
    Xtr, Xte = X.iloc[: int(len(X) * 0.8)], X.iloc[int(len(X) * 0.8):]
    ytr, yte = y.iloc[: int(len(y) * 0.8)], y.iloc[int(len(y) * 0.8):]

    model = RandomForestRegressor(n_estimators=300, min_samples_leaf=2, random_state=2026)
    model.fit(Xtr, ytr)

    pred_te = model.predict(Xte)
    X_all = X.values.astype(np.float32)
    check_onnx = _validar_onnx("m7_escuelas", model, _export_onnx(model, len(FEATURES_M7_ESC)), X_all)

    ficha = _ficha(
        model, "m7_escuelas",
        tarea="Escuelas esperadas dado el tamaño (cross-sectional; sin serie temporal)",
        contrato="salida = escuelas esperadas (conteos continuos); el consumidor lo divide por pob para /1k",
        fea=FEATURES_M7_ESC, fea_despliegue=[
            "LOG_POB (SQL: LN(poblacion proyectada por M3))",
            "EDAD_MEDIA, PCT_MENOR_15, PCT_65MAS, DISTANCIA_SOL_KM, TIEMPO_CENTRO_MIN (estáticos de PV_BASE_M3_M4)",
        ],
        model_params=model.get_params(),
        dataset_info={
            "fichero": XLSX.name, "sha256": sha256_archivo(XLSX),
            "nota_dato": "escuelas: solo corte estático; 23/155 municipios con 0 escuelas en xlsx",
            "filas_entrenamiento": int(len(Xtr)), "filas_test": int(len(Xte)),
            "split": "iloc 80/20 (cohortes establecidas)",
        },
        metas={
            "mae_test_escuelas": float(np.abs(pred_te - yte.values).mean()),
            "mediana_abs_err_test": float(np.median(np.abs(pred_te - yte.values))),
        },
        extra={
            "semantica": "no es una tasa de construcción; es el stock esperado por tamaño de municipio",
        },
    )
    (DIR_MODELOS / "m7_escuelas.json").write_text(json.dumps(ficha, indent=2, ensure_ascii=False), encoding="utf-8")
    (DIR_DOC / "m7_escuelas.json").write_text(json.dumps(ficha, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[m7] m7_escuelas: mae = {ficha['metricas']['mae_test_escuelas']:.2f} escuelas")
    return ficha


def main() -> None:
    entrenar_stocks()
    entrenar_escuelas()


if __name__ == "__main__":
    main()
