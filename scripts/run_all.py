"""Ejecuta los dos pipelines del proyecto en orden y comprueba la salida.

    python scripts/run_all.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
MODELOS = REPO / "oracle_db" / "models"

# M1 deja un único .onnx; M2 baja a la base como 5 ficheros (uno por dimensión);
# M3 (valor catastral proyectado, mapa) deja otro .onnx único; M4 (stocks
# proyectados: viviendas/salud/paradas + escuelas esperadas) deja otros 4.
EXITOS = [
    ("run_m1_demografia.py", ["m1_demografia.onnx"]),
    (
        "run_m2_capacidad.py",
        [
            "m2_capacidad_dem.onnx",
            "m2_capacidad_viv.onnx",
            "m2_capacidad_ser.onnx",
            "m2_capacidad_acc.onnx",
            "m2_capacidad_emp.onnx",
        ],
    ),
    ("run_m3_valor.py", ["m3_valor.onnx"]),
    (
        "run_m4_stocks.py",
        [
            "m4_viviendas.onnx",
            "m4_salud.onnx",
            "m4_paradas.onnx",
            "m4_escuelas.onnx",
        ],
    ),
]


def main() -> int:
    fallos = []
    for script, _ in EXITOS:
        print(f"\n=== {script} ===")
        r = subprocess.run([sys.executable, str(SCRIPTS / script)])
        if r.returncode != 0:
            fallos.append(script)
            print(f"[run_all] FALLÓ {script}")
            break
    print("\n=== RESULTADO ===")
    ok = True
    for script, ficheros in EXITOS:
        for onnx in ficheros:
            p = MODELOS / onnx
            existe = p.exists() and p.stat().st_size > 0
            print(f"  {'OK ' if existe else 'FALTA'}  {p}")
            ok &= existe
    return 0 if (ok and not fallos) else 1


if __name__ == "__main__":
    raise SystemExit(main())
