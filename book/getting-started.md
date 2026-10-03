# Getting started

## Run a lab

1. Open [JupyterLite Lab](https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html) and a numbered notebook.
2. Wait for **Python (Pyodide)**, then select **Run → Run All Cells**. Start with 05 for the response exercise or 01 for satellite foundations.
3. Change named parameters and rerun dependent cells. Each notebook runs independently.
4. Use the generated **Download** links to retain GeoJSON, HTML, JSON and CZML products. Browser storage is local to the browser/origin.

Keep `gev_lab.py`, `astra_contract.py`, `data/`, and `viewers/` beside the notebooks. The published JupyterLite site ships this whole folder; a single downloaded notebook is insufficient for the expanded labs.

## Network and runtime requirements

| Component | Needs | Fallback |
|---|---|---|
| Python calculations | Initial runtime/package download; no key | Executed book charts |
| Leaflet map | Pinned CDN library | Static choropleths |
| Optional Esri imagery | Tile service and provider terms | Synthetic layers with imagery off |
| Cesium scene | Pinned CDN library and WebGL | Notebook 09 static 3D figure |
| NASA Worldview / GIBS | Service and archive availability | Synthetic raster exercise |
| Astra live run | Local Python, OpenAI key, model access, usage | Dry run and illustrative fixture |
| Full God's Eye View | Separate upstream local application | Teaching viewers here |

This is not an air-gapped distribution. Browser caches do not guarantee offline startup or library availability. Deterministic analysis cells do not fetch live data.

## Troubleshooting

- **Old files after publication:** JupyterLite can retain edited browser copies. Export your work, then rename/remove the old copy or use a fresh browser profile. Never clear storage before saving valuable work.
- **Missing helper:** check the helper modules and folders are beside the notebook; restart the kernel.
- **Blank iframe:** rerun the cell; trust the notebook only when you trust its source. Check unpkg/jsDelivr access or try the standalone demo.
- **No 3D:** use supported WebGL/hardware acceleration or the static figure. Analysis does not depend on WebGL.
- **Old imagery:** download time is not acquisition time. Consult product metadata.

## Local build

Create and activate a virtual environment, then run from the root:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build_demos.py
jupyter-book build book --warningiserror --keep-going
jupyter lite build --contents book/notebooks --output-dir book/_build/html/lite
python -m http.server 8000 --directory book/_build/html
```

Visit `http://localhost:8000/` and `/lite/lab/index.html`. Use HTTP, not `file://`. CI uses Python 3.12; the book executes clean source notebooks during the build.

`scripts/generate_data.py` recreates the deterministic fixtures. `scripts/author_notebooks.py` regenerates the eight authored labs and idempotently extends the original four. Revise that authoring source when changing generated lab content and review the resulting notebook diff.

References: [JupyterLite content](https://jupyterlite.readthedocs.io/en/stable/howto/content/files.html), [Jupyter Book](https://jupyterbook.org/en/stable/), [Pyodide](https://pyodide.org/en/stable/).
