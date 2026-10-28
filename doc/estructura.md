# Estructura del proyecto — fichero por fichero

> Referencia rápida: qué es y para qué sirve cada archivo del repositorio.
> Si tocas un fichero, actualiza esta lista.
> Última revisión: 28-oct-2026 (limpieza del repositorio: caches `__pycache__` eliminadas, `.gitignore` reorganizado, `README.md` raíz, `run_all.py` corregido a `oracle_db/models`; detalle en `project_context.md` §10).

---

## Raíz

| Fichero / carpeta | Qué es |
|---|---|
| `README.md` | Portada del proyecto: qué es, cómo reproducir los modelos (`scripts/run_all.py`), mapa del repositorio y convenciones. |
| `.gitignore` | Reglas de versionado: excluye el wallet, `.env`, `opencode.json` (config local), caches de Python y carpetas de IDE. |
| `opencode.json` | Configuración de **OpenCode** para este workspace: define el servidor MCP local `apex-mcp` (que conecta a Oracle/APEX). El `APEX_MCP_READ_ONLY=false` permite DML/DDL por MCP. |
| `data/dataset_155_municipios_2010-2025.xlsx` | **Único dataset de entrada**: 5 sheets (LEEME, panel municipio-año 2010-2025 = 2.480 filas × 32 columnas oficiales INE/CAM, estática de los 155 municipios < 50.000 hab, diccionario, fuentes). Alimenta los pipelines de M3 y M4. |

## src/ — código Python del pipeline (esto es el proyecto)

| Fichero | Qué es |
|---|---|
| `common/dataset.py` | Carga del xlsx (panel + municipios), rutas del repo, hash del dataset. Único punto de acceso a los datos. |
| `common/oracle.py` | Conexión local a Oracle con `python-oracledb` (thin) + wallet. Lee el `.env` del servidor MCP (fuera del repo); acepta wybór usuario (`conectar(usuario, contraseña)`) para imports de ONNX y de la app APEX. **Infra del asistente, no del pipeline.** |
| `m3_demografia/features.py` | Dataset de entrenamiento M3: fila por (municipio, año base t, horizonte h): features solo a fecha t (CAGR 1/3/5/10, volatilidad, demografía, paro, migración, acceso) + target `log(pob(t+h)/pob(t))`. |
| `m3_demografia/train_export.py` | Entrena `GradientBoostingRegressor`, split por municipio (sin fuga temporal), exporta `oracle_db/models/m3_demografia.onnx` (ValueInfo parcheada a `(N,1)`), valida ONNX↔sklearn (mediana del error del factor en test: 1,27 %) y escribe la ficha JSON. |
| `m4_capacidad/features.py` | Estados municipales por año: ratios de saturación "crudos" y targets = 5 dimensiones de la app (percent-rank por corte anual). Excluye los años con indicadores vacíos del xlsx (telefonía 2010-11, sanidad 2014/2025, transporte 2024-25). |
| `m4_capacidad/train_export.py` | Entrena 5 `RandomForestRegressor` (uno por dimensión, porque Oracle exige salida escalar en ONNX), exporta a `oracle_db/models/m4_capacidad_{dem,viv,ser,acc,emp}.onnx`, valida y escribe la ficha. |
| `deprecated/` | Código antiguo (LoDCORE). **Solo referencia**; no forma parte del pipeline. |

## scripts/ — los ejecutables del pipeline (lo que corre el equipo)

| Fichero | Qué hace |
|---|---|
| `run_m3_demografia.py` | Pipeline completo M3: xlsx → features → entrenar → `.onnx` + ficha. |
| `run_m4_capacidad.py` | Pipeline completo M4 → 5 `.onnx` + ficha. |
| `run_all.py` | Lanza los dos en orden y comprueba que existen los 6 `.onnx` esperados (1 de M3 + 5 de M4) en `oracle_db/models/`. |

## mcp/ — operación del asistente (conexión con la base y APEX)

> **Nota externa:** esta carpeta es infraestructura para gestionar Oracle/APEX
> desde un PC de desarrollo (la usa el asistente). El pipeline no depende de
> ella. No toques nada si solo quieres ejecutar los modelos (usa `scripts/`).

| Fichero | Qué hace |
|---|---|
| `generar_estado_base.py` | Carga en Oracle la tabla `PV_BASE_M3_M4` (estado base 2025 con las features exactas de los modelos; regla "último dato disponible") y deja referencia en `oracle_db/sql/01_estado_base_m3_m4.sql`. |
| `cargar_onnx.py` | Sube los `.onnx` a la base (`IMPORT_ONNX_MODEL`, BLOB directo) y valida paridad contra `onnxruntime` local (diff 0.00e+00). |
| `editar_export_simulador.py` + `editar_export_contenido.py` | Genera `oracle_db/backups/simulador.sql` desde el export original: inyecta el front actual de la pág. 10, renombra páginas y limpia el menú. `editar_export_contenido.py` es la **única fuente de verdad del HTML/JS** del Simulador. |
| `importar_export.py` | Ciclo completo de reimport de la app 215: borra la app (como ADMIN) → importa el export mutado (como WKSP_DATATHON, `p_default_workspace_id=>NULL`) → verifica páginas. |

