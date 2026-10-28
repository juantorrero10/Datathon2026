# MODELOS — M1 · M2 · M3 · M4

> Documentación técnica de los cuatro modelos del proyecto (lo que se entrena
> en `src/`, se exporta a `oracle_db/models/*.onnx` y se consume dentro de
> Oracle por `PV_SIMULA` (Simulador What-If, pág. 10) y `PV_MAPA` (Mapa, pág. 40).
> Fichas de referencia: `oracle_db/models/*.json` (y copias en `doc/modelos/`).
>
> **Anexo histórico:** la explicación anterior en `doc/legacy/`
> (`algoritmos_m3_m4_explicacion.docx`) describía la enumeración residual
> M3/M4/M6/M7 — renombrada a la actual M1/M2/M3/M4 el 29-oct-2026.

---

## Cómo se lee esta página

| Nº | Modelo | Qué proyecta/puntúa | Ficheros ONNX | Consumo |
|---|---|---|---|---|
| **M1** | Demografía | factor de crecimiento de la **población** a horizonte h | `m1_demografia.onnx` | `PV_MAPA` + `PV_SIMULA` |
| **M2** | Capacidad / Vitalidad | las **5 dimensiones** (0-100) de un estado municipal | `m2_capacidad_{dem,viv,ser,acc,emp}.onnx` | `PV_MAPA` + `PV_SIMULA` |
| **M3** | Valor (AVM) | factor de crecimiento del **valor catastral** a horizonte h | `m3_valor.onnx` | `PV_MAPA` |
| **M4** | Stocks proyectados | **construcción prevista**: viviendas, salud, paradas + escuelas esperadas | `m4_viviendas.onnx`, `m4_salud.onnx`, `m4_paradas.onnx`, `m4_escuelas.onnx` | `PV_MAPA` + `PV_SIMULA` |

Cadena de reprodución (todo desde el xlsx de la raíz de `data/`):

```bash
python scripts/run_m1_demografia.py   # → m1_demografia.onnx + ficha
python scripts/run_m2_capacidad.py    # → 5 × m2_capacidad_*.onnx + ficha
python scripts/run_m3_valor.py        # → m3_valor.onnx + ficha
python scripts/run_m4_stocks.py       # → 4 × m4_*.onnx + fichas
python scripts/run_all.py             # encadena los 4 (11 .onnx) y comprueba salidas
```

Regla de la casa: **sin ficha JSON no se sube un modelo a Oracle**
(`mcp/cargar_onnx.py` requiere las fichas y valida paridad
`PREDICTION(Oracle)` ↔ `onnxruntime` = 0.00e+00 antes de dar por válida la
carga).

---

## M1 · Demografía (crecimiento de población)

- **Tarea** (ficha `m1_demografia.json`): regresión del **factor de crecimiento
  poblacional** a horizonte h. Cada muestra es un "momento de decisión"
  `(municipio, año base t, horizonte h)`; todas las features se conocen en t.
- **Target**: `log( población(t+h) / población(t) )` — el consumidor aplica
  `EXP(PREDICTION(...))` para obtener el factor.
- **Features (10, orden posicional)**: `log_pob, cagr_1, cagr_3, cagr_5,
  cagr_10, vol_5, edad_media, pct_menor_15, pct_65mas, reemplazamiento,
  paro_100, var_paro, migracion_3y, distancia_sol_km, tiempo_centro_min,
  horizonte`.
- **Algoritmo**: `GradientBoostingRegressor` (400 árboles, lr 0.05, depth 3).
- **Split**: `GroupShuffleSplit` por MUNICIPIO (test 20 %, semilla 2026) — el
  municipio nunca está en train y test a la vez.
- **Métricas (test)**: MAE log 0.0174; **error mediano del factor 1.27 %**.
- **Consumo en SQL**:
  ```sql
  EXP(PREDICTION(M1_DEMOGRAFIA USING b.LOG_POB AS LOG_POB, ...,
                 :h AS HORIZONTE))
  ```
  Para horizontes h > 5 el factor se compone geométricamente:
  `EXP(pred(5))**(h/5)` (patrón común a M3 y M4).
- **Uso**: en `PV_MAPA` y `PV_SIMULA` da la **población base del año
  objetivo** (`POBLACION_2025 × factor`) y su banda (mediana |err| % del
  backtest por horizonte: 0.93 % (h1) … 2.20 % (h≥5)).

---

## M2 · Capacidad / Vitalidad (las 5 dimensiones)

- **Tarea** (ficha `m2_capacidad.json`): puntuar un estado municipal — 5
  dimensiones en 0-100 (demografía, vivienda, servicios, accesibilidad,
  empleo). Baja a la base como **5 ficheros ONNX** (uno por dimensión, salida
  escalar, requisito de Oracle).
- **Dataset**: 1.550 estados `(municipio × año)` con ratios de saturación
  (salud/10k, escuelas/1k, paradas/1k, teléfono/1k, viviendas/1k, crecimiento
  10y, demografía) + estática. **Saneo declarado**: se excluyen los años con
  indicadores vacíos del xlsx (telefonía 2010-11, sanidad 2014 y 2025,
  transporte 2024-25).
- **Targets**: las 5 dimensiones **recalculadas con la misma fórmula
  percent-rank que la app, por corte anual**.
- **Features (14)**: `log_pob, salud_10k, escuelas_1000, paradas_1000,
  telefono_1000, viv_1000, crec_10y_pct, pct_menor_15, pct_65mas,
  reemplazamiento, paro_100, var_paro, tiempo_centro_min, distancia_sol_km`.
- **Algoritmo**: `RandomForestRegressor` (uno por dimensión).
- **Métricas (test)**:

  | dim | MAE | Spearman |
  |---|---|---|
  | demografía | 2.68 | 0.987 |
  | vivienda | 1.39 | 0.998 |
  | servicios | 1.90 | 0.991 |
  | accesibilidad | 0.74 | 0.997 |
  | empleo | 9.82 | 0.826 |

- **Consumo en SQL**:
  `PREDICTION(M2_CAPACIDAD_DEM USING e.LOG_POB_Y AS LOG_POB, e.SALUD_10K_Y AS SALUD_10K, ...)` —
  los ratios del estado los monta el propio SQL (proyección + choque del
  usuario normalizado por población).
- **Uso**: las 5 dims alimentan el **índice ponderado** (0.20 / 0.15 / 0.25 /
  0.25 / 0.15) y el **factor limitante** (argmin de las 5 dims) en mapa y WI.

---

## M3 · Valor catastral (AVM)

- **Tarea** (ficha `m3_valor.json`): factor de crecimiento del **valor
  catastral residencial** a horizonte h (mismo esquema de M1: `t, h`).
- **Target**: `log( valor(t+h) / valor(t) )`.
- **Features**: log del valor, VCAGR 1/3/5/10, volatilidad 5 años, log pob,
  CAGR pob 5, edad media, pct 65+, reemplazamiento, paro.
- **Algoritmo**: `GradientBoostingRegressor`; split por municipio.
- **Métricas (test)**: MAE log 0.0205; **error mediano del factor 0.80 %**;
  por horizonte: 0.43 % (h1) … 1.80 % (h5).
- **Uso**: **sólo el mapa** — `d.FACTOR_M6`… (nombre interno en `PV_MAPA`;
  compuesto como `EXP(pred(5))**(h/5)` para h>5) da el valor proyectado del
  año objetivo (capa "ΔValor catastral").

---

## M4 · Stocks proyectados (construcción prevista)

Llegados aquí: el mapa/WI entregaba viviendas, centros de salud, paradas y
escuelas como stocks **fijos** (solo cambiaba la población al denominador), de
modo que esas capas "empeoraban" mecánicamente. **M4 introduce la pieza que
faltaba: cuánto stock se predeciría que se CONSTRUIRÍA** — la llamada visual
"dónde haría falta producir vivienda, servicios… teniendo en cuenta lo que se
predice construir".

### M4_VIVIENDAS / M4_SALUD / M4_PARADAS (crecimiento, esquema M1)

- **Stock**: viviendas = `unidades_urbanas_residencial` (serie completa
  2010-2025, despliegue t=2025); salud = `centros_de_salud +
  consultorios_locales` (sanidad ausente 2014 y 2025, despliegue t=2024);
  paradas = autobús + metro + cercanías (transporte ausente 2024-25, despliegue
  t=2023).
- **Target**: log-factor en escala **log1p** —
  `log(stock(t+h)+1) − log(stock(t)+1)` — permite stocks 0 sin romper los
  CAGRs; el inverso es `stock(t+h) = (1+stock)·EXP(pred)**(h/h_model) − 1`.
- **Features (10)**: `log_st, st_cagr_1, st_cagr_3, st_cagr_5, st_cagr_10,
  st_vol_5, st_p1000, log_pob, pob_cagr_5, horizonte` (en `PV_BASE_MODELOS`
  van prefijadas `VIV_/SAL_/PAR_` con su `T_DEPLOY`).
- **Algoritmo**: `GradientBoostingRegressor`; split por municipio.
- **Métricas (test)**:

  | modelo | mediana \|err\| % | por horizonte (h1→h5) |
  |---|---|---|
  | viviendas | 0.55 % | 0.33 → 1.09 |
  | salud | 0.01 % * | 0.0004 → (h≤4) |
  | paradas | 2.34 % | 1.92 → 3.47 |

  \* salud: el stock sanitario apenas cambia en 2015-2023 — el modelo predice
  crecimiento ~0; **no hay señal de inversión sanitaria en el dataset** (decisión
  abierta: otra fuente o reformularlo como "esperado por tamaño").

- **Semántica clave**: el stock futuro = lo que **se predeciría construir**;
  los choques del WI (`P_ADD_*`) se suman **encima** de la proyección.
  Para `año ≤ 2025` el stock queda real (sin proyección).

### M4_ESCUELAS (cross-sectional)

- **Por qué no serie temporal**: el dataset solo tiene escuelas como **un corte
  estático** (`centros_educativos_alta`, 23/155 municipios con 0) — no existe
  una señal honesta de "tasa de construcción escolar"; inventarla no entraba.
- **Qué aprende**: "cuántas escuelas esperadas tiene un municipio de tamaño X"
  (features: `log_pob, edad_media, pct_menor_15, pct_65mas, distancia_sol_km,
  tiempo_centro_min` — con la imputación declarada del tiempo: `max(0,
  a + b·distancia)`, la misma del M2). Algoritmo `RandomForestRegressor`
  (300, leaf 10, depth 4); **mae 1.19 escuelas**.
- **Semántica de uso (declarada)**: el stock proyectado crece por la
  **proporción** del esperado entre `pob_y` y `pob_2025` —
  `escuelas_y = escuelas_2025 · pred(pob_y) / pred(pob_2025)` — un municipio
  sin escuelas hoy no las gana "de la nada" y el stock actual no se da de baja.

---

## Integración en la base (por si te toca tocarla)

| Tabla / objeto | Rol |
|---|---|
| `PV_BASE_MODELOS` | Estado base 2025 con TODAS las features (M1, M2, M3 y las M4 prefijadas `VIV_/SAL_/PAR_` con `T_DEPLOY`). Generado por `mcp/generar_estado_base.py` (referencia en `oracle_db/sql/01_estado_base.sql`). |
| `PV_SIMULA(cod, año, add_pop, add_viv, add_salud, addesc, add_paradas)` | WI (pág. 10): M1 → proyección M4 → estado (+choque) → 5×M2 → índice + limitante → JSON "antes/después" |
| `PV_MAPA(año)` | Mapa (pág. 40): mismo estado para los 155 en una sola SQL → JSON con todos los diferenciales |

Criterio de calidad (§8 del doc maestro): los 11 `.onnx` reproducibles con
`run_all.py`, paridad `PREDICTION` ↔ `onnxruntime` ≤ 1e-5, y mismo estado
en ambos endpoints (delta 0 en la batería de validación de 155×5 campos).
