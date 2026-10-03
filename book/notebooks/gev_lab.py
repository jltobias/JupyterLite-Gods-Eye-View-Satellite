"""Small, auditable geospatial helpers shared by CPython and JupyterLite.

All scenario inputs are fictional. GeoJSON uses [longitude, latitude].
No network, credentials, or heavyweight GIS libraries are required here.
"""
from pathlib import Path
from html import escape
import base64
import csv
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent
EARTH_KM = 6371.0088
AS_OF = "2026-09-15T12:00:00Z"


def load_scenario():
    return json.loads((ROOT / "data/riverbend.geojson").read_text(encoding="utf-8"))


def load_cases():
    with (ROOT / "data/daily_cases.csv").open(encoding="utf-8", newline="") as stream:
        return [{**r, "cases": int(r["cases"])} for r in csv.DictReader(stream)]


def sectors(collection=None):
    return [f for f in (collection or load_scenario())["features"]
            if f["properties"]["kind"] == "sector"]


def haversine_km(lon1, lat1, lon2, lat2):
    """Great-circle distance on the mean-radius sphere, with broadcasting."""
    a, b, c, d = map(np.deg2rad, (lon1, lat1, lon2, lat2))
    h = np.sin((d-b)/2)**2 + np.cos(b)*np.cos(d)*np.sin((c-a)/2)**2
    return 2 * EARTH_KM * np.arcsin(np.sqrt(np.clip(h, 0, 1)))


def rate_per_10000(cases, population):
    """Return NaN for missing/nonpositive denominators, never a false zero."""
    cases, population = np.broadcast_arrays(np.asarray(cases, float), np.asarray(population, float))
    if np.any(cases < 0):
        raise ValueError("Cases must be nonnegative")
    return np.divide(cases * 10000, population, out=np.full(cases.shape, np.nan),
                     where=np.isfinite(population) & (population > 0))


def wilson_interval(cases, population, z=1.96):
    """Binomial proportion interval; assumes unique first episodes and a closed cohort."""
    k, n = np.broadcast_arrays(np.asarray(cases, float), np.asarray(population, float))
    if np.any(n <= 0) or np.any(k < 0) or np.any(k > n):
        raise ValueError("Require 0 <= cases <= population and population > 0")
    p = k / n
    center = (p + z*z/(2*n)) / (1 + z*z/n)
    half = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return np.maximum(0, center-half), np.minimum(1, center+half)