## oracle_db/ — lo que vive dentro de la base, visto desde el repo

### models/ (salida de los pipelines)

| Fichero | Qué es |
|---|---|
| `m3_demografia.onnx` | M3: regresión → `log(factor de crecimiento)` a horizonte h. Consumo: `EXP(PREDICTION(M3_DEMOGRAFIA USING ...))`. |
| `m4_capacidad_{dem,viv,ser,acc,emp}.onnx` | M4: un fichero por dimensión (regresión escalar, 0-100). |
| `m3_demografia.json`, `m4_capacidad.json` | Fichas técnicas (hash del dataset, orden de features, métricas, imputaciones). **Sin ficha no se sube a Oracle.** |
| `README.md` | Notas de la carpeta. |

### sql/

| Fichero | Qué es |
|---|---|
| `01_estado_base_m3_m4.sql` | DDL + INSERTs de `PV_BASE_M3_M4` (155 filas), generado por `mcp/generar_estado_base.py`. |
| `03_pv_simula_v2.sql` | `PV_SIMULA(p_cod, p_anio, p_add_pop, p_add_viv, p_add_salud, p_add_esc, p_add_paradas)`: motor del simulador. M3 (factor; si año ≤ 2025 usa la serie real) → estado simulado → 5 `PREDICTION` de M4 → índice ponderado + factor limitante → CLOB JSON "antes/después". Banda M3 tomada del backtest por horizonte. |

### backups/

| Fichero | Qué es |
|---|---|
| `sql_original.sql` | **Backup del export SQL de la app 215 tal como estaba antes de la unificación**. Es el punto de restauración oficial de la app. No lo sobreescribas. |
| `simulador.sql` | Export mutado que se instala (generado por `mcp/editar_export_simulador.py`): pág. 10 "Simulador What-If" con el front actual, pág. 20 retirada, menú limpio, proceso `SIMULAR` de 7 parámetros, `p_default_workspace_id=>NULL`. |

## doc/

| Fichero | Qué es |
|---|---|
| `project_context.md` | **Documento maestro**: definición del Simulador como única funcionalidad, decisión de modelos (M3 y M4 ONNX; M1/M2/M5 fuera), arquitectura N1→N3, criterios de éxito. |
| `estructura.md` | Este documento. |
| `modelos/m3_demografia.json` · `modelos/m4_capacidad.json` | Copias de las fichas para el jurado (mismas que `oracle_db/*/…json`). |
| `legacy/contexto_primer_borrador.md` | Primer plan (5 perfiles, 3 capas, FastAPI…): **retirado**, referencia histórica. |
| `legacy/perfil_ciudadano.md` | Espec C1-C7 del perfil ciudadano: **retirada** (unificada en el Simulador). |

## tests/

Reservada para tests (pytest). Hoy **vacía**: solo contiene un `.gitkeep`
para que git preserve la carpeta en el repositorio.

## wallet/

Clon del wallet de la Autonomous Database (eu-madrid, instancia `N590X9G2V58K2MZG`): `tnsnames.ora` (alias `_tp`, `_low`, `_high`...), `ewallet.pem`, `cwallet.sso`. Lo usan el servidor MCP `apex-mcp` y los scripts que conectan por `src/common/oracle.py`. Contiene credenciales: no publicar, no meter en git.

---

## Convenciones

1. Cadena oficial: `data/*.xlsx` → `scripts/run_*.py` → `oracle_db/models/*.onnx` → (`mcp/cargar_onnx.py` + `mcp/generar_estado_base.py`) → Oracle → `PV_SIMULA` → APEX (pág. 10).
2. La simulación es **efímera**: nada se persiste.
3. `oracle_db/backups/sql_original.sql` es la única manera de restaurar la app 215 si se rompe algo — no lo sobreescribas.
4. Toda feature del xlsx que entre al modelo **debe quedar declarada en la ficha JSON** (hash, orden de features, imputaciones).
5. El front de APEX no lleva datos hardcodeados: todo lo visible sale del JSON de `PV_SIMULA` (o del proceso `DATOS` para la lista de municipios). Y **todos los botones llevan `type="button"`** — APEX envuelve la página en un `<form>` y sin eso los botones provocan submit y recarga.
