# Attribution, sources and licensing

## Primary inspiration

Bilawal Sidhu. **God's Eye View** (2026). [Repository](https://github.com/bilawalsidhu/gods-eye-view). Integration inspected at [`e7707d9a0f34d9fbffc300023c319f95caa5be30`](https://github.com/bilawalsidhu/gods-eye-view/tree/e7707d9a0f34d9fbffc300023c319f95caa5be30) on 2 October 2026.

Upstream source is MIT, copyright © 2026 Bilawal Sidhu. The [license](https://github.com/bilawalsidhu/gods-eye-view/blob/main/LICENSE) expressly excludes third-party data and assets. Consult [DATA_SOURCES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/main/DATA_SOURCES.md) and [model credits](https://github.com/bilawalsidhu/gods-eye-view/blob/main/public/models/README.md). The TeleGeography cable dataset is flagged upstream as CC BY-NC-SA 3.0; Bhote Koshi event imagery/derived coordinates as CC BY-NC 4.0; OSM-derived datasets as ODbL. These assets are not included here.

Original code, prose, diagrams and synthetic fixtures are released under this repository's [MIT license](https://github.com/jltobias/JupyterLite-Gods-Eye-View-Satellite/blob/main/LICENSE). No upstream implementation, models or bundled datasets are copied. The extension is original code calling Cesium's API in an inspected upstream scene lifecycle.

## Actual runtime providers and libraries

| Resource | Use and attribution | License / terms |
|---|---|---|
| Esri World Imagery | Notebook 04, optional 05 basemap. **Powered by Esri — Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community** | [Service metadata](https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer); Esri/provider terms |
| Leaflet 1.9.4 | Original 2D viewers, loaded from unpkg | [BSD-2-Clause](https://github.com/Leaflet/Leaflet/blob/v1.9.4/LICENSE) |
| CesiumJS 1.124.0 | Original 3D teaching scene, loaded from jsDelivr | [Apache-2.0](https://github.com/CesiumGS/cesium/blob/1.124/LICENSE.md) |
| NASA GIBS / Worldview | Dated links and browse-image request in 08 | [GIBS guide](https://nasa-gibs.github.io/gibs-api-docs/access-basics/); cite selected product and acquisition metadata |
| Jupyter Book / JupyterLite | Build and browser runtime | BSD-3-Clause; see repository notices |
| Pyodide | WebAssembly Python kernel | MPL-2.0 and component licenses |
| NumPy / Matplotlib | Numerical work and analytical figures | BSD-3-Clause / Matplotlib's PSF-based license |
| OpenAI API | Optional local `gpt-6-astra` example | Service terms, account access and usage charges apply |

Imagery is requested at runtime; no Esri/NASA tiles are committed as data. Normal browser/provider caches may retain fetched responses. Keep on-map provider credits visible. Request time is not acquisition time, and display filters are not spectral measurements.

The approximate Akobo center (7.79293° N, 33.00294° E) is inherited from the original notebook's OpenStreetMap/GeoNames-derived place reference. It is only a map center, not a surveyed location. No OSM tiles, population surfaces, real facility records, or case line lists are included in the new exercise.

## Teaching sources

- [CDC Field Epidemiology Manual](https://www.cdc.gov/field-epi-manual/php/chapters/index.html): definitions, descriptive analysis, outbreak investigation context. No surveillance dataset is copied.
- [WHO AccessMod](https://www.who.int/tools/accessmod-geographic-access-to-health-care): geographic accessibility context. The simple distance lab is not an implementation of AccessMod.
- [PySAL global Moran's I](https://pysal.org/esda/stable/user-guide/global_morans_i.html): statistic and weights reference. The lab uses original NumPy code.
- [RFC 7946](https://www.rfc-editor.org/rfc/rfc7946): GeoJSON coordinates and interchange.
- [Cesium API](https://cesium.com/learn/cesiumjs/ref-doc/): scene and time-dynamic rendering.
- [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [vision limitations](https://developers.openai.com/api/docs/guides/images-vision): applied model workflows, verified 2 October 2026.

## Artwork and generated products

The README/book splash is an AI-generated illustration made with OpenAI's built-in image generation tool. It is not remotely sensed imagery or scientific evidence. The prompt, date and provenance are recorded in [`book/assets/README.md`](https://github.com/jltobias/JupyterLite-Gods-Eye-View-Satellite/blob/main/book/assets/README.md). Analytical figures are computed from the original synthetic fixtures; the workflow SVG is an original diagram. No third-party logos are used.

See [THIRD_PARTY_NOTICES.md](https://github.com/jltobias/JupyterLite-Gods-Eye-View-Satellite/blob/main/THIRD_PARTY_NOTICES.md) and [CITATION.cff](https://github.com/jltobias/JupyterLite-Gods-Eye-View-Satellite/blob/main/CITATION.cff). This independent project is not endorsed by its inspiration, cited institutions, or service providers.
