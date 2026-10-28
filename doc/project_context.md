# PROJECT_CONTEXT.md — Pueblos con vida · Simulador What-If

> Documento de contexto operativo. Sustituye por completo al borrador anterior
> (`doc/legacy/contexto_primer_borrador.md`), que describía 5 perfiles, 3 capas
> de datos y 73 tests. **Ese plan está retirado.** Este proyecto ahora tiene
> UNA funcionalidad, y todo esfuerzo se concentra en que funcione de verdad.

---

## 1. Qué es el proyecto

Un simulador What-If para los 155 municipios de la Comunidad de Madrid con
menos de 50.000 habitantes, dentro de la aplicación APEX **215 "Pueblos con
vida"** (página 10, Perfil Institucional).

**Una sola interacción:**

```
El usuario elige municipio + año + parámetros de choque
   → pulsa "Simular escenario"
   → se ejecutan los modelos M3 y M4 (ONNX, dentro de la base de datos)
   → el resultado son las métricas SIMULADAS de ese municipio para ese año
   → se pintan de forma visual (barras antes/después, semáforos, índice)
```

La salida de la simulación es **efímera**: no se guarda en ninguna tabla. Si
el usuario recarga, el escenario desaparece (volvió el mapa original).

**Qué es el tronco del proyecto:** los **modelos y el análisis de datos**
(`data/` → `scripts/run_*.py` → `oracle_db/models/` + sus fichas JSON) y su
carga a Oracle (`mcp/`). La página APEX 215 es el **visor** de esos modelos:
todo lo que existe solo para ella (front, exports, polígonos del mapa, backups
de la app) vive aislado en `web/` y no es necesario para reproducir el tronco.

**Pregunta que responde el simulador:**
> Si este municipio gana N habitantes y hacemos X inversión/en ampliaciones,
> ¿cómo queda su índice vitalidad para el año Y? ¿Y qué se rompe primero?

---

## 2. Datos: una única fuente

`data/dataset_155_municipios_2010-2025.xlsx` — construido por el equipo, casi
todo datos **oficiales** del INE y de la Comunidad de Madrid (ver sheet
`Fuentes`). Se guarda la versión anterior calibrada: ya no hay variables
inventadas, por lo que la regla de honestidad ahora es más sencilla.

| Sheet | Contenido |
|---|---|
| `LEEME` / `Diccionario` / `Fuentes` | Metadatos (109 indicadores) |
| `Panel_2010_2025` | Panel apilado: 155 municipios × años 2010-2025 = 2.480 filas × 32 columnas (demografía, paro, centros de salud, consultorios, transporte, paradas, valor catastral) |
| `Municipios` | 155 filas: datos geográficos y de accesibilidad de cada municipio (distancia a Madrid, paradas por modo, escuelas en ALTA, estaciones de calidad del aire) |

---

## 3. Los modelos M1-M5: qué se sube a Oracle y qué no

Espectro de decisión (hay 2 modelos ONNX en `oracle_db/models`):

| Modelo | ¿Se sube? | Motivo |
|---|---|---|
| **M3 · Demografía** | ✅ **Sí, ONNX** | Es lo que da la **dimensión temporal** al simulador: predice la trayectoria poblacional (factor de crecimiento por horizonte h) del municipio para el año elegido. Sin él, el "año seleccionado" tendría que volver a ser una tabla precalculada estática |
| **M4 · Capacidad / Vitalidad** | ✅ **Sí, ONNX** | Es el **motor de las métricas simuladas**: aprende el mapeo estado municipal (ratios de saturación) → 5 dimensiones + índice. Al pasarle el estado simulado del año Y devuelve las 5 dims (0-100) que pinta la interfaz |
| **M1 · AVM (precio vivienda)** | ❌ No | El negocio del simulador no es comprar piso; los precios quedan como valor estático del mapa. Además sus métricas son las más débiles del proyecto (imposible ajustar bien el precio con esta muestra y con target unitario) |
| **M2 · Indicadores (PCA)** | ❌ No | Era un motor para los sub-índices calibrados del borrador antiguo. Las 5 dimensiones viven ahora (en el índice) como rangos percentiles calcados en SQL; el PCA no modela nada nuevo sobre este estado |
| **M5 · Recomendador / ranking** | ❌ No | El ranking de los 155 municipios ya es una vista del mapa (columna `indice`), altamente interpretable y probada. **El simulador no ordena municipios; simula un municipio**. Una recomendación y un ranking son cosas distintas (ver §4 del legacy) |
| **M6 · Valor catastral (AVM)** | ⚠️ **Residual** | Está presente (`src/m6_mapa/`, `m6_valor.onnx` y `PV_MAPA` lo consume para proyectar el valor), pero quedó **fuera del árbol de decisión** de este doc (M1 descartado). Decisión pendiente: retirarlo y dejar el valor estático, o documentarlo plenamente. No durante esta reorganización. |

