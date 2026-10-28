"""Añade el/los municipios que faltan a PV_GEO_MUNIS + al GeoJSON local.

Uso:  python web/completar_geojson.py "El Boalo" 28023
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from src.common.dataset import cargar_municipios  # noqa: E402
from src.common.oracle import conectar  # noqa: E402
from web.descargar_geojson import (  # noqa: E402
    OUT_JSON,
    ensamblar_anillos,
    cerrar_ring,
    dentro_del_anillo,
    clave_nombre,
)

QUERY = """[out:json][timeout:300];
area["name"="Comunidad de Madrid"]["boundary"="administrative"]->.cm;
rel(area.cm)["name"="{nombre}"]["boundary"="administrative"]["admin_level"="8"];
out geom;
"""

MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass.osm.jp/api/interpreter",
]


def main() -> None:
    nombre, codine = sys.argv[1], sys.argv[2].zfill(5)
    munis = cargar_municipios().set_index("cod_ine")
    assert codine in munis.index, f"{codine} no está en el dataset"

    req = None
    for intento in range(len(MIRRORS) * 2):
        url = MIRRORS[intento % len(MIRRORS)]
        req = urllib.request.Request(
            url, data=QUERY.format(nombre=nombre).encode("utf-8"),
            headers={"User-Agent": "datathon-mapa/1.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except Exception as e:
            print(f"[completar] fallo {url}: {str(e)[:100]}")
            req = None
            time.sleep(20)
    if req is None:
        raise SystemExit("[completar] ningún mirror respondió")
    rels = [x for x in data.get("elements", []) if x.get("type") == "relation"]
    print(f"[completar] relaciones para '{nombre}': {len(rels)}")
    if not rels:
        raise SystemExit("[completar] Overpass no devolviÃ³ nada")

    poligonos_final = None
    for rel in rels:
        tags = rel.get("tags", {})
        outer = [m["geometry"] for m in rel.get("members", []) if m.get("role") in ("outer", "") and "geometry" in m]
        inner = [m["geometry"] for m in rel.get("members", []) if m.get("role") == "inner" and "geometry" in m]
        if not outer:
            continue
        outer_anillos, outer_abiertas = ensamblar_anillos(outer, cerradas_solo=False)
        if not outer_anillos:
            print(f"[completar] rel {rel['id']}: {len(outer)} tramos exteriores, 0 anillos")
            continue
        if outer_abiertas:
            print(f"[completar] rel {rel['id']}: {len(outer_abiertas)} tramo(s) exterior NO cerrado")
        inner_anillos, _ = ensamblar_anillos(inner, cerradas_solo=False)
        outer_rings = [cerrar_ring([[x, y] for (x, y) in a]) for a in outer_anillos if len(a) > 3]
        inner_rings = [cerrar_ring([[x, y] for (x, y) in a]) for a in inner_anillos if len(a) > 3]
        poligonos = []
        inner_restantes = list(inner_rings)
        for oring in outer_rings:
            huecos = [h for h in inner_restantes if dentro_del_anillo(h[0], oring)]
            poligonos.append([oring] + huecos)
            for h in huecos:
                inner_restantes.remove(h)
        poligonos_final = poligonos
        print(f"[completar] usada rel {rel['id']} (tags: {tags.get('admin_level')})")

    if poligonos_final is None:
        raise SystemExit("[completar] ninguna relación con geometría exterior")

    # validación idéntica al script principal: saltos de ensamblaje sobre el crudo
    for poligono in poligonos_final:
        for ring in poligono:
            for a, b in zip(ring, ring[1:]):
                if ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 > 0.05:
                    raise SystemExit("[completar] anillo con salto de ensamblaje > 5 km; no se sube")

    # simplificar a las mismas reglas del script principal
    from web.descargar_geojson import dp_simplify
    poligonos_s = []
    for poligono in poligonos_final:
        pg = [[[round(x, 5), round(y, 5)] for x, y in dp_simplify(ring, 0.0004)] for ring in poligono]
        pg = [r for r in pg if len(r) >= 4]
        if pg and len(pg[0]) >= 4:
            poligonos_s.append(pg)
    geom = (
        {"type": "Polygon", "coordinates": poligonos_s[0]}
        if len(poligonos_s) == 1
        else {"type": "MultiPolygon", "coordinates": poligonos_s}
    )

    # GeoJSON local (con NOMBRE del dataset)
    nombre_ds = munis.loc[codine, "municipio"]
    fc = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    fc["features"] = [f for f in fc["features"] if f["properties"]["cod"] != codine]
    fc["features"].append({
        "type": "Feature",
        "properties": {"cod": codine, "nombre": nombre_ds},
        "geometry": geom,
    })
    OUT_JSON.write_text(json.dumps(fc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"[completar] {OUT_JSON}: {len(fc['features'])} features")

    # Oracle (UPSERT, sin recrear tabla)
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        MERGE INTO PV_GEO_MUNIS g
        USING (SELECT :1 COD FROM dual) b ON (g.COD_INE = b.COD)
        WHEN MATCHED THEN UPDATE SET g.NOMBRE = :2, g.GEO = :3
        WHEN NOT MATCHED THEN INSERT (COD_INE, NOMBRE, GEO) VALUES (:1, :2, :3)
    """, [codine, nombre_ds, json.dumps(geom, ensure_ascii=False, separators=(",", ":"))])
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM PV_GEO_MUNIS")
    n = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(f"[completar] PV_GEO_MUNIS: {n} filas")


if __name__ == "__main__":
    main()