def rook_weights(rows=3, cols=4):
    n = rows * cols
    w = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            w[i, j] = abs(i//cols-j//cols) + abs(i%cols-j%cols) == 1
    return w


def moran_i(values, weights):
    """Global Moran's I with symmetric binary adjacency (not row standardized)."""
    x = np.asarray(values, float)
    w = np.asarray(weights, float)
    if x.ndim != 1 or w.shape != (len(x), len(x)) or not np.isfinite(x).all():
        raise ValueError("Finite vector and matching square weights required")
    z = x - x.mean()
    if z @ z == 0 or w.sum() == 0:
        raise ValueError("Moran's I undefined for a constant field or no neighbors")
    return len(x) / w.sum() * (z @ w @ z) / (z @ z)


def sector_summary(collection=None):
    features = sectors(collection)
    rows = load_cases()
    totals = {f["id"]: 0 for f in features}
    for r in rows:
        totals[r["sector_id"]] += r["cases"]
    return [{**f["properties"], "id": f["id"], "cases": totals[f["id"]],
             "rate_10000": float(rate_per_10000(totals[f["id"]], f["properties"]["population"]))}
            for f in features]


def styled_sectors():
    collection = load_scenario()
    stats = {r["id"]: r for r in sector_summary(collection)}
    for f in collection["features"]:
        if f["id"] in stats:
            f["properties"].update(stats[f["id"]])
    return collection


def evidence_bundle():
    """Aggregates only: deliberately excludes patient locations and line lists."""
    stats = sector_summary()
    return {
        "scenario": "Riverbend synthetic exercise", "synthetic": True, "as_of": AS_OF,
        "period": "2026-09-01/2026-09-14", "crs": "OGC:CRS84",
        "sources": [
            {"id": "S1", "path": "data/riverbend.geojson", "description": "Fictional sectors, population and clinics"},
            {"id": "S2", "path": "data/daily_cases.csv", "description": "Synthetic reported first episodes by onset day; last 3 days incomplete"}
        ],
        "metrics": {
            "reported_cases": sum(r["cases"] for r in stats),
            "population": sum(r["population"] for r in stats),
            "sectors": [{k: r[k] for k in ("id", "population", "cases", "rate_10000", "flood_fraction")}
                        for r in stats]
        },
        "limitations": ["Fictional training data, not a real outbreak", "Final 3 onset days have reporting delay",
                        "No causal inference from spatial overlap", "Flood fractions are invented, not satellite measurements"]
    }


def validate_geojson(data):
    """Validate the intentionally narrow Point/LineString/Polygon lab interchange."""
    if data.get("type") != "FeatureCollection" or not isinstance(data.get("features"), list):
        raise ValueError("Expected a GeoJSON FeatureCollection")
    ids = set()
    def point(p):
        if not isinstance(p, (list, tuple)) or len(p) != 2:
            raise ValueError("Use 2D longitude/latitude coordinates")
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in p):
            raise ValueError("Coordinates must be finite numbers")
        if not (-180 <= p[0] <= 180 and -90 <= p[1] <= 90):
            raise ValueError("Coordinate outside longitude/latitude bounds")
    for f in data["features"]:
        if f.get("type") != "Feature" or not isinstance(f.get("properties"), dict):
            raise ValueError("Invalid feature")
        key = f.get("id")
        if not isinstance(key, str) or key in ids:
            raise ValueError("Unique string feature IDs required")
        ids.add(key)
        g = f.get("geometry", {})
        coords = g.get("coordinates", [])
        if g.get("type") == "Point":
            point(coords)
        elif g.get("type") == "LineString":
            if len(coords) < 2:
                raise ValueError("Line needs at least two points")
            for p in coords:
                point(p)
        elif g.get("type") == "Polygon":
            if not coords:
                raise ValueError("Polygon needs a ring")
            for ring in coords:
                if len(ring) < 4 or ring[0] != ring[-1]:
                    raise ValueError("Polygon rings must be closed")
                for p in ring:
                    point(p)
        else:
            raise ValueError("Only Point, LineString and Polygon supported in these labs")
    return data


def map_page(collection=None, mode="2d"):
    if mode not in ("2d", "3d"):
        raise ValueError("mode must be 2d or 3d")
    data = validate_geojson(collection or styled_sectors())
    template = (ROOT / "viewers" / ("map2d.html" if mode == "2d" else "scene3d.html")).read_text(encoding="utf-8")
    # Escape '<' so data cannot terminate a script element.
    return template.replace("__SCENARIO_JSON__", json.dumps(data, allow_nan=False).replace("<", "\\u003c"))


def show_map(collection=None, mode="2d", height=650):
    from IPython.display import HTML, display
    page = map_page(collection, mode)
    display(HTML(f'<iframe title="Riverbend synthetic {mode} training map" width="100%" height="{int(height)}" '
                 f'style="border:1px solid #27465e;border-radius:12px" '
                 f'sandbox="allow-scripts allow-same-origin allow-downloads" srcdoc="{escape(page, quote=True)}"></iframe>'))


def download(name, value, mime="application/json"):
    """A browser download works in JupyterLite even when kernel files are virtual."""
    from IPython.display import HTML, display
    body = value if isinstance(value, str) else json.dumps(value, indent=2, allow_nan=False)
    encoded = base64.b64encode(body.encode()).decode()
    display(HTML(f'<a download="{escape(name, quote=True)}" href="data:{escape(mime, quote=True)};base64,{encoded}">'
                 f'Download {escape(name)}</a>'))


def plot_sectors(ax, values, title, cmap="YlOrRd"):
    from matplotlib.collections import PolyCollection
    fs = sectors()
    coll = PolyCollection([f["geometry"]["coordinates"][0] for f in fs],
                          array=np.asarray(values, float), cmap=cmap, edgecolors="white", linewidths=1.5)
    ax.add_collection(coll)
    coll.autoscale()
    for f, value in zip(fs, values):
        p = f["properties"]
        red, green, blue, _ = coll.cmap(coll.norm(value))
        label_color = "white" if .2126*red + .7152*green + .0722*blue < .48 else "#152639"
        ax.text(p["lon"], p["lat"], f["id"], ha="center", va="center", fontsize=8, color=label_color)
    ax.autoscale_view()
    ax.set(xlabel="Longitude (degrees east)", ylabel="Latitude (degrees north)", title=title)
    ax.set_aspect(1/np.cos(np.deg2rad(7.8)))
    return coll
