"""Descarga los polígonos municipales de la Comunidad de Madrid (OSM/Overpass),
los ensambla POR ID DE NODO con crecimiento bidireccional (exacto), simplifica
con Douglas-Peucker, filtra a los 155 municipios del dataset y los sube a
Oracle como PV_GEO_MUNIS. Deja referencia en oracle_db/sql/05_pv_geo_munis.sql.

Por qué por ids y no por coordenadas: los tramos de una relación se enlazan
por los ids de nodos compartidos (discretos e idénticos en Overpass).
Ensamblando por igualdad de coordenadas, el extremo de un tramo corto puede
"engancharse" a un tramo vecino próximo (mm de diferencia) y aparecen anillos
rotos, saltos internos de kilómetros y municipios partidos en pedazos.

Y el detalle que lo rompía TODO: si un tramo entra al revés, se agrega con la
rebanada CORRECTA:
  cur = cur + list(reversed(t))[1:]     # el [:-1] era el bug histórico
Python quita el ÚLTIMO elemento con [:-1], no el primero: el ensamblador
"entraba" el tramo de cabeza y el anillo cerraba con saltos enormes.

Método de descarga: el dump elegido es el que traiga MÁS relaciones de los
mirrors (kumi a veces entrega vistas parciales de 180/181).

Uso:  python web/descargar_geojson.py
      FORCE_RELOAD=1 fuerza re-descargar aunque exista el dump crudo (caché)
      GEO_MODE=geom   usa la query `out geom` (coords inline) en vez de ids
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import unicodedata
import urllib.request
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from src.common.dataset import cargar_municipios  # noqa: E402
from src.common.oracle import conectar  # noqa: E402

OUT_JSON = REPO / "web" / "geo_municipios_madrid.geojson"
OUT_RAW = REPO / "web" / "osm_raw_cm.json"   # caché local: NO versionado (.gitignore)
SQL_REF = REPO / "oracle_db" / "sql" / "05_pv_geo_munis.sql"

MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
]

# Query en 3 partes: rels (tags + members), ways (ids de nodos), nodes (coords).
# Gramática Overpass: el set de entrada va como prefijo ".rels out body;" —
# escribir "out body .rels;" es un parse error (comprobado en la consola de
# errores del servidor).
QUERY_IDS = """[out:json][timeout:900];
area["name"="Comunidad de Madrid"]["boundary"="administrative"]->.cm;
rel(area.cm)["boundary"="administrative"]["admin_level"="8"]->.rels;
way(r.rels)->.ways;
node(w.ways)->.nodes;
.rels out body;
.ways out body;
.nodes out skel;
"""

# Fallback histórico (funciona en cualquier mirror; coords inline en members)
QUERY_GEOM = """[out:json][timeout:600];
area["name"="Comunidad de Madrid"]["boundary"="administrative"]->.cm;
rel(area.cm)["boundary"="administrative"]["admin_level"="8"];
out geom;
"""


def plano(s: str) -> str:
    """Nombre plano: sin acentos y en minúsculas."""
    return re.sub(r"[\u0300-\u036f]", "", unicodedata.normalize("NFD", s or "")).lower()


def clave_nombre(s: str) -> str:
    """Clave canónica para matching: sin acentos, minúsculas y SIN artículos.

    El dataset trae 'Escorial, El' y OSM trae 'El Escorial' (y variantes con
    La/Los/Las); quitando el artículo ambos producen la misma clave.
    """
    n = plano((s or "").strip())
    n = re.sub(r"\s*,\s*(el|la|los|las)$", "", n)
    n = re.sub(r"^(el|la|los|las)\s+", "", n)
    return re.sub(r"\s+", " ", n).strip()


def cerrar_ring(ring: list) -> list:
    """Cierra el anillo (primer punto = último) y elimina duplicados consecutivos."""
    dedup: list = []
    for pt in ring:
        if not dedup or dedup[-1] != pt:
            dedup.append(pt)
    if len(dedup) > 3 and dedup[0] != dedup[-1]:
        dedup.append(dedup[0])
    return dedup


def dentro_del_anillo(pt: list, ring: list) -> bool:
    """Ray-casting simple para saber si pt está dentro del anillo."""
    x, y = pt
    dentro = False
    for i in range(1, len(ring)):
        x1, y1 = ring[i - 1]
        x2, y2 = ring[i]
        if (y1 > y) != (y2 > y):
            xc = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < xc:
                dentro = not dentro
    return dentro


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


def _clave_pt(pt):
    """Punto hasheable para el ensamblado: id int o tupla (lon,lat)."""
    if isinstance(pt, int):
        return pt
    return (pt[0], pt[1])


def ensamblar_anillos(tramos: list, cerradas_solo: bool = True) -> tuple[list, list]:
    """Enlaza tramos discretos en anillos con crecimiento BIDIRECCIONAL.

    `tramos` son listas de puntos: ids de nodo (int) o pares (lon, lat).
    Devuelve listas de CLAVES de punto: ints en modo ids, tuplas (lon,lat)
    en modo coords. Y (anillos_cerrados, polilineas_abiertas).
    El crecimiento es por los DOS extremos de la cadena: en un anillo, la
    última pieza a veces solo conecta contra el inicio y crecer a una
    dirección provoca el cierre "a tiros" que partía las formas.
    """
    tramos = [[_clave_pt(p) for p in t] for t in tramos if len(t) >= 2]
    extremos: dict = defaultdict(list)
    for idx, t in enumerate(tramos):
        extremos[t[0]].append((idx, False))
        extremos[t[-1]].append((idx, True))

    anillos, abiertas = [], []
    en_uso = [True] * len(tramos)
    for semilla in range(len(tramos)):
        if not en_uso[semilla]:
            continue
        en_uso[semilla] = False
        cur = tramos[semilla][:]
        guard = 0
        while guard < 2000:
            guard += 1
            if len(cur) > 2 and cur[0] == cur[-1]:
                break
            crecido = False
            # 1) extender por el FINAL de la cadena
            for idx, _ in extremos.get(cur[-1], []):
                if not en_uso[idx]:
                    continue
                en_uso[idx] = False
                t = tramos[idx]
                if t[0] == cur[-1]:
                    cur = cur + t[1:]
                else:
                    # el tramo entra al revés: [1:] suelta su primer punto
                    # (el compartido con el extremo de la cadena) y conserva
                    # el orden desde su extremo opuesto
                    cur = cur + list(reversed(t))[1:]
                crecido = True
                break
            # 2) si no: extender por el PRINCIPIO de la cadena
            if not crecido:
                for idx, _ in extremos.get(cur[0], []):
                    if not en_uso[idx]:
                        continue
                    en_uso[idx] = False
                    t = tramos[idx]
                    if t[-1] == cur[0]:
                        cur = list(reversed(t))[1:] + cur
                    else:
                        cur = t[1:] + cur
                    crecido = True
                    break
            if not crecido:
                break
        if len(cur) > 3 and cur[0] == cur[-1]:
            anillos.append(cur)
        elif not cerradas_solo and len(cur) > 3:
            abiertas.append(cur)
    return anillos, abiertas


def dividir_eight(anillo: list) -> list:
    """Divide un anillo fusionado en sub-anillos que comparten nodo de empalme.

    Con municipios cuyo límite forma 'ochos' (dos lazos que se tocan en un
    nodo de grado 4), la cadena ensamblada pasa dos veces por ese nodo y el
    dibujo produce un pinzamiento. Se trocea en lazos disjuntos.
    Opera sobre CLAVES (ids o tuplas); los trozos resultantes son listas de
    claves cerradas (primer elemento = último).
    """
    seq = anillo[:-1] if (len(anillo) > 1 and anillo[0] == anillo[-1]) else anillo[:]
    vistos: dict = {}
    for pos, k in enumerate(seq):
        vistos.setdefault(k, []).append(pos)
    repetidos = {k: v for k, v in vistos.items() if len(v) > 1}
    if not repetidos:
        return [seq + [seq[0]]]
    k, posiciones = min(repetidos.items(), key=lambda kv: kv[1][0])
    i1, i2 = posiciones[0], posiciones[1]
    if i1 == 0 and i2 == len(seq) - 1:
        return [seq + [seq[0]]]
    lazo = seq[i1:i2 + 1]              # cerrado en k
    resto = seq[0:i1 + 1] + seq[i2:]   # también cerrado en k
    trozos = dividir_eight(lazo) + dividir_eight(resto)
    return [t for t in trozos if len(t) > 3]


def descargar_osm() -> dict:
    """Descarga el dump de Overpass o reutiliza el dump crudo local (caché).

    Se queda con el dump que traiga MÁS relaciones: algunos mirrors
    devuelven vistas parciales (kumi a veces omite relaciones, v. g. Griñón).
    Para temprano si un mirror entrega >= 181 (179 municipios + margen).
    """
    if OUT_RAW.exists() and not os.environ.get("FORCE_RELOAD"):
        print(f"[geo] reutilizando dump crudo: {OUT_RAW}", flush=True)
        return json.loads(OUT_RAW.read_text(encoding="utf-8"))

    modo = os.environ.get("GEO_MODE", "ids")
    query = QUERY_GEOM if modo == "geom" else QUERY_IDS
    last = ""
    mejor = None
    mejores_rels = -1
    for paso in range(24):
        url = MIRRORS[paso % len(MIRRORS)]
        req = urllib.request.Request(url, data=query.encode("utf-8"),
                                     headers={"User-Agent": "datathon-mapa/1.0"})
        try:
            print(f"[geo] [{paso}] descargando de {url} ...", flush=True)
            with urllib.request.urlopen(req, timeout=900) as r:
                data = json.loads(r.read().decode("utf-8"))
            rels = [e for e in data.get("elements", []) if e["type"] == "relation"]
            print(f"[geo] {len(rels)} relaciones", flush=True)
            if len(rels) > mejores_rels:
                mejor, mejores_rels = data, len(rels)
            if mejores_rels >= 181:
                break
            if paso >= 2 * len(MIRRORS) - 1:
                break
            last = f"dump corto: {len(rels)} relaciones"
            print(f"[geo] {last}; guardado como mejor hasta ahora", flush=True)
        except Exception as e:
            last = str(e)[:120]
            # 400 = error de gramática: cambia al modo geom (funciona seguro)
            body = getattr(e, "read", None)
            if body is not None:
                try:
                    cuerpo = body().decode(errors="replace")
                    err = re.findall(r"<strong[^>]*>([^<]+)</strong>", cuerpo)
                    if err:
                        last += " | " + " ".join(err[:2])[:150]
                        if modo == "ids":
                            print(f"[geo] {url}: 400 -> cambio a modo geom", flush=True)
                            modo = "geom"
                            query = QUERY_GEOM
                            continue
                except Exception:
                    pass
            print(f"[geo] fallo {url}: {last}", flush=True)
        time.sleep(30)
    if mejor is None:
        raise SystemExit(f"[geo] sin dump tras los intentos: {last}")
    OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT_RAW.write_text(json.dumps(mejor, ensure_ascii=False), encoding="utf-8")
    return mejor


def main() -> None:
    data = descargar_osm()

    # 1) estructura: nodos, ways (por node ids), relations
    nodos = {e["id"]: [e["lon"], e["lat"]] for e in data["elements"] if e["type"] == "node"}
    ways = {e["id"]: e.get("nodes") for e in data["elements"] if e["type"] == "way" and e.get("nodes")}
    modo_ids = bool(ways)
    print(f"[geo] modo ensamblado: {'ids de nodo' if modo_ids else 'coords (out geom)'}", flush=True)

    features = []
    for rel in (e for e in data["elements"] if e["type"] == "relation"):
        tags = rel.get("tags", {})
        if modo_ids:
            outer_tramos = [ways[m["ref"]] for m in rel.get("members", [])
                            if m.get("type") == "way" and m.get("role") in ("outer", "") and m["ref"] in ways]
            inner_tramos = [ways[m["ref"]] for m in rel.get("members", [])
                            if m.get("type") == "way" and m.get("role") == "inner" and m["ref"] in ways]
            outer_anillos, outer_abiertas = ensamblar_anillos(outer_tramos)
            inner_anillos, _ = ensamblar_anillos(inner_tramos)
            outer_anillos = [t for a in outer_anillos for t in dividir_eight(a)]
            inner_anillos = [t for a in inner_anillos for t in dividir_eight(a)]
            outer_rings = [cerrar_ring([[nodos[n][0], nodos[n][1]] for n in anillo])
                           for anillo in outer_anillos if len(anillo) > 3]
            inner_rings = [cerrar_ring([[nodos[n][0], nodos[n][1]] for n in anillo])
                           for anillo in inner_anillos if len(anillo) > 3]
        else:
            outer_geoms = [m["geometry"] for m in rel.get("members", [])
                           if m.get("role") in ("outer", "") and "geometry" in m]
            inner_geoms = [m["geometry"] for m in rel.get("members", [])
                           if m.get("role") == "inner" and "geometry" in m]
            outer_anillos, outer_abiertas = ensamblar_anillos(outer_geoms, cerradas_solo=False)
            inner_anillos, _ = ensamblar_anillos(inner_geoms, cerradas_solo=False)
            outer_anillos = [t for a in outer_anillos for t in dividir_eight(a)]
            inner_anillos = [t for a in inner_anillos for t in dividir_eight(a)]
            outer_rings = [cerrar_ring([[x, y] for (x, y) in anillo]) for anillo in outer_anillos if len(anillo) > 3]
            inner_rings = [cerrar_ring([[x, y] for (x, y) in anillo]) for anillo in inner_anillos if len(anillo) > 3]
        if not outer_rings:
            print(f"[geo] SIN anillo: {tags.get('name')} "
                  f"({len(outer_tramos) if modo_ids else len(outer_geoms)} tramos ext.)", flush=True)
            continue
        if outer_abiertas:
            print(f"[geo] AVISO '{tags.get('name')}': {len(outer_abiertas)} tramo(s) exterior NO cerrado",
                  flush=True)
        poligonos = []
        inner_restantes = list(inner_rings)
        for oring in outer_rings:
            huecos = [h for h in inner_restantes if dentro_del_anillo(h[0], oring)]
            poligonos.append([oring] + huecos)
            for h in huecos:
                inner_restantes.remove(h)
        ref = tags.get("ref", "")
        cod = (ref if re.fullmatch(r"\d{4,5}", ref or "") else "").zfill(5)
        features.append({"cod": cod, "nombre": tags.get("name", ""), "poligonos": poligonos})

    # 2) matching con los 155 del dataset (por ref INE, por nombre y variantes)
    munis = cargar_municipios()
    nombres_planos: dict = {}
    for nombre_muni, cod_muni in munis.set_index("municipio")["cod_ine"].items():
        clave = clave_nombre(nombre_muni)
        if clave in nombres_planos and nombres_planos[clave] != cod_muni:
            print(f"[geo] AVISO: colisión de nombre canónico '{clave}' "
                  f"({nombres_planos[clave]} vs {cod_muni})")
        nombres_planos[clave] = cod_muni

    salida = {}
    for f in features:
        cod = f["cod"] if f["cod"] in munis["cod_ine"].values else None
        if cod is None:
            clave_full = clave_nombre(f["nombre"])
            if clave_full in nombres_planos:
                cod = nombres_planos[clave_full]
            else:
                # nombres OSM compuestos con guion: 'El Boalo-Cerceda-Mataelpino'
                for parte in (f["nombre"] or "").split("-"):
                    clave_parte = clave_nombre(parte)
                    if clave_parte in nombres_planos:
                        cod = nombres_planos[clave_parte]
                        break
        if cod and cod not in salida:
            salida[cod] = f["poligonos"]

    faltan = set(munis["cod_ine"]) - set(salida)
    print(f"[geo] municipios con polígono: {len(salida)}/155 | sin polígono: {sorted(faltan) or 'ninguno'}", flush=True)

    # 3) simplificar, redondear y montar el GeoJSON
    fc = {"type": "FeatureCollection", "features": []}
    tbl_munis = munis.set_index("cod_ine")
    for cod, poligonos in sorted(salida.items()):
        poligonos_s = []
        saltos_crudos = 0
        for poligono in poligonos:
            # los saltos de ENSAMBLAJE se miden sobre el dato CRUDO (antes de
            # simplificar): los lados rectos largos y reales (0.03-0.05°;
            # límites rectos entre municipios) se detectan bien ahí, y una
            # vez el DP los comprime a un segmento dejarían de distinguirse.
            for ring in poligono:
                for a, b in zip(ring, ring[1:]):
                    if ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 > 0.05:
                        saltos_crudos += 1
            pg = [[[round(x, 5), round(y, 5)] for x, y in dp_simplify(ring, 0.0004)] for ring in poligono]
            pg = [r for r in pg if len(r) >= 4]
            if pg and len(pg[0]) >= 4:
                poligonos_s.append(pg)
        if saltos_crudos:
            print(f"[geo] invalido {cod} ({tbl_munis.loc[cod, 'municipio']}): "
                  f"{saltos_crudos} salto(s) de ensamblaje > 5 km", flush=True)
            continue
        if not poligonos_s:
            continue
        geom = ({"type": "Polygon", "coordinates": poligonos_s[0]}
                if len(poligonos_s) == 1
                else {"type": "MultiPolygon", "coordinates": poligonos_s})
        fc["features"].append({
            "type": "Feature",
            "properties": {"cod": cod, "nombre": tbl_munis.loc[cod, "municipio"]},
            "geometry": geom,
        })

    # 3b) validación estricta ANTES de tocar la base: cierre de anillos
    invalidos = []
    for f in fc["features"]:
        g = f["geometry"]
        rings = (g["coordinates"] if g["type"] == "Polygon"
                 else [r for p in g["coordinates"] for r in p])
        for ring in rings:
            if len(ring) < 4 or tuple(ring[0]) != tuple(ring[-1]):
                invalidos.append(f["properties"]["cod"])
                break
    if invalidos:
        raise SystemExit(f"[geo] features inválidas: {sorted(invalidos)}")
    multipol = [(f["properties"]["cod"], len(f["geometry"]["coordinates"]))
                for f in fc["features"] if f["geometry"]["type"] == "MultiPolygon"]
    print(f"[geo] {len(fc['features'])} features válidas | multi: {len(multipol)}", flush=True)

    OUT_JSON.write_text(json.dumps(fc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"[geo] GeoJSON: {OUT_JSON} ({OUT_JSON.stat().st_size / 1024:.0f} KB)", flush=True)

    # 4) subir a Oracle
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

    # 5) referencia SQL (los INSERTs van por binds; ver web/descargar_geojson.py)
    SQL_REF.parent.mkdir(parents=True, exist_ok=True)
    SQL_REF.write_text(
        "-- 05_pv_geo_munis — polígonos municipales para el mapa (fuente: OSM vía Overpass API,\n"
        "-- ensamblados POR ID DE NODO con crecimiento bidireccional, simplificados con\n"
        "-- Douglas-Peucker eps=0.0004°, coords a 5 decimales). Dump crudo reproducible en\n"
        "-- web/osm_raw_cm.json (caché local, no versionada; FORCE_RELOAD=1 para re-descargar).\n"
        "-- La carga se hace con binds desde web/descargar_geojson.py (los CLOB son grandes).\n"
        "-- Verificar: SELECT COUNT(*) FROM PV_GEO_MUNIS;  -- = 155\n",
        encoding="utf-8",
    )
    cur.close()
    conn.close()
    print("[geo] PV_GEO_MUNIS cargada en Oracle: OK", flush=True)


if __name__ == "__main__":
    main()
