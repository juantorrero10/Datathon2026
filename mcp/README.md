# mcp/ — loaders del tronco hacia Oracle (asistente ↔ base de datos)

Carpeta de **infraestructura del tronco**: los scripts que suben los artefactos
de los modelos (N1) a Oracle (N2). La parte de la página web / visor APEX vive
en `web/` — los scripts de front, export e importación de la app 215 se
movieron a esa carpeta (ver `web/README.md`).

| Script | Qué hace |
|---|---|
| `generar_estado_base.py` | Carga en Oracle la tabla `PV_BASE_M3_M4` (estado base 2025 con las features exactas de los modelos) y deja la referencia en `oracle_db/sql/01_estado_base_m3_m4.sql`. |
| `cargar_onnx.py` | Sube los `.onnx` de `oracle_db/models/` a la base (`IMPORT_ONNX_MODEL`) y valida paridad con `onnxruntime` local. |

El resto del proyecto (src/, scripts/) no depende de esta carpeta.
