# Pueblos con vida — Simulador What-If (Datathon 2026)

Simulador de escenarios para los **155 municipios de la Comunidad de Madrid
con menos de 50.000 habitantes**, desplegado dentro de la aplicación APEX
**215 "Pueblos con vida"** (página 10, Perfil Institucional).

**La única interacción:** el usuario elige municipio + año + parámetros de
choque (habitantes, viviendas, centros de salud, escuelas, paradas) → pulsa
"Simular escenario" → los modelos **M3** (demografía) y **M4** (capacidad)
se ejecutan como ONNX **dentro de Oracle** → se pintan las métricas simuladas
(barras antes/después, semáforo, factor limitante). La simulación es
**efímera**: no se persiste en ninguna tabla.

> Si este municipio gana N habitantes y hacemos X inversión, ¿cómo queda su
> índice de vitalidad para el año Y? ¿Y qué se rompe primero?

## Reproducir los modelos

```bash
python scripts/run_m3_demografia.py   # → oracle_db/models/m3_demografia.onnx + ficha
python scripts/run_m4_capacidad.py    # → oracle_db/models/m4_capacidad_{dem,viv,ser,acc,emp}.onnx + ficha
python scripts/run_all.py             # los dos, en orden, y comprueba las salidas
```

Requisitos: Python con `pandas`, `scikit-learn`, `skl2onnx`, `onnx`,
`onnxruntime`. Único dato de entrada: `data/dataset_155_municipios_2010-2025.xlsx`
(fuentes oficiales INE / Comunidad de Madrid).

## Mapa del repositorio

| Carpeta | Qué contiene |
|---|---|
| `data/` | Único dataset de entrada (xlsx, 155 municipios × 2010-2025). **Tronco.** |
| `doc/` | Documentación maestra, fichas de modelos y legacy |
| `scripts/` | Ejecutables del pipeline: `run_m3_…`, `run_m4_…`, `run_all.py` |
| `src/` | Código Python: `common/`, `m3_demografia/`, `m4_capacidad/`, `m6_mapa/` (residual) y `deprecated/` (solo referencia) |
| `oracle_db/` | `models/` (ONNX + fichas) y `sql/` (estado base + `PV_SIMULA`, `PV_MAPA`, `PV_GEO_MUNIS`) |
| `mcp/` | Loaders del tronco hacia Oracle (estado base + carga ONNX) |
| `web/` | **Visor**: todo lo exclusivo de la app APEX 215 — front del Simulador/Mapa, exports e `backups/` con `sql_original.sql`. No es necesario para reproducir el tronco. |
| `visuals/` | PNGs y diagramas del análisis (mapas de calor, rankings, arquitectura) |
| `tests/` | Reservada para tests (pytest); hoy vacía |
| `wallet/` | Wallet de Oracle con credenciales (local, no versionado) |

> La pieza principal del proyecto son los modelos y el análisis de datos
> (`data/`, `src/`, `scripts/`, `oracle_db/`, `mcp/`). La carpeta `web/` es
> la capa de presentación (app APEX).

## Documentación

- **`doc/project_context.md`** — documento maestro: definición, decisión de
  modelos (M3 y M4 en ONNX; M1/M2/M5 fuera), arquitectura N1→N3 y criterios
  de éxito.
- **`doc/estructura.md`** — inventario del repositorio fichero a fichero.
- `doc/modelos/` — fichas técnicas de M3 y M4 (copia para el jurado).
- `doc/legacy/` — borradores retirados (referencia histórica).

## Convenciones clave

1. Cadena oficial del tronco: `data/*.xlsx` → `scripts/run_*.py` →
   `oracle_db/models/*.onnx` → Oracle → `PV_SIMULA`/`PV_MAPA` → APEX.
2. Sin ficha JSON (`doc/modelos/…`) no se sube un modelo a Oracle.
3. La simulación es efímera: nada se persiste.
4. `web/backups/sql_original.sql` es el punto de restauración de la
   app 215: no se sobreescribe.
5. La caché del geo (`web/osm_raw_cm.json`) no va versionada.
