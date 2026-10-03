# EOC and global-health exercise playbook

## Scenario and roles

Riverbend is fictional, located near the Akobo map for teaching continuity. An exercise cell receives invented flood exposure, aggregate illness reports and clinic status. Explain what is known, how it was computed, what remains uncertain, and which evidence to verify next.

| Role | Product | Review question |
|---|---|---|
| GIS analyst | Layers, manifest, 2D/3D views | Are CRS, extent, units, dates and legends correct? |
| Epidemiology analyst | Curve, counts, rates, intervals | Do definitions and denominators match the window? |
| Logistics analyst | Access and capacity scenarios | Are closure and network assumptions visible? |
| Exercise lead | Briefing and decision log | Does evidence support each statement? Who verifies it? |

This is a training workflow, not a deployed multi-user EOC. Real deployment needs authenticated access, data stewardship, tested feeds, versioned snapshots, operating procedures and accountable incident leadership. Static Pages does not provide those services.

## A 90-minute tabletop

| Time | Activity | Retain |
|---|---|---|
| 0–15 min | Data dictionary and lab 05 | Source IDs, assumptions, snapshot |
| 15–35 min | Counts, denominators and delay in 06 | Annotated curve and map |
| 35–50 min | Close C3 in 07; inspect capacity | Access and speed assumptions |
| 50–65 min | Rotate and flatten 3D in 09 | Comparable 2D/3D views |
| 65–80 min | Packet in 10; critique response | Claim-by-claim review |
| 80–90 min | Capstone 12 | GeoJSON, manifest, briefing, unknowns |

## An honest situation report

Lead with observation period and snapshot cutoff. Give counts their definition and rates their denominator and time window. Identify incomplete onset days. Flood fractions are exercise inputs; spatial overlap suggests a hypothesis, not an established cause.

Separate observations from proposed actions. Assign verification steps an owner and due time within the exercise. Preserve previous snapshots so late reports are not mistaken for new onset. Pair interactive views with a static map and data table.

## Global-health transfer

Before applying these methods to authorized surveillance aggregates, adapt case definitions, geographies, population estimates, reporting completeness, seasonality, language and local access modes. Boundaries and names can be contested or stale; engage responsible local data and public-health teams.

Do not publish identifiable line lists or household locations in a static site. Small-cell suppression alone can permit reconstruction through overlapping maps and totals. Select disclosure controls with the data steward. These labs use fabricated aggregates.

Future connections could include authorized surveillance, population surfaces, facility registries, precipitation, flood products and road/boat networks. Each needs a date, coverage, quality, permission and license record. No real feed is silently substituted for synthetic inputs.

References: [CDC field investigation](https://www.cdc.gov/field-epi-manual/php/chapters/field-investigation.html), [CDC descriptive epidemiology](https://www.cdc.gov/field-epi-manual/php/chapters/describing-epi-data.html), [WHO AccessMod](https://www.who.int/tools/accessmod-geographic-access-to-health-care). No endorsement is implied.
