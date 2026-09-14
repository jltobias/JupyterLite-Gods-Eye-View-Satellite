# JupyterLite God's Eye View — Satellite Examples

Browser-only JupyterLite notebooks and a Jupyter Book that explore satellite/orbital concepts inspired by [Bilawal Sidhu's **God's Eye View**](https://github.com/bilawalsidhu/gods-eye-view).

## Live sites

| Resource | Live link |
|---|---|
| **Jupyter Book** | https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/ |
| **JupyterLite Lab** | https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html |
| Orbital ground track notebook | https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html?path=01_orbit_ground_track.ipynb |
| Sensor / line-of-sight footprint notebook | https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html?path=02_sensor_footprint.ipynb |
| Synthetic constellation dashboard | https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html?path=03_constellation_dashboard.ipynb |
| **Akobo, South Sudan satellite imagery HUD** | https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html?path=04_akobo_satellite_imagery.ipynb |
| Akobo notebook in the Jupyter Book | https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/notebooks/04_akobo_satellite_imagery.html |

The GitHub Actions workflow builds both sites on pushes to `main`. If this repository has not used GitHub Pages before, enable **Settings → Pages → Build and deployment → Source: GitHub Actions** once; the URLs above are the standard GitHub Pages locations for this repository.

## What is included

1. **Orbital ground track** — a simplified circular two-body orbit transformed onto a rotating Earth.
2. **Sensor / line-of-sight footprint** — spherical-Earth horizon geometry and a surface footprint ring.
3. **Synthetic constellation dashboard** — a small Walker-like synthetic constellation, global sub-satellite view, and occupancy grid.
4. **Akobo satellite imagery HUD** — a live Esri World Imagery view centered on Akobo, South Sudan, with pan/zoom, coordinate readout, center reticle, 5/15/30 km rings, and optional display filters inspired by the visual language of the upstream demos.
5. **Jupyter Book** — narrative documentation, notebook rendering, and attribution/source notes.
6. **JupyterLite** — the same notebooks running client-side in a Pyodide Python kernel; no notebook server is required.

These examples are intentionally lightweight and original. They do **not** copy the upstream application's JavaScript/Cesium implementation or bundle its third-party datasets. The Akobo notebook requests Esri imagery directly from Esri at runtime and keeps the imagery attribution visible.

## Upstream project citation

Primary inspiration and reference implementation:

> **Bilawal Sidhu. _God's Eye View_ (2026).** GitHub: https://github.com/bilawalsidhu/gods-eye-view

The upstream project describes itself as a browser-based situational-awareness globe with live aircraft, ships, satellites, earthquakes, traffic, public cameras, and other public signals. Its satellite implementation uses [`satellite.js`](https://github.com/shashwatak/satellite-js) for orbital propagation and documents **CelesTrak** as the TLE source. Its keyless satellite basemap uses **Esri World Imagery**.

Upstream licensing and attribution documents:

- Source-code license: https://github.com/bilawalsidhu/gods-eye-view/blob/main/LICENSE
- Data sources and provider terms: https://github.com/bilawalsidhu/gods-eye-view/blob/main/DATA_SOURCES.md
- Bundled 3D-model provenance: https://github.com/bilawalsidhu/gods-eye-view/blob/main/public/models/README.md

The upstream code is MIT-licensed (copyright © 2026 Bilawal Sidhu), but its license expressly states that the MIT grant does **not** extend to third-party datasets, runtime data providers, or third-party 3D assets. Those remain subject to their respective licenses and terms.

## Upstream data/source attribution

The upstream `DATA_SOURCES.md` is the authoritative list. Important providers documented there include:

| Source | Used by God's Eye View for | Attribution / terms noted upstream |
|---|---|---|
| **CelesTrak** | Satellite TLEs / SGP4 | Credit: “CelesTrak (celestrak.org), Dr. T.S. Kelso”; citation requested. |
| **Esri World Imagery** | Keyless satellite basemap | Esri/provider attribution required; provider terms apply. |
| **Re:Earth Terrain / Mapterhorn** | Keyless terrain | Terrain mesh CC BY 4.0; EGM2008 geoid material U.S. public-domain-origin. |
| **OpenStreetMap / Overpass** | Roads and mapped context | ODbL 1.0; © OpenStreetMap contributors. |
| **OpenSky Network** | Primary live-flight snapshot | Upstream documents non-commercial research/education restrictions; consult provider terms. |
| **adsb.lol** | Flight fallback, military traffic, traces | ODbL 1.0. |
| **AISStream.io** | Live vessels | Courtesy attribution; provider/service terms apply. |
| **The Space Devs — Launch Library 2** | Launch/payload/stage/recovery context | Provider terms and API limits apply; attribution encouraged. |
| **USGS** | Earthquakes | U.S. public domain; courtesy attribution. |
| **Open-Meteo** | Weather | CC BY 4.0 with attribution requirements. |
| **GDELT Project** | Regional-news fallback | Citation/link required under upstream-documented terms. |
| **City/transport camera providers** | Public CCTV layers | Provider-specific open-data terms; several require attribution. |
| **TeleGeography Submarine Cable Map** | Bundled cable layer | CC BY-NC-SA 3.0; **NonCommercial**. Upstream warns commercial users to remove or separately license it. |
| **OpenStreetMap-derived datacenters/dams** | Bundled infrastructure | ODbL 1.0. |
| **NASA FIRMS** | Active-fire data | Upstream documents U.S. public-domain/CC0-origin with citation requested. |

See the upstream [`DATA_SOURCES.md`](https://github.com/bilawalsidhu/gods-eye-view/blob/main/DATA_SOURCES.md) before integrating any real feed. Provider licenses, quotas, authentication requirements, and commercial-use rules are independent of this repository.

### Data actually used in this repository

The first three notebooks use **synthetic orbital parameters only** plus standard mathematical/physical constants.

The fourth notebook uses **Esri World Imagery at runtime** to display Akobo, South Sudan. Imagery tiles are fetched directly from Esri in the browser and are not committed, cached, or redistributed by this repository. The notebook displays the provider credit **“Powered by Esri — Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community.”** The Akobo view is centered at approximately **7.79293° N, 33.00294° E**, based on OpenStreetMap/GeoNames-derived place references.

Its MONO, NVG-like, and THERMAL-like buttons are only browser display filters; they do not represent real sensor products.

## Local build

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter-book build book
jupyter lite build --contents book/notebooks --output-dir book/_build/html/lite
```

Open `book/_build/html/index.html` for the Jupyter Book and `book/_build/html/lite/lab/index.html` for JupyterLite.

## Repository structure

```text
.github/workflows/deploy-pages.yml   GitHub Pages build/deploy
book/
  _config.yml                        Jupyter Book configuration
  _toc.yml                           Book table of contents
  intro.md                           Book landing page
  attribution.md                     Attribution and source notes
  notebooks/
    01_orbit_ground_track.ipynb
    02_sensor_footprint.ipynb
    03_constellation_dashboard.ipynb
    04_akobo_satellite_imagery.ipynb
requirements.txt
```

## Disclaimer

This is an independent educational repository. It is not affiliated with or endorsed by Bilawal Sidhu, CelesTrak, Esri, OpenStreetMap, OpenSky, or other upstream providers. Simplified notebook calculations and display effects are for learning and visualization, not operational orbit determination, targeting, navigation, sensor analysis, or safety-of-life use.