Filosofía: **una dimension, un modelo, un fichero .onnx** (M4 baja a la
base como 5 ficheros, uno por dimensión). Resultado simple: dos pipelines
Python (M3, M4) → seis .onnx → cargados en Oracle. El M6 residual añade un
tercer pipeline (`src/m6_mapa/`) y `m6_valor.onnx` — ver su fila en la tabla.

---

## 4. Arquitectura

| Nivel | Dónde | Qué |
|---|---|---|
| **N1** | Entrenamiento (Python) | `src/m3_demografia` y `src/m4_capacidad` entrenan y exportan `oracle_db/models/*.onnx` |
| **N2** | Oracle 23ai | Carga de ONNX (`DBMS_DATA_MINING` / `LOAD_ONNX_MODEL`) + `PREDICTION()` dentro de la función `PV_SIMULA` |
| **N3** | APEX (app 215) | Formulario → proceso AJAX "SIMULAR" → `PV_SIMULA` → JSON → render previo en la página con JS |

**Flujos ya verificados en la app de hoy (estado):**

```
Proceso AJAX "DATOS"    → ya funciona (tabla de municipios + serie)
Proceso AJAX "SIMULAR"  → hoy llama a `PV_SIMULA` solo para el año ACTUAL,
                          con recálculo del índice por percent-ranks puro en SQL
                          (es el esqueleto — hay que enchufarle los modelos)
Enlace Mapa ↔ Simulador → clic izq. en el mapa (o menú contextual "Detalles")
                          guarda {cod, año} en sessionStorage "pvWiJugada" y
                          navega a la pág. 10; el Simulador, tras rellenar el
                          select con DATOS, auto-ejecuta la FASE 1 (SIMULAR con
                          sliders a 0). "Comparar" en el menú contextual queda
                          reservado (no-op). Implementado como OPCIÓN 1
                          (recordar y re-jugar): los JSON de PV_MAPA y
                          PV_SIMULA NO se unifican.
```

### El estado simulado (la parte ONNX)

Ante cada combinación (año Y, P) el PL/SQL:

1. **M3** entrega el factor de crecimiento del municipio hacia el año Y →
   `poblacion_base(Y) = poblacion_2025 × factor` (y la banda de confianza
   baja/alta de la misma forma).
2. Se añade el choque del usuario: `poblacion_sim(Y) = poblacion_base(Y) + N_hab`
   (+ viviendas, + centros salud, + escuelas, + paradas añadidas) → ratios.
3. **M4** toma los ratios del estado simulado → devuelve
   `(dim_dem, dim_viv, dim_ser, dim_acc, dim_emp)` ∈ [0,100].
4. El `índice_sim` es combinación ponderada fija (0,20/0,15/0,25/0,25/0,15);
   el `factor_limitante` es el `argmin₁` de las 5 dims (regla SQL que ya
   funciona en `PV_SIMULA` y se conserva).
5. Todo esto NO se persiste; sale como CLOB JSON. La función `PV_SIMULA`
   devuelve el mismo esquema "antes/después" que ya muestra el front: los 10
   pares + `delta_indice`.

