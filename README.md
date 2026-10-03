# God's Eye View · Geospatial Learning Lab

![Illustrative Earth-observation and global-health workbench; artwork map panels are synthetic](book/assets/geospatial-lab-hero.png)

**Explore. Compute. Question. Explain.** Twelve browser-ready notebooks connect satellite geometry, 2D/3D maps, emergency operations, spatial epidemiology, and GPT-6 Astra-assisted analysis.

[**Read the Jupyter Book**](https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/) · [**Launch JupyterLite**](https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html) · [**2D EOC demo**](https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/_static/demos/riverbend-2d.html) · [**3D scene demo**](https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/_static/demos/riverbend-3d.html)

An independent educational companion to [Bilawal Sidhu's **God's Eye View**](https://github.com/bilawalsidhu/gods-eye-view), with original Python labs, Leaflet/Cesium teaching viewers, and an optional adapter for loading notebook layers into the actual upstream app. **NASA Worldview**, used in lab 08, is a separate NASA imagery application.

## Start with a mission

| Mission | Route | Produce |
|---|---|---|
| Browser EOC | 05 → 07 → 09 → 12 | Common operating picture, clinic-access comparison, 3D handover |
| Spatial epidemiology and global health | 06 → 08 → 11 → 12 | Onset curve, rates, imagery provenance, spatial uncertainty |
| Astra as an analysis partner | 05 → 10 → 12 | Aggregate evidence packet and a structured, reviewed briefing |
| Satellite foundations | 01 → 02 → 03 → 04 | Ground tracks, visibility geometry and imagery context |

The **Riverbend exercise is fictional**. Its sectors, clinics, populations, cases, and flood fractions describe no real outbreak or community. Analysis runs with bundled data and no model key. Interactive libraries require CDN access; optional imagery and NASA links require their providers. Initial JupyterLite startup downloads its runtime/packages. This is not an air-gapped or operational EOC deployment.

![Same fictional sectors compared by workload, population-normalized reports and invented flood exposure](book/assets/analytical-preview.png)

## Notebook gallery

| Lab | Explore | Artifact / exercise |
|---|---|---|
| [01 · Orbital ground track](book/notebooks/01_orbit_ground_track.ipynb) | Circular orbit and rotating Earth; 3D surface trace | Check inclination and period |
| [02 · Sensor footprint](book/notebooks/02_sensor_footprint.ipynb) | Horizon and minimum-elevation geometry | Compare geometric visibility limits |
| [03 · Constellation](book/notebooks/03_constellation_dashboard.ipynb) | Synthetic subpoints and site access over time | Distinguish occupancy from coverage |
| [04 · Akobo imagery](book/notebooks/04_akobo_satellite_imagery.ipynb) | Esri satellite basemap, HUD, distance and provenance | Label acquisition-date uncertainty |
| [05 · EOC picture](book/notebooks/05_eoc_common_operating_picture.ipynb) | Linked count/rate/exposure maps, status and freshness | Export an interactive map and GeoJSON |
| [06 · Spatial epidemiology](book/notebooks/06_spatial_epidemiology.ipynb) | Onset curve, denominators, Wilson intervals, reporting delay | Interpret a rate without claiming causation |
| [07 · Health access](book/notebooks/07_health_access_logistics.ipynb) | Clinic closure, distance, speed and capacity sensitivity | Identify modeling assumptions |
| [08 · NASA Worldview](book/notebooks/08_worldview_remote_sensing.ipynb) | Dated imagery requests, synthetic NDWI and cloud masking | Export an imagery manifest |
| [09 · 3D scenes](book/notebooks/09_cesium_3d_scenes.ipynb) | Cesium 2D/3D, thematic columns, timed route, invented terrain | Explore scale, occlusion and time |
| [10 · GPT-6 Astra](book/notebooks/10_astra_geospatial_analyst.ipynb) | Evidence packet, structured request, image context and response checks | Reject unsupported citations |
| [11 · Spatial uncertainty](book/notebooks/11_spatial_uncertainty.ipynb) | Moran's I, seeded permutation test and aggregation | Explain scale and inference limits |
| [12 · Response capstone](book/notebooks/12_capstone_response.ipynb) | GeoJSON, CZML, scene, manifest and tabletop injects | Deliver a reviewable exercise handover |

Open any notebook in [JupyterLite](https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html), wait for **Python (Pyodide)**, then **Run → Run All Cells**. Keep the helper modules and `data/` / `viewers/` folders alongside the notebooks. Use the generated Download links to preserve browser work.

## What Astra adds

The documented `gpt-6-astra` model supports text/image input, reasoning, coding, tool calling, and structured output. This repository applies those capabilities to evidence synthesis, map interpretation, analytical critique, and briefing preparation. Numerical calculations remain explicit Python; visual reasoning is not a coordinate survey or a validated diagnostic method. [Official model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra), [image limitations](https://developers.openai.com/api/docs/guides/images-vision), [structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) (checked 2 October 2026).

Notebook 10 includes a clearly labeled illustrative fixture and a dry-run request. Optional live use runs through `tools/astra_brief.py` in a **local Python process** with `OPENAI_API_KEY` in its environment. It uses Responses, checks the aggregate input contract and cited source IDs, and handles incomplete/refused output. No key goes into JupyterLite or Pages. Live API calls incur usage and require model access; they are not part of CI. Schema validity does not establish factual validity.

![Evidence workflow from observation context to reviewed handover](book/assets/evidence-workflow.svg)

See [getting started](book/getting-started.md), [EOC playbook](book/eoc-playbook.md), [integration guide](book/integration.md), [glossary](book/glossary.md), and [data dictionary](book/notebooks/data/README.md).

## Citation, attribution and licenses

**Primary inspiration:** Bilawal Sidhu. *God's Eye View* (2026). [Source repository](https://github.com/bilawalsidhu/gods-eye-view). Integration inspected at [`e7707d9a0f34d9fbffc300023c319f95caa5be30`](https://github.com/bilawalsidhu/gods-eye-view/tree/e7707d9a0f34d9fbffc300023c319f95caa5be30).

Upstream source is **MIT**, copyright © 2026 Bilawal Sidhu. Its MIT grant excludes third-party data and assets. Consult the [upstream LICENSE](https://github.com/bilawalsidhu/gods-eye-view/blob/main/LICENSE), [DATA_SOURCES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/main/DATA_SOURCES.md), and [3D-model credits](https://github.com/bilawalsidhu/gods-eye-view/blob/main/public/models/README.md). No upstream models, imagery, bundled infrastructure data, or source implementation are copied here. Some upstream datasets have NonCommercial or ShareAlike conditions; those do not become MIT by appearing in an MIT application.

| Used here | Credit and terms |
|---|---|
| Original code, prose and synthetic fixtures | [MIT license](LICENSE), © 2026 James L. Tobias and contributors |
| Leaflet 1.9.4 | © Vladimir Agafonkin and contributors; [BSD-2-Clause](https://github.com/Leaflet/Leaflet/blob/v1.9.4/LICENSE), runtime CDN |
| CesiumJS 1.124.0 | Cesium contributors; [Apache-2.0](https://github.com/CesiumGS/cesium/blob/1.124/LICENSE.md), runtime CDN; provider credits stay visible |
| Esri World Imagery | Runtime imagery in 04, optional in 05; **Powered by Esri — Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community**. [Service details](https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer), [Esri terms](https://www.esri.com/en-us/legal/terms/full-master-agreement) |
| NASA Worldview / GIBS | Links and request construction in 08; [NASA GIBS](https://nasa-gibs.github.io/gibs-api-docs/access-basics/) and product-specific provenance apply. No NASA imagery is bundled |
| Jupyter Book / JupyterLite / Pyodide | Executable Book and Project Jupyter communities / Pyodide contributors; BSD-3-Clause / BSD-3-Clause / MPL-2.0; [notices](THIRD_PARTY_NOTICES.md) |
| NumPy / Matplotlib | Their contributors; BSD-3-Clause / Matplotlib's PSF-based license; [notices](THIRD_PARTY_NOTICES.md) |
| Splash artwork | AI-generated illustration using OpenAI's built-in image generation tool; synthetic visual, not sensor evidence. [Prompt and provenance](book/assets/README.md) |

The book cites [CDC field epidemiology](https://www.cdc.gov/field-epi-manual/php/chapters/index.html), [WHO AccessMod](https://www.who.int/tools/accessmod-geographic-access-to-health-care), [PySAL](https://pysal.org/esda/stable/user-guide/global_morans_i.html), and [GeoJSON RFC 7946](https://www.rfc-editor.org/rfc/rfc7946). See [full attributions](book/attribution.md) and [CITATION.cff](CITATION.cff). Akobo coordinates are an approximate pre-existing view center, not a survey. CSS “thermal”/“NVG” looks are display effects, not sensor bands. Tiles are fetched at runtime; they are not committed or redistributed as data, although browsers/providers may cache them normally.

This project is independent and is not affiliated with or endorsed by Bilawal Sidhu, OpenAI, NASA, CDC, WHO, Esri, Cesium, or other providers. It is for education and exercises, not validated clinical, navigation, dispatch, orbit-determination, or safety-of-life decisions.

## Build and verify

CI uses Python 3.12 and Node 24. [Validation results and browser-testing limits](VALIDATION.md) distinguish build/contract checks from live-service and browser testing.

```bash
python -m venv .venv
# Activate: source .venv/bin/activate
# PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build_demos.py
node --test tests/test_viewers.mjs
jupyter-book build book --warningiserror --keep-going
jupyter lite build --contents book/notebooks --output-dir book/_build/html/lite
python scripts/verify_site.py
python -m http.server 8000 --directory book/_build/html
```

Open `http://localhost:8000/`. Use HTTP, not `file://`. CI executes all notebooks and builds both sites; pushes to `main` deploy Pages. Enable **Settings → Pages → Source: GitHub Actions** if needed. Pull requests build and validate without deployment.

```text
book/notebooks/       12 labs, shared Python helpers, data/ and viewers/
book/assets/          Splash, analytical preview and evidence infographic
book/_static/demos/   Standalone viewers and example exports
integrations/        God's Eye View local-layer adapter
tools/astra_brief.py  Optional local-process API example (dry run by default)
scripts/             Reproducible fixture, notebook and demo generation
tests/               Numerical and request/response contract checks
```
