# web/ — elemento del visor APEX 215 (no es el tronco del proyecto)

**El tronco del proyecto son los modelos y el análisis de datos** (`data/`,
`src/`, `scripts/`, `oracle_db/models` y `oracle_db/sql`). Esta carpeta reúne
TODO lo que existe solo para servir a la página web (app APEX 215
"Pueblos con Vida"): el simulador (pág. 10), el mapa (pág. 40) y los exports
de respaldo de la app. No se usa para reproducir modelos.

## Ficheros

| Fichero | Qué es |
|---|---|
| `geo_municipios_madrid.geojson` | Polígonos de los 155 municipios para el mapa (OSM vía Overpass, ensamblados por id de nodo y simplificados). Lo consume el AJAX `GEO` de la pág. 40 vía `PV_GEO_MUNIS`. |
| `limite_madrid.json` | Límite de la Comunidad de Madrid que se inyecta como `window.__MV_LIMITE` en el front del mapa. |
| `descargar_geojson.py` | Pipeline geo: descarga OSL/Overpass → ensamblado por nodos → `PV_GEO_MUNIS` + GeoJSON. `FORCE_RELOAD=1` re-descarga (la caché `osm_raw_cm.json` NO va versionada). |
| `completar_geojson.py` | Rescate de un municipio: re-descarga y `MERGE` de una relación individual en la tabla. |
| `front_mapa.py` | HTML/JS del front del mapa (única fuente de verdad; lo inyecta `anadir_pagina_mapa.py`). Fondo **gris plano por defecto** y un único interruptor "Satélite" (`mvSw`). **Interacción con el Simulador:** clic izquierdo en un municipio → abre el WI con la fase 1 auto-ejecutada (`sessionStorage "pvWiJugada"`); clic derecho → menú "Detalles" (= WI) y "Comparar" (inactivo, por ahora). |
| `front_simulador.py` | HTML/JS del front del Simulador (pág. 10; canonizado del estado vivo con `canonizar_front_sim.py`) + el consumo de `pvWiJugada`: preselecciona municipio/año y ejecuta la fase 1 (SIMULAR con sliders a 0) sin interacción. |
| `actualizar_front_simulador.py` | Reaplica el front del Simulador a la pág. 10 instalada (parche sobre export vivo + reimport). |
| `canonizar_front_sim.py` | Generador único de `front_simulador.py` desde el export vivo (ejecutar solo si el front de la pág. 10 cambió a mano; después, ediciones a mano en `front_simulador.py`). |
| `menu_mapa.py` | Helper de mutación del export: coloca la entrada **'Mapa'** (`fa-map`, secuencia 30) en el **Navigation Menu** compartido (y la quita de la barra de navegación, donde estaba mal puesta). |
| `actualizar_front_mapa.py` | Reaplica el front del mapa a la página 40 instalada. |
| `anadir_pagina_mapa.py` | Añade la página 40 (Mapa) al export. |
| `aplicar_front_simulador.py` | (histórico) Reaplicaba el front antiguo v3 del Simulador; **obsoleto**: el front vigente vive en `front_simulador.py` y se aplica con `actualizar_front_simulador.py`. |
| `editar_export_simulador.py` + `editar_export_contenido.py` | Generan `web/backups/simulador.sql` desde `sql_original.sql`: mutan el export (front pág. 10 v3 antiguo, procesos AJAX, menú). **La fuente de verdad del front v3 era este; hoy el front vigente de la pág. 10 está en `front_simulador.py`.** |
| `importar_export.py` | Ciclo completo de reimport de la app 215: borra la app (ADMIN) e importa el export mutado (WKSP_DATATHON). |
| `backups/` | Exports SQL de la app 215. **`sql_original.sql` es el punto de restauración oficial: no se sobreescribe.** |

## Cómo regenerar los polígonos del mapa

```bash
python web/descargar_geojson.py        # OSM → PV_GEO_MUNIS (155 filas) + geojson
# re-descarga completa si la caché de Overpass no sirve:
FORCE_RELOAD=1 python web/descargar_geojson.py
```

Después de cambiar el front, el ciclo es:

```bash
python web/editar_export_simulador.py          # sql_original.sql → simulador.sql
python web/importar_export.py                  # reimport de la app 215 en APEX
# ciclo rápido para re-aplicar los fronts ACTUALES (pág. 10 / pág. 40):
python web/actualizar_front_simulador.py
python web/actualizar_front_mapa.py
```