**Regla de los pesos:** los pesos del índice son decisión del diseño y no
cambia con el año ni con el perfil (no hay perfiles ya).

---

## 5. Estructura del repositorio

```
Datathon2026/
├── README.md                                   ← portada del proyecto
├── data/
│   └── dataset_155_municipios_2010-2025.xlsx   ← único dataset de entrada (TRONCO)
├── doc/
│   ├── project_context.md                      ← ESTE documento
│   ├── estructura.md                           ← inventario fichero a fichero
│   ├── legacy/                                 ← borrador anterior (referencia)
│   └── modelos/                                ← fichas de M3 y M4 (para el jurado)
├── mcp/                                        ← loaders del tronco hacia Oracle
│   ├── generar_estado_base.py                  ← PV_BASE_M3_M4 (estado base)
│   └── cargar_onnx.py                          ← sube los .onnx a la base
├── web/                                        ← VISOR: todo lo exclusivo de la app APEX 215
│   ├── geo_municipios_madrid.geojson           ← polígonos de los 155 (mapa)
│   ├── limite_madrid.json                      ← límite de la CM (front del mapa)
│   ├── descargar_geojson.py / completar_geojson.py  ← pipeline geo Overpass → PV_GEO_MUNIS
│   ├── front_mapa.py / actualizar_front_mapa.py / anadir_pagina_mapa.py
│   ├── aplicar_front_simulador.py / editar_export_simulador.py / editar_export_contenido.py
│   ├── importar_export.py                      ← reimport de la app
│   └── backups/                                ← exports de la app (sql_original.sql = punto de restauración)
├── oracle_db/
│   ├── models/                                 ← SALIDA: .onnx + fichas
│   │   ├── m3_demografia.onnx
│   │   └── m4_capacidad_{dem,viv,ser,acc,emp}.onnx
│   ├── sql/                                    ← estado base + PV_SIMULA + PV_MAPA/PV_GEO
│   └── (los exports de la app viven ahora en web/backups/)
├── scripts/
│   ├── run_m3_demografia.py                    ← ejecuta TODO el pipeline M3
│   ├── run_m4_capacidad.py                     ← ejecuta TODO el pipeline M4
│   └── run_all.py                              ← encadena los dos y comprueba salidas
├── src/
│   ├── common/                                 ← carga del xlsx + rutas + Oracle
│   ├── m3_demografia/                          ← features + train + export ONNX
│   ├── m4_capacidad/                           ← features + train + export ONNX
│   ├── m6_mapa/                                ← M6 residual (AVM valor catastral)
│   └── deprecated/                             ← código antiguo, solo referencia
├── visuals/                                    ← PNGs y diagramas del análisis
├── tests/                                      ← reservada para pytest (hoy vacía)
└── wallet/                                     ← credenciales Oracle (no versionado)
```

Convenciones:

- Cada pipeline acaba con sus `.onnx` + un fichero de **ficha del modelo**
  (`doc/modelos/m3_demografia.json`, `m4_capacidad.json`): features exactas,
  orden, métricas de backtest, fecha, hash del dataset. Sin ficha no se sube
  el modelo.
- Los scripts `run_*.py` corrigen `sys.path`, cargan `data/*.xlsx`, entrenan,
  validan con onnxruntime **desde disco** (error Python ↔ ONNX < 1e-6) y dejan
  los ficheros en `oracle_db/models/`. Son auto-contenidos y se ejecutan desde
  cualquier sitio, sin dependencia mutua.

---

## 6. Ficha de cada modelo (intención)

