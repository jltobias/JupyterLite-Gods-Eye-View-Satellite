# JupyterLite God's Eye View — Satellite Examples

This Jupyter Book contains small, browser-executable Python examples inspired by the satellite/orbital capabilities of [Bilawal Sidhu's **God's Eye View**](https://github.com/bilawalsidhu/gods-eye-view).

The upstream application is a full 3D situational-awareness web application built with Cesium and `satellite.js`; its satellite layer uses CelesTrak orbital elements and SGP4 propagation. The first three notebooks here are **original educational Python examples** using synthetic inputs and simplified spherical/two-body geometry. The fourth notebook adds a browser-native satellite imagery view of Akobo, South Sudan using Esri World Imagery fetched at runtime, with an original Leaflet/HUD presentation designed to run in JupyterLite without a notebook server or API key.

## Run in your browser

- [Open JupyterLite](https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html)
- [Orbital ground track](https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html?path=01_orbit_ground_track.ipynb)
- [Sensor footprint](https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html?path=02_sensor_footprint.ipynb)
- [Constellation dashboard](https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html?path=03_constellation_dashboard.ipynb)
- [Akobo satellite imagery HUD](https://jltobias.github.io/JupyterLite-Gods-Eye-View-Satellite/lite/lab/index.html?path=04_akobo_satellite_imagery.ipynb)

```{note}
This repository does not mirror the upstream application's live feeds or bundled third-party datasets. The Akobo notebook requests Esri World Imagery directly from Esri at runtime and keeps the provider attribution visible. Provider terms can change; consult the upstream `DATA_SOURCES.md` and each provider before using real data.
```
