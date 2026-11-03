# web/ — assets del visor (datos del mapa)

Los ficheros de DATOS que consumen las páginas APEX (pág. 40 Mapa) y sus
derivados. El código del visor (fronts de APEX, updaters, helpers de menú
y export/import de la app 215) vive en `mcp/`.

| Fichero | Qué es |
|---|---|
| `geo_municipios_madrid.geojson` | Polígonos de los 155 municipios para el mapa (OSM vía Overpass, ensamblados por id de nodo y simplificados). Lo consume el AJAX `GEO` de la pág. 40 vía `PV_GEO_MUNIS`; lo genera/regenera `mcp/descargar_geojson.py` (caché local `osm_raw_cm.json` NO versionada). |
| `limite_madrid.json` | Límite de la Comunidad de Madrid inyectado como `window.__MV_LIMITE` en el front del mapa. |

Aplicación: **MadridNext** (app APEX 215; antes "Pueblos con Vida").