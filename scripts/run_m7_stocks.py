"""M7 · Stocks — ejecuta TODO el pipeline: xlsx → features → entrenar → .onnx + fichas.

Salidas: oracle_db/models/m7_{viviendas,salud,paradas,escuelas}.onnx (+ .json)
y copias de fichas en doc/modelos/.

Uso:  python scripts/run_m7_stocks.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.m7_stocks.train_export import entrenar_escuelas, entrenar_stocks  # noqa: E402

if __name__ == "__main__":
    entrenar_stocks()
    entrenar_escuelas()
    print("[m7] pipeline completo OK")
