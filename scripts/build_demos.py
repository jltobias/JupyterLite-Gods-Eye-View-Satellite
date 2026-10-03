"""Publish standalone demos and a compact static analytical preview."""
from pathlib import Path
import sys
import json
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'book/notebooks'))
from gev_lab import map_page,styled_sectors,sector_summary,plot_sectors,evidence_bundle

dest=ROOT/'book/_static/demos';dest.mkdir(parents=True,exist_ok=True)
for mode in ('2d','3d'):
    (dest/f'riverbend-{mode}.html').write_text(map_page(mode=mode),encoding='utf-8')
(dest/'riverbend-analysis.geojson').write_text(json.dumps(styled_sectors(),indent=2)+'\n',encoding='utf-8')
(dest/'evidence-bundle.json').write_text(json.dumps(evidence_bundle(),indent=2)+'\n',encoding='utf-8')
stats=sector_summary()
fig,axes=plt.subplots(1,3,figsize=(14,4.5),constrained_layout=True)
fig.suptitle('RIVERBEND · FICTIONAL EXERCISE | 1–14 September 2026',fontsize=16,fontweight='bold')
for ax,key,title,unit in zip(axes,['cases','rate_10000','flood_fraction'],['Reported workload','Population-normalized reports','Invented flood fraction'],['reported first episodes','reports / 10,000','fraction (0–1)']):
    coll=plot_sectors(ax,[s[key] for s in stats],title)
    fig.colorbar(coll,ax=ax,shrink=.7,label=unit)
fig.savefig(ROOT/'book/assets/analytical-preview.png',dpi=160)
plt.close(fig)
print('Standalone 2D/3D demos, export fixtures, and analytical preview generated')
