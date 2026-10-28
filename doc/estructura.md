# Estructura del proyecto — fichero por fichero

> Referencia rápida: qué es y para qué sirve cada archivo del repositorio.
> Si tocas un fichero, actualiza esta lista.
> Última revisión: 28-oct-2026 (2.ª pasada del día: **reorganización del visor
> web** — nueva carpeta `web/` con todo lo exclusivo de la app APEX 215; `mcp/`
> queda reducida a los loaders del tronco; `osm_raw_cm.json` fuera del repo
> caché no versionada; M6 documentado como residual; **29-oct-2026:
> enumeración redefinida M3→M1, M4→M2, M6→M3, M7→M4; documentación de modelos
> en `doc/models.md`; `PV_BASE_M3_M4` → `PV_BASE_MODELOS`. Detalle en
> `project_context.md` §10.

---

## Raíz

| Fichero / carpeta | Qué es |
|---|---|
| `README.md` | Portada del proyecto: qué es, cómo reproducir los modelos (`scripts/run_all.py`), mapa del repositorio y convenciones. |
| `.gitignore` | Reglas de versionado: excluye el wallet, `.env`, `opencode.json` (config local), cachés de Python, carpetas de IDE y la caché OSM del visor (`web/osm_raw_cm.json`). |
| `opencode.json` | Configuración de **OpenCode** para este workspace: define el servidor MCP local `apex-mcp` (que conecta a Oracle/APEX). El `APEX_MCP_READ_ONLY=false` permite DML/DDL por MCP. |
| `data/dataset_155_municipios_2010-2025.xlsx` | **Único dataset de entrada (TRONCO)**: 5 sheets (LEEME, panel municipio-año 2010-2025 = 2.480 filas × 32 columnas oficiales INE/CAM, estática de los 155 municipios < 50.000 hab, diccionario, fuentes). Alimenta los pipelines M1, M2, M3 y M4. |

> **El tronco vs. el visor:** la pieza principal del proyecto son los modelos
> y el análisis de datos (`data/`, `src/`, `scripts/`, `oracle_db/` salvo sus
> subcarpetas web). Todo lo que existe solo para la página APEX 215 vive en
> `web/` — poligonos del mapa, front, exports de la app.

## src/ — código Python del pipeline (esto es el proyecto)

| Fichero | Qué es |
|---|---|
| `common/dataset.py` | Carga del xlsx (panel + municipios), rutas del repo, hash del dataset. Único punto de acceso a los datos. |
| `common/oracle.py` | Conexión local a Oracle con `python-oracledb` (thin) + wallet. Lee el `.env` del servidor MCP (fuera del repo); acepta wybór usuario (`conectar(usuario, contraseña)`) para imports de ONNX y de la app APEX. **Infra del asistente, no del pipeline.** |
| `m1_demografia/features.py` | Dataset de entrenamiento M1 (demografía): fila por (municipio, año base t, horizonte h): features solo a fecha t (CAGR 1/3/5/10, volatilidad, demografía, paro, migración, acceso) + target `log(pob(t+h)/pob(t))`. |
| `m1_demografia/train_export.py` | Entrena `GradientBoostingRegressor` (M1), split por municipio (sin fuga temporal), exporta `oracle_db/models/m1_demografia.onnx` (ValueInfo parcheada a `(N,1)`), valida ONNX↔sklearn (mediana del error del factor en test: 1,27 %) y escribe la ficha JSON. |
| `m2_capacidad/features.py` | Estados municipales (M2) por año: ratios de saturación "crudos" y targets = 5 dimensiones de la app (percent-rank por corte anual). Excluye los años con indicadores vacíos del xlsx (telefonía 2010-11, sanidad 2014/2025, transporte 2024-25). |
| `m2_capacidad/train_export.py` | Entrena 5 `RandomForestRegressor` (M2) (uno por dimensión, porque Oracle exige salida escalar en ONNX), exporta a `oracle_db/models/m2_capacidad_{dem,viv,ser,acc,emp}.onnx`, valida y escribe la ficha. |
| `m3_valor/features.py` · `m3_valor/train_export.py` | Código del modelo M3 (AVM de valor catastral, ant. M6) → `m3_valor.onnx`, lo consume `PV_MAPA` (capa ΔValor). Documentado en `doc/models.md`. |
| `m4_stocks/features.py` | Features de la familia M4 (stocks proyectados): crecimiento por stock con serie (viviendas/salud/paradas, esquema M1 con horizontes 1..5 y escala log1p) y un **cross-sectional** de escuelas (sin serie temporal — único honesto: "escuelas esperadas dado el tamaño"), con `features_despliegue_series` que alimenta `PV_BASE_MODELOS`. |
| `m4_stocks/train_export.py` | Entrena M4_VIVIENDAS/SALUD/PARADAS (GB) + M4_ESCUELAS (RF), exporta `oracle_db/models/m4_*.onnx` con paridad ONNX↔sklearn y escribe fichas JSON (copias en `doc/modelos/`). |
| `deprecated/` | Código antiguo (LoDCORE). **Solo referencia**; no forma parte del pipeline. |

## scripts/ — los ejecutables del pipeline (lo que corre el equipo)

| Fichero | Qué hace |
|---|---|
| `run_m1_demografia.py` | Pipeline completo M1: xlsx → features → entrenar → `.onnx` + ficha. |
| `run_m2_capacidad.py` | Pipeline completo M4 → 5 `.onnx` + ficha. |
| `run_m4_stocks.py` | Pipeline completo M4: xlsx → features de stocks → 4 modelos (viviendas/salud/paradas + escuelas esperadas) → `.onnx` + fichas. |
| `run_all.py` | Lanza los pipelines en orden y comprueba las 11 salidas `.onnx` (1 M1 + 5 M2 + 1 M3 + 4 M4) en `oracle_db/models/`. |

## mcp/ — loaders del tronco hacia Oracle (infraestructura)

> Los scripts del front/export/import de la app 215 **se movieron a `web/`**.
> Lo que queda aquí es lo que conecta los modelos entrenados con la base.

| Fichero | Qué hace |
|---|---|
| `generar_estado_base.py` | Carga en Oracle la tabla `PV_BASE_MODELOS` (estado base 2025 con las features exactas de los modelos; regla "último dato disponible") y deja referencia en `oracle_db/sql/01_estado_base.sql`. |
| `cargar_onnx.py` | Sube los `.onnx` a la base (`IMPORT_ONNX_MODEL`, BLOB directo) y valida paridad contra `onnxruntime` local (diff 0.00e+00). |

## web/ — todo lo exclusivo de la app APEX 215 (visor, NO tronco)

> Detalle completo y ciclo de regeneración en `web/README.md`. Resumen:

| Fichero | Qué hace |
|---|---|
| `geo_municipios_madrid.geojson` + `limite_madrid.json` | Polígonos de los 155 municipios (OSM/Overpass ensamblados por id de nodo, Douglas-Peucker eps=0.0004°) y límite de la CM: alimentan el AJAX `GEO` y el `__MV_LIMITE` del mapa (pág. 40). |
| `descargar_geojson.py` | Pipeline geo completo: Overpass → `PV_GEO_MUNIS` (155 filas) + GeoJSON. `$env:FORCE_RELOAD="1"` re-descarga; el dump crudo (`osm_raw_cm.json`) es caché local NO versionada. |
| `completar_geojson.py` | Rescate de un municipio individual (`MERGE` en la tabla sin recrearla). |
| `front_mapa.py` · `actualizar_front_mapa.py` · `anadir_pagina_mapa.py` | HTML/JS del front de la pág. 40 y su ciclo de aplicación (única fuente de verdad del front del mapa). |
| `aplicar_front_simulador.py` · `editar_export_simulador.py` + `editar_export_contenido.py` | Ciclo del front del Simulador (pág. 10) sobre el export: `editar_export_contenido.py` es la **única fuente de verdad del HTML/JS** del Simulador. |
| `importar_export.py` | Reimport completo de la app 215: borra la app (ADMIN) e importa el export mutado (`web/backups/simulador.sql`, `p_default_workspace_id=>NULL`). |
| `backups/` | Exports SQL de la app 215. **`sql_original.sql` es el punto de restauración oficial: no se sobreescribe.** |

## oracle_db/ — lo que vive dentro de la base, visto desde el repo

### models/ (salida de los pipelines)

| Fichero | Qué es |
|---|---|
| `m1_demografia.onnx` | M1: regresión → `log(factor de crecimiento)` a horizonte h. Consumo: `EXP(PREDICTION(M1_DEMOGRAFIA USING ...))`. |
| `m2_capacidad_{dem,viv,ser,acc,emp}.onnx` | M2: un fichero por dimensión (regresión escalar, 0-100). |
| `m4_viviendas.onnx` · `m4_salud.onnx` · `m4_paradas.onnx` | M4 (crecimiento, esquema M1, horizontes 1..5): proyectan el stock al año objetivo; el consumidor compone geométricamente para h>5 con factor EXP(pred(5))**(h/5). |
| `m4_escuelas.onnx` | M4 cross-sectional: escuelas esperadas dado el tamaño; el stock crece por PROPORCIÓN del esperado (pob_y vs pob_2025). |
| `m3_valor.onnx` + `m3_valor.json` | M3 (AVM de valor catastral, ant. M6; lo consume `PV_MAPA` para proyectar el valor). Documentado en `doc/models.md`. |
| `m1_demografia.json`, `m4_capacidad.json` | Fichas técnicas (hash del dataset, orden de features, métricas, imputaciones). **Sin ficha no se sube a Oracle.** |
| `README.md` | Notas de la carpeta. |

### sql/

| Fichero | Qué es |
|---|---|
| `01_estado_base.sql` | DDL + INSERTs de `PV_BASE_MODELOS` (155 filas con features de M1, M2, M3 y M4 — las M4 prefijadas VIV_/SAL_/PAR_ con su `T_DEPLOY`), generado por `mcp/generar_estado_base.py`. |
| `03_pv_simula_v2.sql` | `PV_SIMULA(p_cod, p_anio, p_add_pop, p_add_viv, p_add_salud, p_add_esc, p_add_paradas)`: motor del simulador. M1 (factor; si año ≤ 2025 usa la serie real) → proyección M4 de stocks (viviendas/salud/paradas con composición geométrica h>5 y escuelas por proporción del "esperado por tamaño") → estado simulado (proyección + choque del usuario) → 5 `PREDICTION` de M2 → índice ponderado + factor limitante → CLOB JSON "antes/después". El bloque "antes" sale de `PV_BASE_MODELOS` (mismo estado que el mapa); `PV_MUN_BASE` solo aporta dims/índice del corte 2025. |
| `04_pv_mapa.sql` | `PV_MAPA(p_anio)`: métricas masivas de los 155 municipios para el mapa (7 `PREDICTION` en línea: M3 → estado → 5×M4 → M6 → índice + factor limitante). Extrapolación sostenida: f(h>5) = POWER(f5, h/5). |
| `05_pv_geo_munis.sql` | Referencia de `PV_GEO_MUNIS` (códigos + CLOB GeoJSON por municipio); los INSERTs van por binds desde `web/descargar_geojson.py`. |

## web/backups/ (movido desde oracle_db/backups/)

| Fichero | Qué es |
|---|---|
| `sql_original.sql` | **Backup del export SQL de la app 215 tal como estaba antes de la unificación**. Es el punto de restauración oficial de la app. No lo sobreescribas. |
| `simulador.sql` | Export mutado que se instala (generado por `web/editar_export_simulador.py`): pág. 10 "Simulador What-If" con el front actual, pág. 20 retirada, menú limpio, proceso `SIMULAR` de 7 parámetros, `p_default_workspace_id=>NULL`. |
| `sql_*_estado_usuario.sql` | Export del estado de APEX con cambios hechos a mano en la app ("estado usuario"): `sql_2026-10-28_1659...` es el estado vigente según el equipo. |

## doc/

| Fichero | Qué es |
|---|---|
| `project_context.md` | **Documento maestro**: definición del Simulador como única funcionalidad, decisión de modelos (M3 y M4 ONNX; M1/M2/M5 fuera), arquitectura N1→N3, criterios de éxito. |
| `estructura.md` | Este documento. |
| `modelos/m1_demografia.json` · `modelos/m4_capacidad.json` | Copias de las fichas para el jurado (mismas que `oracle_db/*/…json`). |
| `legacy/contexto_primer_borrador.md` | Primer plan (5 perfiles, 3 capas, FastAPI…): **retirado**, referencia histórica. |
| `legacy/perfil_ciudadano.md` | Espec C1-C7 del perfil ciudadano: **retirada** (unificada en el Simulador). |

## tests/

Reservada para tests (pytest). Hoy **vacía**: solo contiene un `.gitkeep`
para que git preserve la carpeta en el repositorio.

## wallet/

Clon del wallet de la Autonomous Database (eu-madrid, instancia `N590X9G2V58K2MZG`): `tnsnames.ora` (alias `_tp`, `_low`, `_high`...), `ewallet.pem`, `cwallet.sso`. Lo usan el servidor MCP `apex-mcp` y los scripts que conectan por `src/common/oracle.py`. Contiene credenciales: no publicar, no meter en git.

---

## Convenciones

1. **Tronco** (reproducible): `data/*.xlsx` → `scripts/run_*.py` → `oracle_db/models/*.onnx` → (`mcp/cargar_onnx.py` + `mcp/generar_estado_base.py`) → Oracle → `PV_SIMULA`/`PV_MAPA` → APEX. La pieza principal del proyecto son **los modelos y el análisis de datos**; el visor web es la capa de presentación.
2. La simulación es **efímera**: nada se persiste.
3. `web/backups/sql_original.sql` es la única manera de restaurar la app 215 si se rompe algo — no lo sobreescribas. Todo lo exclusivo de la página web vive en `web/`.
4. Toda feature del xlsx que entre al modelo **debe quedar declarada en la ficha JSON** (hash, orden de features, imputaciones).
5. El front de APEX no lleva datos hardcodeados: todo lo visible sale del JSON de `PV_SIMULA` (o del proceso `DATOS` para la lista de municipios). Y **todos los botones llevan `type="button"`** — APEX envuelve la página en un `<form>` y sin eso los botones provocan submit y recarga.
6. La caché del geo (`web/osm_raw_cm.json`) no va versionada: el GeoJSON oficial (`web/geo_municipios_madrid.geojson`) regenera `PV_GEO_MUNIS` sin tocar Overpass; `FORCE_RELOAD=1` solo si hay que re-descargar.
