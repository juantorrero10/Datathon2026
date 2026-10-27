# mcp/ — scripts de operación (asistente ↔ base de datos)

Carpeta de **infraestructura**, no del proyecto en sí: aquí viven los scripts
que sirven para gestionar la base de datos y la aplicación APEX desde un
ordenador de desarrollo (los usa el asistente de desarrollo; una persona
externa al repo normalmente no los necesita).

| Script | Qué hace |
|---|---|
| `generar_estado_base.py` | Carga en Oracle la tabla `PV_BASE_M3_M4` (estado base 2025 con las features exactas de los modelos) y deja la referencia en `oracle_db/sql/01_estado_base_m3_m4.sql`. |
| `cargar_onnx.py` | Sube los `.onnx` de `oracle_db/models/` a la base (`IMPORT_ONNX_MODEL`) y valida paridad con `onnxruntime` local. |
| `editar_export_simulador.py` + `editar_export_contenido.py` | Genera `oracle_db/backups/simulador.sql` a partir del export original (`sql_original.sql`): inyecta el front actual de la página 10, renombra páginas y limpia el menú. |
| `importar_export.py` | Ciclo completo de reimport de la app 215: borra la app (como ADMIN), importa el export mutado (como WKSP_DATATHON) y verifica. |

`editar_export_contenido.py` contiene el HTML/JS del front (única fuente de
verdad de la interfaz). El resto del proyecto (src/, scripts/) no depende de
esta carpeta.
