"""Descarga los polígonos municipales de la Comunidad de Madrid (OSM/Overpass),
los simplifica, filtra a los 155 municipios del dataset y los sube a Oracle
como PV_GEO_MUNIS (cod_ine, nombre, geo CLOB). Deja referencia en
oracle_db/sql/05_pv_geo_munis.sql.

Uso:  python mcp/descargar_geojson.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from src.common.dataset import cargar_panel, cargar_municipios  # noqa: E402
from src.common.oracle import conectar  # noqa: E402

OUT_JSON = REPO / "data" / "geo_municipios_madrid.geojson"
SQL_REF = REPO / "oracle_db" / "sql" / "05_pv_geo_munis.sql"

OVERPASS_URLS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
]

QUERY = """[out:json][timeout:600];
area["name"="Comunidad de Madrid"]["boundary"="administrative"]->.cm;
rel(area.cm)["boundary"="administrative"]["admin_level"="8"];
out geom;
"""


def plano(s: str) -> str:
    return re.sub(r"[\u0300-\u036f]", "", (s or "").normalize("NFD") if False else __import__("unicodedata").normalize("NFD", s or "")).lower()


def dp_simplify(points: list[list[float]], eps: float) -> list[list[float]]:
    """Douglas-Peucker simple (recursivo) sobre [[lon,lat],...]."""
    if len(points) < 3:
        return points

    def perp(p, a, b):
        ax, ay = a
        bx, by = b
        px, py = p
        dx, dy = bx - ax, by - ay
        L = dx * dx + dy * dy
        if L == 0:
            d2 = (px - ax) ** 2 + (py - ay) ** 2
        else:
            t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
            d2 = (px - ax - t * dx) ** 2 + (py - ay - t * dy) ** 2
        return d2

    dmax, idx = 0.0, 0
    for i in range(1, len(points) - 1):
        d = perp(points[i], points[0], points[-1])
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps * eps:
        left = dp_simplify(points[: idx + 1], eps)
        right = dp_simplify(points[idx:], eps)
        return left[:-1] + right
    return [points[0], points[-1]]


def ensamblar_anillos(ways: list[list]) -> list[list[list[float]]]:
    """Enlaza tramos (listas de [lon,lat]) por extremos coincidentes en anillos."""
    pend = [w[:] for w in ways]
    anillos = []
    while pend:
        cur = pend.pop(0)
        guard = 0
        while guard < 500:
            guard += 1
            start, end = cur[0], cur[-1]
            if end == cur[0] and len(cur) > 2:
                break
            nxt = None
            for i, w in enumerate(pend):
                if w[0] == end:
                    nxt = (i, w[1:])
                    break
                if w[-1] == end:
                    nxt = (i, list(reversed(w))[:-1])
                    break
            if nxt is None:
                break
            i, cont = nxt
            cur = cur + cont
            pend.pop(i)
        if len(cur) > 3:
            anillos.append(cur)
    return anillos


def main() -> None:
    panel = cargar_panel()
    munis = cargar_municipios()
    nombres = {}  # nombre plano -> cod_ine

    # 1) Overpass (sigue probando hasta recibir relaciones)
    data = None
    for url in OVERPASS_URLS + OVERPASS_URLS:  # dos pasadas por si la primera está fría
        try:
            print(f"[geo] descargando de {url} ...", flush=True)
            req = urllib.request.Request(url, data=QUERY.encode("utf-8"), headers={"User-Agent": "datathon-mapa/1.0"})
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.loads(r.read().decode("utf-8"))
            n = len(data.get("elements", []))
            print(f"[geo] {n} relaciones recibidas", flush=True)
            if n > 0:
                break
        except Exception as e:
            print(f"[geo] fallo {url}: {str(e)[:120]}", flush=True)
    if not data or not data.get("elements"):
        raise SystemExit("[geo] no se pudo descargar de ningún mirror")

    # 2) construir polígonos por municipio
    features = []
    for rel in data.get("elements", []):
        tags = rel.get("tags", {})
        outer = [m["geometry"] for m in rel.get("members", []) if m.get("role") in ("outer", "") and "geometry" in m]
        inner = [m["geometry"] for m in rel.get("members", []) if m.get("role") == "inner" and "geometry" in m]
        if not outer:
            continue
        outer_rings = ensamblar_anillos([[[pt["lon"], pt["lat"]] for pt in g] for g in outer])
        if not outer_rings:
            continue
        inner_rings = ensamblar_anillos([[[pt["lon"], pt["lat"]] for pt in g] for g in inner])
        anillo = max(outer_rings, key=len)  # el municipio: anillo exterior mayor
        rings = [anillo] + inner_rings
        ref = tags.get("ref", "")
        cod = (ref if re.fullmatch(r"\d{4,5}", ref or "") else "").zfill(5)
        nombre = tags.get("name", "")
        features.append({"cod": cod, "nombre": nombre, "rings": rings})

    # 3) matchear con los 155 del dataset (por ref o por nombre plano)
    nombres_planos = {plano(k): v for k, v in munis.set_index("municipio")["cod_ine"].items()}
    salida = {}
    usados = set()
    for f in features:
        cod = None
        if f["cod"] and f["cod"] in munis["cod_ine"].values:
            cod = f["cod"]
        elif plano(f["nombre"]) in nombres_planos:
            cod = nombres_planos[plano(f["nombre"])]
        if cod and cod not in usados:
            usados.add(cod)
            salida[cod] = f["rings"]

    faltan = set(munis["cod_ine"]) - set(salida)
    print(f"[geo] municipios con polígono: {len(salida)}/155 | sin polígono: {len(faltan)}")
    if faltan:
        print("[geo] faltan:", sorted(faltan)[:20])

    # 4) simplificar y redondear
    fc = {"type": "FeatureCollection", "features": []}
    for cod, rings in sorted(salida.items()):
        rings_s = [
            [[round(x, 5), round(y, 5)] for x, y in dp_simplify(ring, 0.0004)]
            for ring in rings
        ]
        nombre = munis.set_index("cod_ine").loc[cod, "municipio"]
        fc["features"].append({
            "type": "Feature",
            "properties": {"cod": cod, "nombre": nombre},
            "geometry": {"type": "Polygon", "coordinates": rings_s},
        })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(fc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    size = OUT_JSON.stat().st_size
    print(f"[geo] GeoJSON: {OUT_JSON} ({size / 1024:.0f} KB, {len(fc['features'])} features)")

    # 5) subir a Oracle
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("DROP TABLE PV_GEO_MUNIS PURGE")
    except Exception:
        pass
    cur.execute("""
        CREATE TABLE PV_GEO_MUNIS (
            COD_INE VARCHAR2(5) NOT NULL PRIMARY KEY,
            NOMBRE  VARCHAR2(120),
            GEO     CLOB
        ) LOB (GEO) STORE AS SECUREFILE
    """)
    for feat in fc["features"]:
        cur.execute(
            "INSERT INTO PV_GEO_MUNIS (COD_INE, NOMBRE, GEO) VALUES (:1, :2, :3)",
            [feat["properties"]["cod"], feat["properties"]["nombre"],
             json.dumps(feat["geometry"], ensure_ascii=False, separators=(",", ":"))],
        )
    conn.commit()

    # 6) referencia SQL (DDL + comentario de método; los INSERTs van por bind)
    SQL_REF.parent.mkdir(parents=True, exist_ok=True)
    SQL_REF.write_text(
        "-- 05_pv_geo_munis — polígonos municipales para el mapa (fuente: OSM vía Overpass API,\n"
        "-- simplificados con Douglas-Peucker eps=0.0004°, coords redondeadas a 5 decimales).\n"
        "-- La carga se hace con binds desde mcp/descargar_geojson.py (los CLOB son grandes).\n"
        "-- Verificar: SELECT COUNT(*) FROM PV_GEO_MUNIS;  -- = 155\n",
        encoding="utf-8",
    )
    cur.close()
    conn.close()
    print("[geo] PV_GEO_MUNIS cargada en Oracle ✓")


if __name__ == "__main__":
    main()
