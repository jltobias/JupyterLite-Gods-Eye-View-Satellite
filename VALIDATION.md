# Validation record

Checked 2 October 2026 in a local Windows checkout using Python 3.13 and Node 24.14.0. CI repeats the checks on Ubuntu with Python 3.12 and Node 24.

| Check | Result |
|---|---|
| Seven Python tests | Passed: distances, denominators/intervals, exact small-grid Moran expectation, fixture integrity, model contracts, refusals/incomplete responses, script-embedding escape |
| Four Node tests | Passed: both demo scripts compile; adapter accepts exports, strips untrusted presentation fields, rejects invalid/non-synthetic/oversized input |
| All 12 notebooks | Executed in fresh local Python kernels during book build |
| Jupyter Book | Built with `--warningiserror --keep-going` |
| JupyterLite | Built with 12 notebooks and seven helper/data/viewer files |
| Deployment artifact | Chapters, packaged notebook equality, helpers, demos and local links checked |
| Astra CLI | Dry run generated without network; failure paths tested with fixtures |
| Leaflet integrity | Pinned CDN assets fetched; SHA-256 hashes match HTML attributes |
| Figures | Splash and analytical preview inspected; high-value sector labels use contrasting text |

Limits: no browser UI surface was available, so interactive WebGL/iframe behavior and the actual Pyodide kernel were not exercised through a browser. Node checks are not a browser smoke test. No live OpenAI call was made. The upstream installation point was inspected at the documented revision; the complete upstream app and live feeds were not run.

Before an instructional session, open the deployed site in the target browser, run notebooks 05 and 10 in JupyterLite, switch 2D/3D and scrub the route in 09, and confirm downloads and provider credits. Use static figures when institutional CDN/WebGL restrictions prevent interactive rendering.
