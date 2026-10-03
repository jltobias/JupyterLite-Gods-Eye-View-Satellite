# Riverbend data dictionary

All records are fictional. No patient, facility, surveillance, population or flood data were downloaded. Rectangles near the pre-existing Akobo view are not administrative boundaries. Snapshot: 2026-09-15 12:00 UTC. Period: 2026-09-01 through 2026-09-14 inclusive.

Recreate from the root with `python scripts/generate_data.py`. Deterministic arrays/formulas create 12 sectors, 3 clinics, a river axis and 168 daily aggregate rows.

| Field | Meaning / unit |
|---|---|
| GeoJSON geometry | WGS 84 longitude, latitude in degrees; Point, LineString, Polygon |
| `id` | S01–S12, C1–C3, R1 |
| `kind` | sector, clinic, river |
| `population` | Invented initially at-risk population, fixed over the period |
| `lon`, `lat` | Sector centroid, degrees; no patient/household locations |
| `flood_fraction` | Invented area fraction (0–1), not measured remotely |
| `capacity_day` | Invented visits/day, not beds |
| `available` | Fictional service status; C3 is closed |
| `synthetic` | Always true |
| `as_of` | Snapshot, UTC |
| CSV `sector_id` | Join to sector ID |
| `onset_date` | Exercise onset day, ISO date |
| `cases` | Nonnegative integer reported first episodes |
| `status` | complete for days 1–11; incomplete for days 12–14 |
| derived `rate_10000` | 14-day sum / population × 10,000 |

An invented epidemic shape is scaled by population and fixed multipliers. Final three days are thinned to 75%, 50%, 25%, then rounded. These are simulation inputs, not estimated completeness. Counts assume unique first episodes in a closed population. Spatial overlap with flood fractions establishes no cause.

`styled_sectors()` joins the CSV to GeoJSON and adds counts/rates for export. Missing/nonpositive denominators yield NaN, not zero risk; non-finite JSON metrics are rejected. Range checks cannot catch every in-range coordinate swap.

Synthetic fixtures use the repository MIT license. External providers and libraries retain their own terms.