| | **M3 · Demografía** | **M4 · Capacidad / Vitalidad** |
|---|---|---|
| **Tarea** | Regresión del factor de crecimiento poblacional a horizonte h (1-10 años) | Regresión multi-salida de las 5 dimensiones (0-100) del municipio |
| **Instancia** | Una por (municipio, año base t, horizonte h) — el panel da ~150k muestras | Una por (municipio × año) — 2.480 muestras |
| **Features (M3)** | historial: CAGR 1/3/5/10 años, variabilidad, tasa migración/media edad, paro; sin el futuro | Ratios de saturación: hab/centro salud, hab/escuela, hab/parada, km²/hab, densidad, paro_100, edad, distancia, viviendas/1000 hab |
| **Target (M4)** | población(t+h) / población(t) | Las 5 dims recalculadas con la misma fórmula de percent-rank del panel de ese año |
| **Algoritmo** | GradientBoostingRegressor | RandomForestRegressor multi-output |
| **Export** | `skl2onnx` | `skl2onnx` |
| **Consumo en Oracle** | `PREDICTION(m3..., 1 poblacion, ...) → factor` | `PREDICTION(m4...) → 5 valores de dim` |

## 7. Estado de la app 215 (inventario real)

| Página | Nombre | Uso nuevo |
|---|---|---|
| 1 | Inicio | Enlace al dashboard |
| **10** | **Perfil Institucional** | **Aquí vive el simulador** (región rails PL/SQL, procesos AJAX `DATOS` y `SIMULAR`) |
| 20 | Perfil Ciudadano | Sin perfil: se eliminará o quedará congelada |
| 30 | Datos | Documentación de fuentes (se conserva) |

Tablas Oracle ya cargadas por el equipo (se conservan salvo cambios mínimos):

`PV_MUNICIPIOS` (155 × 36), `PV_MUN_BASE` (más ranks y 5 dims precalculadas),
`PV_SERIE` (2010-2025), `PV_PROYECCION(_SERIE)` (2026-2035 con la extrap. geométrica —
sustituida por M3 ONNX), `PV_VECINOS`, `PV_MUN_2035` (vista de mapa),
`PV_SIMULA` (package actual — como base para la v2).

---

## 8. Cuadro de mando / criterios de éxito

La única forma de saber que el proyecto funciona:

1. `python scripts/run_all.py` reproduce M3 y M4 desde el xlsx y dejan sus
   seis `.onnx` (1 de M3 + 5 de M4) en `oracle_db/models/` con ficha y
   validación ONNX↔Python en verde.
2. En APEX 215 pág 10 se elige municipio+parámetros+**año** → "Simular escenario"
   → los 5 dims y el índice del escenario aparecen visualmente (barras
   antes/después + semáforo + factor limitante) en segundos, y desaparecen al recargar.
3. `PREDICTION()` en SQL de los .onnx es extensión del dato: mismo valor ejecutado
   desde Python y desde PL/SQL (≤1e-6).

Si alguno de los 3 se cumple → funcionamos. Si todos → proyecto redondo.

---

## 9. Fuera del alcance (declarado, para no volver atrás)

- Perfiles de usuario (ciudadano / institución / empresario): retirados
- FastAPI / portal estático / algoritmos.html: retirados
- Optimizador de presupuesto multi-municipio: retirado
- Persistir simulaciones: prohibido por diseño (la simulación es efímera)
- Precios de vivienda predictivos (M1): los precios quedan como dato estático
- Isócronas GTFS, SARIMAX, inferencia causal, ampliar a los 179: roadmap futuro

---

## 10. Registro de mantenimiento

- **28-oct-2026 · fix PV_SIMULA "antes"** (quiebre mapa ↔ WI): el "antes" del
  WI salía de `PV_MUN_BASE` (corte 2025 bruto): su `SALUD_10K` se computó sin
  sumar CONSULTORIOS (121/155 municipios con servicio real a 0 almacenado) y
  sin la regla "último dato disponible" para la sanidad 2025 (155/155 NULL en
  el xlsx) — el mapa, que recalcula desde `PV_BASE_M3_M4`, mostraba 142,86
  (La Acebeda) frente al 0,000 del WI. Ahora los stocks/ratios "antes" se
  derivan de `PV_BASE_M3_M4` con las mismas fórmulas que "después"
  (`PV_MUN_BASE` queda solo para las dims/índice del corte 2025). Verificado:
  155/155 municipios, ratios/stocks "antes" y "después (sin choque)" idénticos
  al mapa (delta 0 en salud/escuelas/paradas/viviendas/población), "antes"
  estable entre años 2025-2035. Nota: escuelas=0 en 23 municipios es DATO
  (estático, no bug).
