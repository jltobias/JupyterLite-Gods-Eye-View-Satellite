# Glossary

| Term | Meaning in these labs |
|---|---|
| Acquisition time | When a sensor observed a location; different from download time. |
| AOI | Area of interest: the selected geographic extent. |
| Ascertainment | How actual events become recognized and reported cases. |
| Basemap | Geographic context beneath analysis; not verification of an event. |
| Bounding box | West, south, east, north extent in the lab's longitude/latitude convention. |
| Case definition | Explicit event, person, place and time criteria for counting a case. |
| CesiumJS | JavaScript library for globes and geospatial scenes. |
| Choropleth | Map shading areas by a variable; population comparisons need appropriate denominators. |
| Closed cohort | Fixed population without entries/exits in the simplified analysis. |
| Common operating picture | Shared, time-stamped evidence, status and uncertainty view. |
| Confidence interval | Uncertainty procedure under stated assumptions; not all errors. |
| CRS | Coordinate reference system: how coordinates relate to Earth. |
| Cumulative incidence | New cases / initially at-risk population over a defined period. Reported first episodes here are an incomplete proxy. |
| CZML | Cesium JSON format for time-dynamic entities. |
| Data provenance | Origins, processing, times, assumptions and rights. |
| Denominator | Population or person-time used to normalize a count. |
| Ecological fallacy | Inferring individual relationships from group-level patterns. |
| Ellipsoid | Smooth approximation of Earth without local terrain relief. |
| EOC | Emergency Operations Center: response coordination function and setting. |
| Epidemic curve | Incident case counts in successive time bins, commonly onset date. |
| EPSG:4326 | WGS 84 geographic CRS; axis order depends on protocol. GeoJSON is longitude first. |
| Exposure | Contact with a possible determinant; overlay overlap is not proof of individual exposure. |
| GeoJSON | Geographic features; positions use longitude, latitude in degrees. |
| GIBS | NASA Global Imagery Browse Services. |
| Ground track | Spacecraft subpoint path on rotating Earth. |
| Haversine | Great-circle distance formula on a sphere, not a road distance. |
| Incidence rate | New cases divided by person-time; distinct from cumulative incidence. |
| Inclination | Orbital-plane tilt relative to the reference plane. |
| Isochrone | Equal travel-time boundary under a travel model; not a distance ring. |
| Jupyter Book | Published narrative and executed notebook outputs. |
| JupyterLite | Browser-hosted Jupyter; Python here uses Pyodide/WebAssembly. |
| Line list | One record per person/event; no real line list is included. |
| MAUP | Modifiable areal unit problem: results change with aggregation boundaries/scale. |
| Moran's I | Spatial-autocorrelation statistic relative to specified neighbor weights. |
| NDWI | Normalized difference water index; here green/NIR, not other similarly named formulations. |
| Near real time | Available after a processing delay; not instantaneous or complete. |
| Nowcast | Estimate of incompletely observed current events; sensitivity arithmetic here is not a fitted nowcast. |
| OGC:CRS84 | WGS 84 longitude/latitude convention used in the evidence packet. |
| Onset date | When illness/event began, not when reported. |
| Permutation test | Comparison to rearranged labels under a specified null assumption. |
| Photorealistic 3D tiles | Provider's textured geometry; distinct from thematic extrusions. |
| Prevalence | Existing cases in a population at a point or period, not new incidence. |
| Pyodide | Python compiled for WebAssembly with compatible packages. |
| RAAN | Right ascension of the ascending node: orientation of an orbital plane. |
| Raster | Grid of cells whose size, projection, bands and quality matter. |
| Reporting delay | Time from event/onset to reporting-system arrival. |
| Rook adjacency | Neighbors share an edge; queen adjacency also includes corners. |
| SGP4 | Orbital propagator commonly paired with TLEs; not the simplified model here. |
| Spatial autocorrelation | Nearby values tend to be more similar/dissimilar than expected. |
| Structured output | Schema-constrained model response; structure is not factual validity. |
| Synthetic data | Invented exercise inputs, not real observations. |
| TLE | Two-line orbital element set for compatible propagation. |
| Uncertainty | Limits from variation, missingness, bias, measurement and assumptions. |
| Vector | Points, lines or polygons representing features. |
| Viewshed | Visible region given viewpoint, geometry and obstruction assumptions. |
| WGS 84 | Global geodetic reference system used for coordinates here. |
| Wilson interval | Binomial proportion interval, excluding reporting/denominator bias. |
| WMS / WMTS | Web Map Service / Web Map Tile Service imagery protocols. |
| Worldview | NASA's imagery browser, separate from God's Eye View. |
| Z-score | Value centered on a mean and divided by standard deviation. |

References: [RFC 7946](https://www.rfc-editor.org/rfc/rfc7946), [CDC manual](https://www.cdc.gov/field-epi-manual/php/chapters/index.html), [GIBS](https://nasa-gibs.github.io/gibs-api-docs/access-basics/), [Cesium](https://cesium.com/learn/cesiumjs/ref-doc/).
