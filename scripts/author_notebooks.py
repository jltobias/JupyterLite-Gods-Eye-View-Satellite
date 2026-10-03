"""Author original lab notebooks and idempotently extend the four starter labs."""
from pathlib import Path
from textwrap import dedent
import hashlib
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1] / 'book/notebooks'


def md(s):
    return nbf.v4.new_markdown_cell(dedent(s).strip())


def code(s):
    return nbf.v4.new_code_cell(dedent(s).strip())


IMPORTS = '''
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
from gev_lab import *
plt.rcParams.update({'figure.dpi': 110, 'axes.spines.top': False, 'axes.spines.right': False})
scenario = styled_sectors()
stats = sector_summary()
print('SYNTHETIC TRAINING EXERCISE | snapshot', AS_OF)
'''


def notebook(name, cells):
    n = nbf.v4.new_notebook(cells=cells, metadata={
        'kernelspec': {'display_name': 'Python (Pyodide)', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python'},
    })
    for i, c in enumerate(n.cells):
        c.id = hashlib.sha256((name + str(i) + c.source).encode()).hexdigest()[:12]
    nbf.write(n, ROOT / name)


def lab(title, intro):
    return [md(f'# {title}\n\n{intro}\n\n**Runtime:** Python + NumPy + Matplotlib; no model key. Run all cells in order. Interactive viewers additionally load JavaScript from a CDN. All scenario records are fictional.'), code(IMPORTS)]


cells = lab('05 · Build a browser EOC common operating picture', '''
**Mission (30 minutes):** brief an exercise team on a fictional river flood and reported illness.
Learn to distinguish count, denominator, exposure assumption, and data freshness. Deliver a 2D layer package and a one-minute situation report.

Riverbend is a fictional exercise located near the Akobo map for continuity. Its rectangles, clinics, population, flood fractions, and cases are invented. They describe no real community or event.
''')
cells += [md('''
## 1. Same places, different questions
Counts indicate reported workload; cumulative reported first episodes per 10,000 describe a population-normalized measure over 1–14 September. Neither is a prevalence estimate. Exposure below is **population × invented flooded fraction**, assuming uniform population within each sector.
'''), code('''
population = np.array([r['population'] for r in stats])
counts = np.array([r['cases'] for r in stats])
rates = rate_per_10000(counts, population)
flood = np.array([r['flood_fraction'] for r in stats])
fig, axes = plt.subplots(1, 3, figsize=(15, 4), constrained_layout=True)
for ax, values, title, units in zip(axes, [counts, rates, flood],
        ['Reported workload', 'Population-normalized reports', 'Invented flood exposure'],
        ['reported cases / 14 days', 'cases / 10,000 / 14 days', 'fraction of sector (0–1)']):
    p = plot_sectors(ax, values, title)
    fig.colorbar(p, ax=ax, shrink=.7, label=units)
plt.show()
print('Reported cases:', counts.sum())
print('Population-weighted aggregate measure:', round(float(rate_per_10000(counts.sum(), population.sum())), 1), 'per 10,000')
print('Illustrative exposed population:', round(float((population*flood).sum())))
'''), md('''
## 2. Explore and inspect
Change the shading, click a sector, toggle clinics, and optionally request imagery. The initial map is synthetic; no tile service is needed until selected. Esri imagery is a basemap mosaic with varying acquisition dates, not a live flood observation.
'''), code('show_map(scenario)'), md('''
## 3. Make freshness visible
The fictional snapshot clock is fixed so the lab is reproducible. A stale record is flagged rather than silently displayed as current. A threshold is an exercise policy, not a universal standard.
'''), code('''
from datetime import datetime, timezone
now = datetime.fromisoformat(AS_OF.replace('Z', '+00:00'))
feeds = [('clinic status', '2026-09-15T10:00:00+00:00'),
         ('invented flood layer', '2026-09-14T04:00:00+00:00'),
         ('case aggregates', '2026-09-15T08:00:00+00:00')]
for name, stamp in feeds:
    age = (now - datetime.fromisoformat(stamp)).total_seconds()/3600
    print(f'{name:22s} {age:5.1f} hours old | {"REVIEW" if age > 24 else "within exercise threshold"}')
download('riverbend-analysis.geojson', scenario, 'application/geo+json')
download('riverbend-eoc.html', map_page(scenario), 'text/html')
'''), md('''
## Lab challenge and debrief
1. Halve the flood fractions. Which headline changes, and which should remain unchanged?
2. Find the sector with the highest count and the highest rate. Explain the denominator effect.
3. Write a briefing that separates observation, assumption, uncertainty, and a request for verification.

**Check:** halving fractions halves the exposure estimate, but does not change reported cases. A high rate alone does not establish where infection occurred or where a response team should go.

**God's Eye View handoff:** use notebook 12 and the book's integration chapter to bring the exported GeoJSON into a local upstream checkout. This viewer is an original teaching companion, not the full upstream application.

**Sources:** [CDC descriptive epidemiology](https://www.cdc.gov/field-epi-manual/php/chapters/describing-epi-data.html), [God's Eye View](https://github.com/bilawalsidhu/gods-eye-view), [Leaflet](https://leafletjs.com/).
''')]
notebook('05_eoc_common_operating_picture.ipynb', cells)

cells = lab('06 · Spatial epidemiology: time, place, denominator', '''
**Mission (40 minutes):** turn aggregate first-episode reports into an epidemic curve, a choropleth, and an uncertainty-aware comparison. The illustrative case definition is one newly reported first episode of the exercise syndrome per resident during the 14-day window. It is not a diagnostic definition.
''')
cells += [md('''
## 1. Plot by onset date, and mark incomplete days
These are aggregated reported cases by onset date. No individual line list or patient coordinates are used. The right edge has deliberately incomplete reporting; a drop there cannot be read as control of an outbreak.
'''), code('''
rows = load_cases()
dates = sorted({r['onset_date'] for r in rows})
daily = np.array([sum(r['cases'] for r in rows if r['onset_date']==d) for d in dates])
fig, ax = plt.subplots(figsize=(11,4), constrained_layout=True)
ax.bar(np.arange(14), daily, width=1, color=['#20a89d']*11+['#e3b258']*3, edgecolor='white')
ax.axvspan(10.5,13.5,color='#e3b258',alpha=.14,label='Incomplete reporting')
ax.set_xticks(range(0,14,2), [d[5:] for d in dates[::2]])
ax.set(xlabel='Onset date (2026)',ylabel='Reported first episodes',title='Synthetic epidemic curve · fixed 15 Sep snapshot')
ax.legend(); plt.show()
assert daily.sum() == sum(s['cases'] for s in stats)
'''), md('''
## 2. Rates and intervals
For this closed fictional population, reported cumulative incidence per 10,000 is `cases / population × 10,000`. A Wilson binomial interval illustrates sampling uncertainty under an independent first-episode assumption. It **does not account for reporting delay, under-ascertainment, migration, spatial dependence, or a wrong denominator**.
'''), code('''
k = np.array([s['cases'] for s in stats]); n = np.array([s['population'] for s in stats])
r = rate_per_10000(k,n); low, high = wilson_interval(k,n)
order = np.argsort(r)
fig, axes = plt.subplots(1,2,figsize=(12,5),constrained_layout=True)
p = plot_sectors(axes[0],r,'Synthetic reported cumulative incidence')
fig.colorbar(p,ax=axes[0],shrink=.7,label='Reported first episodes / 10,000 / 14 days')
axes[1].errorbar(r[order],np.arange(12),xerr=[r[order]-low[order]*10000,high[order]*10000-r[order]],fmt='o',color='#158b85')
axes[1].set_yticks(range(12),[stats[i]['id'] for i in order])
axes[1].set(xlabel='Reported cases / 10,000 (95% Wilson interval)',ylabel='Training sector',title='Intervals omit systematic errors')
plt.show()
print('Missing population yields:', float(rate_per_10000(10,0)), '(not zero risk)')
'''), md('''
## 3. Sensitivity to ascertainment
Hypothetical reporting probabilities are scenario assumptions, not estimates. Dividing by them is an arithmetic sensitivity exercise, not a validated nowcast.
'''), code('''
for reporting in [.4,.7,1.0]:
    adjusted = k.sum()/reporting
    print(f'If reporting probability = {reporting:.0%}: implied episodes ≈ {adjusted:,.0f}')
'''), md('''
## Lab challenge and checks
1. Double S07's population without changing its reports. Its rate should halve.
2. Compare count and rate rankings. Which would you show for staffing workload versus population comparison?
3. Explain why a cluster around the invented river is not proof of waterborne transmission.

**Check:** an onset curve and a report-date curve answer different questions. Population denominators and case definitions must match in space, time, and eligibility. An ecological association cannot identify an individual's exposure or establish a cause.

**Sources:** [CDC: Describing Epidemiologic Data](https://www.cdc.gov/field-epi-manual/php/chapters/describing-epi-data.html), [CDC: Analyzing and Interpreting Data](https://www.cdc.gov/field-epi-manual/php/chapters/analyze-interpret-data.html). Synthetic data generation: `scripts/generate_data.py`; no real surveillance data are redistributed.
''')]
notebook('06_spatial_epidemiology.ipynb', cells)

cells = lab('07 · Health access under disruption', '''
**Mission (35 minutes):** compare nearest-clinic distance before and after a closure, then test travel-speed assumptions. Deliver a service-access gap map. All clinics and capacities are fictional; great-circle travel times are lower-bound illustrations, not routes or dispatch advice.
''')
cells += [code('''
clinics = [f for f in scenario['features'] if f['properties']['kind']=='clinic']
xy = np.array([[s['lon'],s['lat']] for s in stats])
cxy = np.array([c['geometry']['coordinates'] for c in clinics])
dist = haversine_km(xy[:,0,None],xy[:,1,None],cxy[None,:,0],cxy[None,:,1])
open_mask = np.array([c['properties']['available'] for c in clinics])
baseline = dist.min(axis=1)
disrupted = np.where(open_mask[None,:],dist,np.inf).min(axis=1)
assert np.all(disrupted >= baseline)
fig, axes = plt.subplots(1,2,figsize=(12,4),constrained_layout=True)
for ax, values, title in zip(axes,[baseline,disrupted-baseline],['All clinics available','Added distance after C3 closure']):
    p=plot_sectors(ax,values,title,cmap='YlGnBu');fig.colorbar(p,ax=ax,shrink=.75,label='Great-circle km')
plt.show()
'''), md('''
## Travel-time assumptions change the story
Use two invented effective speeds. These omit roads, river crossings, terrain, security, queues, and referral capability. A 60-minute threshold is chosen for the exercise, not a clinical standard. A centroid is not the location of every resident.
'''), code('''
pop=np.array([s['population'] for s in stats])
speeds=np.array([5,15,30,45])
share=np.array([pop[disrupted/speed*60 > 60].sum()/pop.sum()*100 for speed in speeds])
fig,ax=plt.subplots(figsize=(8,4),constrained_layout=True)
ax.plot(speeds,share,'o-',color='#128d87');ax.set(xlabel='Assumed effective speed (km/h)',ylabel='Population beyond 60 min (%)',ylim=(0,100),title='Synthetic access sensitivity · straight-line approximation');ax.grid(alpha=.2);plt.show()
assignment=np.where(open_mask[None,:],dist,np.inf).argmin(axis=1)
for j,c in enumerate(clinics):
    print(c['id'],'assigned population',pop[assignment==j].sum(),'available',open_mask[j])
'''), md('''
## Capacity is a separate constraint
Nearest-facility assignment can overwhelm the closest clinic. This one-day demand fraction is an invented workload scenario, unrelated to the cumulative case count.
'''), code('''
demand_fraction=.02
for j,c in enumerate(clinics):
    demand=pop[assignment==j].sum()*demand_fraction
    capacity=c['properties']['capacity_day'] if open_mask[j] else 0
    print(f"{c['id']}: scenario visits/day {demand:.0f}; capacity {capacity}; unmet {max(0,demand-capacity):.0f}")
'''), md('''
## Lab challenge
Restore C3 and compare accessibility and capacity. Then close all clinics: represent lack of service as infinity/missing, not zero distance, and avoid assigning people to a closed clinic. Discuss the extra evidence needed for a road/boat network model.

**Check:** closing a clinic cannot reduce nearest-open-clinic distance. Population, demand, capacity, and physical access are different quantities. A distance map cannot establish safe access or service quality.

**Sources:** [WHO AccessMod](https://www.who.int/tools/accessmod-geographic-access-to-health-care) for a real accessibility modeling framework; [GeoJSON coordinate convention, RFC 7946](https://www.rfc-editor.org/rfc/rfc7946). This lab does not implement AccessMod or use its datasets.
''')]
notebook('07_health_access_logistics.ipynb', cells)

cells = lab('08 · NASA Worldview, imagery provenance, and change', '''
**Mission (35 minutes):** connect a dated NASA Worldview view to an auditable imagery comparison. NASA **Worldview** is a separate NASA application; **God's Eye View** is Bilawal Sidhu's situational-awareness globe. Use the former to inspect dated Earth-observation context and the latter to combine scene layers.
''')
cells += [md('''
## 1. Construct a dated view, not a claim of an event
The example date is a reproducible archive request, unrelated to the fictional September 2026 exercise. The link opens a real service; network access and product availability are required. Cloud and missing coverage remain possible.
'''), code('''
from urllib.parse import urlencode
imagery_date='2024-09-01'
bbox=[32.4,7.2,33.7,8.4]  # west, south, east, north
worldview='https://worldview.earthdata.nasa.gov/?'+urlencode({'v':','.join(map(str,bbox)),'t':imagery_date,'l':'MODIS_Terra_CorrectedReflectance_TrueColor'})
display(Markdown(f'[Open dated NASA Worldview view]({worldview})'))
# WMS 1.1.1 with EPSG:4326 uses longitude,latitude bounding-box order.
gibs='https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?'+urlencode({
    'SERVICE':'WMS','REQUEST':'GetMap','VERSION':'1.1.1','LAYERS':'MODIS_Terra_CorrectedReflectance_TrueColor',
    'STYLES':'','FORMAT':'image/png','SRS':'EPSG:4326','BBOX':','.join(map(str,bbox)),
    'WIDTH':1000,'HEIGHT':800,'TIME':imagery_date})
display(Markdown(f'[Request NASA GIBS browse image]({gibs})'))
manifest={'provider':'NASA EOSDIS GIBS','product':'MODIS_Terra_CorrectedReflectance_TrueColor',
          'requested_date':imagery_date,'bbox_crs84':bbox,'request_url':gibs,
          'acquisition_time':'VERIFY IN PRODUCT METADATA','cloud_quality':'NOT ASSESSED',
          'interpretation':'browse visualization; not a calibrated reflectance raster'}
download('imagery-manifest.json',manifest)
'''), md('''
## 2. Learn change detection on explicit synthetic spectral arrays
RGB screenshots are not calibrated spectral bands. Here we construct invented green/NIR reflectance arrays on a local **1 km grid** and compute NDWI = (green − NIR)/(green + NIR). Thresholding is a toy method; a cloud mask is essential. Never compute this spectral index from a colored map screenshot.
'''), code('''
y,x=np.mgrid[:60,:80]; axis=35+7*np.sin(y/10)
before_water=np.abs(x-axis)<3
after_water=np.abs(x-axis)<(3+8*np.exp(-((y-30)/13)**2))
cloud=(x-59)**2+(y-20)**2 < 100
def synthetic_ndwi(water):
    green=np.where(water,.30,.16);nir=np.where(water,.06,.38)
    return (green-nir)/(green+nir)
before=synthetic_ndwi(before_water);after=synthetic_ndwi(after_water)
after[cloud]=np.nan
change=(after>0)&~(before>0)&np.isfinite(after)
fig,axes=plt.subplots(1,3,figsize=(13,4),constrained_layout=True)
observed_change=np.where(np.isfinite(after),change.astype(float),np.nan)
for ax,arr,title in zip(axes,[before,after,observed_change],['Before: synthetic NDWI','After: cloud masked','New water-like pixels']):
    im=ax.imshow(arr,origin='lower',cmap='BrBG',vmin=-1 if 'NDWI' in title or 'cloud' in title else 0,vmax=1,extent=[0,80,0,60]);ax.set(title=title,xlabel='Local x (km)',ylabel='Local y (km)')
    fig.colorbar(im,ax=ax,shrink=.7,label='new water mask (0/1)' if 'pixels' in title else 'NDWI (unitless)')
plt.show()
print('New water-like area among observed pixels:',int(change.sum()),'km² (synthetic 1 km² cells)')
print('Cloud/missing area:',int(cloud.sum()),'km²; excluded, not dry')
'''), md('''
## Lab challenge and Astra prompt
Change the threshold from 0 to 0.2, then expand the cloud mask. Explain why the observed area is not the total flooded area. Outline validation with a product quality layer, dates, sensor resolution, and independent field observations.

**Image-grounded prompt:** “Using this exported map, its legend, and the attached manifest, separate visible observations from hypotheses. Cite the layer/date for each observation. State what cloud and resolution prevent you from concluding. Do not infer disease, identify people, or estimate precise area from screenshot pixels.” In notebook 10, numerical evidence comes from computed arrays; Astra can help explain and critique it.

**Sources:** [NASA GIBS access guide](https://nasa-gibs.github.io/gibs-api-docs/access-basics/), [NASA Worldview source](https://github.com/nasa-gibs/worldview), [OpenAI image-input limitations](https://developers.openai.com/api/docs/guides/images-vision). No NASA imagery is bundled.
''')]
notebook('08_worldview_remote_sensing.ipynb', cells)

cells = lab('09 · 3D scenes, terrain intuition, and time', '''
**Mission (40 minutes):** compare an analytical 3D bar scene with a Cesium globe, scrub an invented logistics route, and examine why exaggerated height can change perception. This uses the same CesiumJS family as God's Eye View but is an original, standalone learning scene.
''')
cells += [md('''
## 1. Static 3D fallback: height encodes a rate
Height is a thematic variable, not terrain or building height. A 2D rate map from notebook 06 should accompany it because perspective and occlusion can make comparison harder.
'''), code('''
rates=np.array([s['rate_10000'] for s in stats])
fig=plt.figure(figsize=(10,6));ax=fig.add_subplot(111,projection='3d')
gx,gy=np.meshgrid(np.arange(4),np.arange(3))
ax.bar3d(gx.ravel(),gy.ravel(),np.zeros(12),.8,.8,rates,color=plt.cm.viridis(rates/rates.max()),shade=True)
ax.set(xlabel='Training grid column',ylabel='Training grid row',zlabel='Reported cases / 10,000',title='Fictional sectors · same data, different viewing geometry')
ax.view_init(30,-60);plt.show()
'''), md('''
## 2. Interactive Cesium scene
Switch 2D/3D, change the height scale, play/pause the route, and scrub the time strip. The grid globe uses an ellipsoid: **no photorealistic 3D, real terrain, Cesium ion token, or live tracked vehicles**. CDN access and WebGL are required. The scene explicitly labels its invented 5 km-high route.
'''), code("show_map(scenario,mode='3d',height=720)\ndownload('riverbend-3d.html',map_page(scenario,'3d'),'text/html')"), md('''
## 3. A deliberately simple terrain experiment
The water surface below is a horizontal threshold over an invented elevation grid. It does not enforce hydraulic connectivity, flow, drainage, or conservation of water; it is not a flood model.
'''), code('''
x=np.linspace(-20,20,65);y=np.linspace(-15,15,55);X,Y=np.meshgrid(x,y)
Z=110+25*np.sin(X/8)*np.cos(Y/7)+.4*X**2
water_level_m=120
fig=plt.figure(figsize=(11,5));ax=fig.add_subplot(111,projection='3d')
ax.plot_surface(X,Y,Z,cmap='terrain',alpha=.9,linewidth=0)
ax.plot_surface(X,Y,np.full_like(Z,water_level_m),color='#369bd2',alpha=.28)
ax.set(xlabel='Local x (km)',ylabel='Local y (km)',zlabel='Invented elevation (m)',title='Synthetic terrain + horizontal water plane · not hydrodynamics')
plt.show()
print('Grid cells below threshold:',round(float((Z<water_level_m).mean()*100),1),'%')
'''), md('''
## Lab challenge
Set thematic column scale to zero: which spatial relationships become easier to see? Rotate the static scene and describe occlusion. Raise the water plane by 10 m; identify a disconnected depression that a simple threshold might incorrectly classify as flooded.

**God's Eye View extension:** the integration adapter in notebook 12 loads the same GeoJSON in a local upstream viewer. Real terrain/photorealistic tiles require separate provider configuration and terms.

**Sources:** [Cesium Viewer](https://cesium.com/learn/cesiumjs/ref-doc/Viewer.html), [GeoJsonDataSource](https://cesium.com/learn/cesiumjs/ref-doc/GeoJsonDataSource.html), [SampledPositionProperty](https://cesium.com/learn/cesiumjs/ref-doc/SampledPositionProperty.html), [upstream license](https://github.com/bilawalsidhu/gods-eye-view/blob/main/LICENSE).
''')]
notebook('09_cesium_3d_scenes.ipynb',cells)

cells = lab('10 · GPT-6 Astra as a geospatial analysis partner', '''
**Mission (40 minutes):** prepare an evidence packet, construct a structured Responses API request, inspect a labeled illustrative response, and reject unsupported citations. The notebook runs without credentials. Optional live use happens in a separate local Python process with a server-side key, never in JupyterLite or GitHub Pages.

The documented model supports text/image input, reasoning, tool calling and structured outputs. The workflows below apply these general capabilities to maps; they are not evidence of a dedicated GIS engine or an accuracy guarantee. Distances, rates, and spatial tests stay in explicit code.
''')
cells += [code('''
from astra_contract import build_request, validate_briefing, example_briefing
import json
bundle=evidence_bundle()
request=build_request(bundle)
print('Model:',request['model'])
print('Aggregate reported cases:',bundle['metrics']['reported_cases'])
print('Evidence IDs:',[s['id'] for s in bundle['sources']])
download('evidence-bundle.json',bundle)
download('astra-request.json',request)
'''), md('''
## 1. Give Astra a bounded job
Ask for an exercise situation report, with every finding tied to a supplied source ID, explicit unknowns, and verification steps. Data text is evidence, not instructions. The request disables storage (`store: false`) and exposes no action tools. That setting is not a promise about all service retention; consult your deployment's data controls.

**Useful extensions:** critique a map legend; explain a denominator mismatch; generate a test for coordinate order; compare a map screenshot with its manifest; summarize authorized source documents; propose sensitivity analyses; draft a multilingual briefing for human review. No credentials are needed to study the request structure.
'''), code('''
print(request['instructions'])
print(json.dumps(request['text']['format'],indent=2))
'''), md('''
## 2. Validate an illustrative response
This deterministic fixture is **not an API response**. It demonstrates the schema and citation checks. Schema conformance is not factual validation; a reviewer must check each claim against the numerical packet and source provenance.
'''), code('''
brief=example_briefing(bundle)
validate_briefing(brief,bundle)
display(Markdown('### ILLUSTRATIVE FIXTURE — NOT MODEL OUTPUT'))
for finding in brief['findings']:
    print(finding['claim'],'Evidence:',', '.join(finding['evidence_ids']))
bad=json.loads(json.dumps(brief));bad['findings'][0]['evidence_ids']=['S999']
try:
    validate_briefing(bad,bundle)
except ValueError as error:
    print('Expected rejection:',error)
'''), md('''
## 3. Optional live run, outside the browser kernel
Download `evidence-bundle.json`. In a local checkout, run the following in a **terminal**, not a JupyterLite cell:

```bash
python tools/astra_brief.py --input evidence-bundle.json --output request.json
# Above: dry-run request only, no API call.
# Set OPENAI_API_KEY in the local process environment, then deliberately opt in:
python tools/astra_brief.py --input evidence-bundle.json --output briefing.json --live
```

For a map image you are authorized to send, add `--image map.png` to either command. The image is paired with the evidence packet, not used as a coordinate measurement system. `--live` incurs API usage and requires account access to `gpt-6-astra`. The CLI rejects invalid/unsupported response structures and unknown source IDs; refusals and incomplete responses are surfaced as errors. No live API call is part of CI.

To review the result in JupyterLite, upload `briefing.json` beside this notebook, load it with `json.loads(Path('briefing.json').read_text())`, and call `validate_briefing(result, bundle)`.

## Evaluation lab
Score a real response 0/1 on each: correct total, correct date window, known source IDs, reporting-delay caveat, no causal claim, no invented coordinates, clear next verification step. All seven are required before using the text in an **exercise** brief. Try a malicious instruction in a source description and confirm it does not change the task or lead to a fabricated citation.

**Sources verified 2 October 2026:** [GPT-6 Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra), [structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [images and vision](https://developers.openai.com/api/docs/guides/images-vision), [API data controls](https://developers.openai.com/api/docs/guides/your-data). Account availability and provider behavior may change.
''')]
notebook('10_astra_geospatial_analyst.ipynb',cells)

cells = lab('11 · Spatial pattern, uncertainty, and scale', '''
**Mission (40 minutes):** calculate global Moran's I, use a seeded permutation reference distribution, and show how aggregation changes a map. This is exploratory statistics on 12 fictional sectors, not an outbreak detector.
''')
cells += [md('''
## 1. Define “neighbor” before computing a pattern
The rectangles form a 3 × 4 grid. Rook neighbors share an edge. We use **symmetric binary weights**, with no diagonal self-neighbor, and a two-sided permutation comparison centered on the randomization expectation −1/(n−1).
'''), code('''
values=np.array([s['rate_10000'] for s in stats]);w=rook_weights()
observed=moran_i(values,w);expected=-1/(len(values)-1)
rng=np.random.default_rng(20261002)
permuted=np.array([moran_i(rng.permutation(values),w) for _ in range(999)])
p=(1+np.count_nonzero(np.abs(permuted-expected)>=abs(observed-expected)))/(len(permuted)+1)
fig,axes=plt.subplots(1,2,figsize=(12,4),constrained_layout=True)
axes[0].imshow(w,cmap='Blues');axes[0].set(title='Binary rook adjacency',xlabel='Sector index',ylabel='Sector index')
axes[1].hist(permuted,bins=30,color='#42b8ad',edgecolor='white');axes[1].axvline(observed,color='#ad442e',label=f'Observed I={observed:.3f}')
axes[1].axvline(expected,color='gray',linestyle='--',label='Randomization expectation')
axes[1].set(xlabel="Global Moran's I",ylabel='Permutations',title=f'Two-sided permutation p ≈ {p:.3f}');axes[1].legend();plt.show()
'''), md('''
A small permutation p-value is conditional on the chosen rates, weights, and exchangeability assumption. It is not the probability that an outbreak exists and does not identify a local hotspot. Unequal populations produce unequal precision, weakening simple rate-exchangeability assumptions.

## 2. Aggregation changes the visible pattern (MAUP)
Aggregate counts and denominators **before** dividing. The unweighted mean of sector rates generally differs from a pooled rate.
'''), code('''
counts=np.array([s['cases'] for s in stats]).reshape(3,4)
pop=np.array([s['population'] for s in stats]).reshape(3,4)
pooled_rows=rate_per_10000(counts.sum(axis=1),pop.sum(axis=1))
pooled_cols=rate_per_10000(counts.sum(axis=0),pop.sum(axis=0))
fig,axes=plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
axes[0].bar(range(3),pooled_rows,color='#169c96');axes[0].set(xlabel='Row grouping',ylabel='Reported cases / 10,000',title='Same reports, 3 regions')
axes[1].bar(range(4),pooled_cols,color='#d79536');axes[1].set(xlabel='Column grouping',ylabel='Reported cases / 10,000',title='Same reports, 4 regions')
upper=max(pooled_rows.max(),pooled_cols.max())*1.15
for ax in axes: ax.set_ylim(0,upper)
plt.show()
print('Pooled rate:',float(rate_per_10000(counts.sum(),pop.sum())))
print('Unweighted mean sector rate:',values.mean())
'''), md('''
## Lab challenge
Use queen adjacency (edge or corner) and compare I. Shuffle the rates; do you always get zero? Explain why selecting whichever weights gives the lowest p-value is misleading. Discuss ecological fallacy and why privacy protection needs more than hiding small numbers on a map.

**Check:** both row and column pooling conserve the total count and population. No local significance or causal conclusion follows from this global statistic.

**Sources:** [PySAL Moran reference](https://pysal.org/esda/stable/user-guide/global_morans_i.html) for the statistic and weighting conventions; [CDC analysis and interpretation](https://www.cdc.gov/field-epi-manual/php/chapters/analyze-interpret-data.html). The implementation is original NumPy and does not require PySAL in the browser.
''')]
notebook('11_spatial_uncertainty.ipynb',cells)

cells = lab('12 · Capstone: from notebooks to God’s Eye View', '''
**Mission (60–90 minutes):** act as an exercise analysis cell. Export a portable layer, a timed scene, a provenance manifest, and a source-backed briefing packet. Reopen the products in the browser or use the documented adapter in a local God's Eye View checkout.
''')
cells += [md('''
## 1. Validate the interchange
GeoJSON uses `[longitude, latitude]` in WGS 84 geographic coordinates. An in-range coordinate swap can still be wrong; inspect the map and compare expected bounds. Files contain no real patient records.
'''), code('''
validate_geojson(scenario)
coords=np.array([[s['lon'],s['lat']] for s in stats])
assert np.all((coords[:,0]>32)&(coords[:,0]<34))
assert np.all((coords[:,1]>7)&(coords[:,1]<9))
download('riverbend-analysis.geojson',scenario,'application/geo+json')
download('riverbend-scene.html',map_page(scenario,'3d'),'text/html')
'''), md('''
## 2. CZML for a time-enabled Cesium scene
This invented aircraft/relay trajectory is a display exercise at 5,000 m above the ellipsoid. It is not an operational route. CZML can be loaded with `Cesium.CzmlDataSource.load(...)`; the integration chapter shows direct CZML loading alongside the GeoJSON adapter.
'''), code('''
czml=[{'id':'document','version':'1.0','name':'Synthetic Riverbend route','clock':{
    'interval':'2026-09-15T12:00:00Z/2026-09-15T13:00:00Z','currentTime':AS_OF,'multiplier':120,'range':'LOOP_STOP'}},
    {'id':'training-relay','name':'Fictional logistics route — not navigable','availability':'2026-09-15T12:00:00Z/2026-09-15T13:00:00Z',
     'position':{'epoch':AS_OF,'cartographicDegrees':[0,32.71,7.64,5000,1800,32.90,7.78,5000,3600,33.09,7.61,5000]},
     'point':{'pixelSize':12,'color':{'rgba':[255,178,66,255]}},
     'path':{'width':3,'leadTime':3600,'trailTime':3600,'material':{'solidColor':{'color':{'rgba':[255,178,66,255]}}}}}]
download('riverbend-route.czml',czml)
download('evidence-bundle.json',evidence_bundle())
'''), md('''
## 3. A reviewable exercise handover
'''), code('''
import hashlib,json
manifest={'title':'Riverbend training handover','synthetic':True,'as_of':AS_OF,
          'layer_sha256':hashlib.sha256(json.dumps(scenario,sort_keys=True).encode()).hexdigest(),
          'hash_method':'SHA-256 of json.dumps(layer, sort_keys=True), UTF-8; not raw file bytes',
          'crs':'OGC:CRS84','period':'2026-09-01/2026-09-14','review_status':'NOT REVIEWED',
          'limitations':['Last 3 onset days incomplete','Invented flood fractions','No verified travel network','No causal attribution'],
          'upstream':'https://github.com/bilawalsidhu/gods-eye-view'}
download('handover-manifest.json',manifest)
for r in sorted(stats,key=lambda r:r['rate_10000'],reverse=True)[:3]:
    print(r['id'],f"{r['rate_10000']:.1f} reported episodes / 10,000",'population',r['population'])
'''), md('''
## Exercise injects
1. **Clinic C3 closes:** revisit access and capacity, not only its icon.
2. **Flood layer is 36 hours old:** mark stale evidence and request a timestamped update.
3. **Late reports arrive:** revise the onset curve and preserve the prior snapshot.
4. **Astra asserts a cause:** require evidence, reject unsupported text, and document the correction.
5. **Tile service fails:** brief from static maps and the saved aggregate tables.

## Deliverable rubric (10 points)
Two points each for: reproducible computation; correct units/denominators; readable 2D and 3D views; traceable sources and uncertainty; explicit human review and a next verification action. An unlabeled synthetic map or a patient-identifying export fails the exercise regardless of score.

**Integration:** see [God's Eye View integration](../integration.md) for the adapter, inspected upstream revision, installation point, and teardown. A standalone Cesium scene is not a claim that all upstream feeds run on static GitHub Pages.

**Sources:** [GeoJSON RFC 7946](https://www.rfc-editor.org/rfc/rfc7946), [Cesium CZML guide](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CZML-Guide), [upstream data terms](https://github.com/bilawalsidhu/gods-eye-view/blob/main/DATA_SOURCES.md).
''')]
notebook('12_capstone_response.ipynb',cells)

# Keep the original four notebooks; attach reproducible extensions only once.
extensions = {
'01': [md('''## EOC extension: a 3D ground trace and an evidence question
The longitude/latitude trace can be wrapped onto a unit sphere. These are surface subpoints, not the satellite altitude. Ask Astra to explain the assumptions and propose checks, then verify them in code. This simplified orbit is not a pass predictor.'''), code('''
phi,lam=np.deg2rad(lat),np.deg2rad(lon)
fig=plt.figure(figsize=(7,6));ax=fig.add_subplot(111,projection='3d')
u,v=np.meshgrid(np.linspace(0,2*np.pi,50),np.linspace(-np.pi/2,np.pi/2,25))
ax.plot_wireframe(np.cos(v)*np.cos(u),np.cos(v)*np.sin(u),np.sin(v),color='gray',alpha=.15,rstride=2,cstride=3)
ax.plot(np.cos(phi)*np.cos(lam),np.cos(phi)*np.sin(lam),np.sin(phi),color='#159c9a')
ax.set_box_aspect((1,1,1));ax.set(title='Synthetic ground trace on a unit sphere',xlabel='x / Earth radius',ylabel='y / Earth radius',zlabel='z / Earth radius');plt.show()
assert np.max(np.abs(lat)) <= inclination_deg + 1e-8
print('Lab: double altitude, rerun, and explain the change in period.')
''')],
'02':[md('''## EOC extension: minimum elevation shrinks visibility
For a spherical Earth and a ground minimum elevation e, the central angle is `acos(R/(R+h) × cos(e)) − e`. A link budget, payload swath, clouds, or terrain can shrink useful coverage further. This is not a sensor-detection guarantee.'''),code('''
elevations=np.array([0,5,10,20,30,60])
e=np.deg2rad(elevations)
angles=np.arccos(R_E/(R_E+altitude_km)*np.cos(e))-e
fig,ax=plt.subplots(figsize=(8,4));ax.plot(elevations,R_E*angles,'o-',color='#159c9a');ax.set(xlabel='Minimum ground elevation (degrees)',ylabel='Surface radius (km)',title='Geometric access shrinks as elevation requirement rises');ax.grid(alpha=.2);plt.show()
assert np.all(np.diff(angles)<0)
print('Lab: compare 10° and 30° at 550 km and 1,200 km.')
''')],
'03':[md('''## EOC extension: count geometry-visible spacecraft over time
An occupancy grid counts subpoints, not service coverage. Here we explicitly count satellites above a 10° ground-elevation mask at the Akobo map center using spherical geometry. This is synthetic line of sight, not usable communications, imagery revisit, or satellite availability.'''),code('''
from gev_lab import haversine_km, EARTH_KM
site_lat,site_lon=7.79293,33.00294
times=np.arange(0,6*3600+1,60)
elev=np.deg2rad(10)
visible=[]
for tick in times:
    count=0
    for alt,inc,raan,phase,plane in records:
        la,lo=subpoint(alt,inc,raan,phase,tick)
        central=haversine_km(site_lon,site_lat,lo,la)/EARTH_KM
        limit=np.arccos(R_E/(R_E+alt)*np.cos(elev))-elev
        count += central <= limit
    visible.append(count)
fig,ax=plt.subplots(figsize=(10,4));ax.step(times/3600,visible,where='post',color='#159c9a');ax.set(xlabel='Hours since synthetic epoch',ylabel='Spacecraft above 10° mask',title='Geometry-only access at the Akobo view center');ax.grid(alpha=.2);plt.show()
print('Sampled minutes with no geometry-visible craft:',sum(v==0 for v in visible[:-1]))
''')],
'04':[md('''## EOC extension: pair a basemap with dated evidence
A basemap is geographic context. It does not establish a current flood or outbreak. Record the acquisition date, product, quality mask, coordinate system, and observation provenance before drawing an analytical conclusion. See notebook 08 for dated NASA Worldview links and notebook 05 for a synthetic response overlay.

The exercise coordinate below is an invented offset, not a real clinic location. Range rings are distance cues, not travel-time isochrones.'''),code('''
from gev_lab import haversine_km, download
offset_lon,offset_lat=33.10,7.90
d=float(haversine_km(AKOBO_LON,AKOBO_LAT,offset_lon,offset_lat))
print(f'Distance to invented exercise point: {d:.2f} km (spherical great circle)')
download('akobo-view-notes.json',{'center_lon_lat':[AKOBO_LON,AKOBO_LAT],
    'provider':'Esri World Imagery','acquisition_date':'UNKNOWN — check provider metadata',
    'observation':'Basemap context only','filters':'CSS effects, not sensor bands'})
''')]
}
for path in sorted(ROOT.glob('0[1-4]_*.ipynb')):
    n=nbf.read(path,as_version=4)
    n.cells=[c for c in n.cells if 'gev-extension' not in c.metadata.get('tags',[])]
    for c in n.cells:
        # Correct the pre-existing Leaflet CSS SRI value.
        c.source=c.source.replace('sha256-p4NxAoJBhIINfQ3ynQWZ1QC6+Q3P9G1y5B+MZ4O2X4A=', 'sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=')
        c.source=c.source.replace("where is coverage concentrated?", "where are subpoints concentrated?")
        c.source=c.source.replace('for operational satellite propagation', 'for satellite propagation')
    for c in extensions[path.name[:2]]:
        c.metadata['tags']=['gev-extension'];n.cells.append(c)
    for i,c in enumerate(n.cells):
        c.id=hashlib.sha256((path.name+str(i)+c.source).encode()).hexdigest()[:12]
        if c.cell_type=='code': c.outputs=[];c.execution_count=None
    nbf.write(n,path)
print('Authored 8 new labs and extended 4 starter notebooks')
