# Attribution and data-source notes

## Primary inspiration

This project cites and is inspired by:

> Bilawal Sidhu. **God's Eye View** (2026). GitHub repository: https://github.com/bilawalsidhu/gods-eye-view

The upstream source code is released under the MIT License, copyright © 2026 Bilawal Sidhu. Its MIT grant applies to source code, **not** to third-party data or visual assets. See:

- Upstream license: https://github.com/bilawalsidhu/gods-eye-view/blob/main/LICENSE
- Upstream data/source attribution: https://github.com/bilawalsidhu/gods-eye-view/blob/main/DATA_SOURCES.md
- Upstream bundled 3D-model attribution: https://github.com/bilawalsidhu/gods-eye-view/blob/main/public/models/README.md

This repository is not affiliated with or endorsed by Bilawal Sidhu or the upstream data providers.

## Upstream sources relevant to these examples

God's Eye View documents a much larger source catalog. Sources especially relevant to its satellite/globe context include:

| Upstream source | Upstream use | Attribution / terms summary |
|---|---|---|
| [CelesTrak](https://celestrak.org/) | Satellite TLEs used with SGP4 | Upstream credits “CelesTrak (celestrak.org), Dr. T.S. Kelso”; consult CelesTrak terms/citation guidance. |
| [Esri World Imagery](https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9) | Keyless satellite imagery basemap | Provider attribution and Esri terms apply. |
| [Re:Earth / Mapterhorn terrain](https://github.com/reearth/reearth-visualizer) | Keyless terrain stack | Upstream identifies terrain mesh as CC BY 4.0 and EGM2008 geoid material as U.S. public-domain-origin. |
| [OpenStreetMap](https://www.openstreetmap.org/copyright) | Roads and mapped context | ODbL 1.0; © OpenStreetMap contributors. |
| [USGS](https://www.usgs.gov/) | Earthquakes | U.S. public-domain data; upstream requests courtesy attribution. |
| [OpenSky Network](https://opensky-network.org/) | Live aircraft | Upstream documents non-commercial research/education restrictions; consult OpenSky before deployment. |
| [adsb.lol](https://adsb.lol/) | Flight fallback / military traffic | Upstream documents ODbL 1.0. |
| [AISStream.io](https://aisstream.io/) | Live vessels | Upstream documents it as a public-broadcast/beta service and gives courtesy attribution. |
| [The Space Devs — Launch Library 2](https://thespacedevs.com/llapi) | Launch and payload context | Use subject to The Space Devs terms and API limits. |
| [Open-Meteo](https://open-meteo.com/en/licence) | Weather | CC BY 4.0 with linked attribution requirements. |
| [GDELT Project](https://www.gdeltproject.org/) | Regional-news fallback | Upstream documents citation/link requirements. |
| [TeleGeography Submarine Cable Map](https://www.submarinecablemap.com/) | Bundled submarine-cable layer | Upstream explicitly flags CC BY-NC-SA 3.0 / NonCommercial and says commercial users must remove or separately license it. |

The complete and controlling list is the upstream project's [`DATA_SOURCES.md`](https://github.com/bilawalsidhu/gods-eye-view/blob/main/DATA_SOURCES.md), not this summary.

## What these notebooks actually use

The notebooks in this repository currently use only NumPy/Matplotlib plus synthetic orbital parameters and standard orbital/spherical geometry constants. They do **not** download, bundle, cache, or redistribute CelesTrak TLEs, imagery, aircraft feeds, vessel feeds, camera images, or upstream bundled datasets. This choice keeps the JupyterLite demonstrations deterministic and avoids silently transferring third-party usage rights.