- **28-oct-2026 · interacción Mapa ↔ Simulador (fase 1 auto-ejecutada):**
  clic izquierdo en un municipio del mapa (y menú contextual con "Detalles" y
  "Comparar", este último no-op) guarda `{cod, año}` en
  `sessionStorage "pvWiJugada"` y navega a la pág. 10, cuyo front canonizado
  (`web/front_simulador.py`, extraído del estado vivo con
  `web/canonizar_front_sim.py`) preseleciona municipio+año tras el DATOS y
  ejecuta la FASE 1 automáticamente; la clave se limpia para que un refresh
  no re-juegue. Detalle del enlace en §4.
- **28-oct-2026 · reorganización tronco vs. visor + pipeline geo** (dos cosas
  en una):
  1. *Carpeta `web/`:* todo lo exclusivo de la página APEX 215 vive ahora en
     `web/` (front del Simulador y del Mapa, export/import de la app,
     `geo_municipios_madrid.geojson`, `limite_madrid.json` y los exports
     movidos de `oracle_db/backups/` a `web/backups/`). `mcp/` queda reducida
     a los loaders del tronco (`generar_estado_base.py`, `cargar_onnx.py`).
     El `data/` queda solo con el xlsx del tronco. El dump crudo de Overpass
     (`web/osm_raw_cm.json`) es caché local NO versionada (`.gitignore`).
  2. *Pipeline geo de OSM:* reescrito el ensamblado de polígonos por
     **id de nodo** con crecimiento bidireccional y división de "ochos", tras
     diagnosticar (a) que `PV_GEO_MUNIS` estaba vacía y (b) el bug histórico
     del ensamblador (`list(reversed(t))[:-1]`, que metía los tramos
     invertidos comiéndose el punto compartido y rompiendo los anillos con
     saltos de kilómetros). Resultado: 155/155 features válidas (147 Polygon,
     8 MultiPolygon de exclaves reales), 244 KB, cargadas en Oracle.
     Falsos de validación corregidos: los saltos de ensamblaje se miden sobre
     el dato crudo (antes de Douglas-Peucker) porque los lados rectos largos
     y reales de los límites se comprimen a un segmento.
  3. *M6 documentado como residual* (fila ⚠️ en §3): presente en `src/m6_mapa/`
     y `oracle_db/models/m6_valor.onnx`, consumido por `PV_MAPA`, pero fuera
     del árbol de decisión del doc maestro. Decisión de retiro/conservación
     pendiente.
- **28-oct-2026 · limpieza del repositorio** (sin cambios de funcionalidad):
  eliminadas todas las carpetas `__pycache__/` (incluida la huérfana de
  `m6_proyeccion`); `.gitignore` reorganizado por secciones (`+.idea/`;
  eliminada la línea `src/common`, que era un residuo peligroso — ese código
  del pipeline ya está versionado); nueva portada `README.md` en la raíz;
  `tests/.gitkeep` para que git preserve la carpeta; corregidas las
  referencias al antiguo `oracle/` que quedaron tras la reorganización
  (`scripts/run_all.py`, docstrings de `src/` y `mcp/`, `README.md` de
  `oracle_db/models/`, comentario de `PV_SIMULA`) hacia el `oracle_db/`
  actual. `run_all.py` vuelve a comprobar las salidas reales: 1 `.onnx` de
  M3 + 5 de M4 en `oracle_db/models/`. También se ha restaurado el texto
  corrompido de este documento.
- **27-oct-2026 · reorganización:** carpetas `oracle_db/`, `mcp/` y `tests/`;
  unificación de la app en el Simulador (pág. 10).
