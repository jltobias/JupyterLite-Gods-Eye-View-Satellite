"""Recreate the fictional Riverbend fixtures; never downloads real records."""
from pathlib import Path
import csv
import json
import math
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1] / "book/notebooks/data"


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    features, cases = [], []
    shape = [1, 1, 2, 3, 5, 8, 12, 16, 18, 17, 14, 12, 10, 8]
    for row in range(3):
        for col in range(4):
            i = row*4 + col
            key = f"S{i+1:02d}"
            west, south = round(32.6 + .2*col, 4), round(7.5 + .2*row, 4)
            east, north = round(west+.2, 4), round(south+.2, 4)
            pop = [4200, 6800, 3500, 9100, 5200, 8000, 2900, 6100, 7600, 4800, 5600, 3900][i]
            flood = round(.05 + .65 * math.exp(-((col-1.3)**2+(row-.8)**2)/1.3), 3)
            risk = [1.1, 1.6, .9, .6, 1.4, 2.8, 2.2, .7, .5, 1.3, .8, .4][i]
            props = dict(name=f"Training sector {key}", kind="sector", population=pop,
                         lon=round(west+.1,4), lat=round(south+.1,4), flood_fraction=flood,
                         synthetic=True, as_of="2026-09-15T12:00:00Z")
            features.append(dict(type="Feature", id=key, properties=props,
                                 geometry=dict(type="Polygon", coordinates=[[[west,south],[east,south],[east,north],[west,north],[west,south]]])))
            for d, wave in enumerate(shape):
                completeness = [1]*11 + [.75, .5, .25]
                observed = round(wave * risk * pop / 6000 * completeness[d])
                cases.append(dict(sector_id=key, onset_date=str(date(2026,9,1)+timedelta(days=d)), cases=observed,
                                  status="incomplete" if d >= 11 else "complete", synthetic="true"))
    for i, (lon, lat, capacity, available) in enumerate([(32.71,7.64,90,True),(33.09,7.61,70,True),(32.9,7.99,50,False)]):
        features.append(dict(type="Feature", id=f"C{i+1}", properties=dict(name=f"Fictional clinic {i+1}", kind="clinic",
                            capacity_day=capacity, available=available, synthetic=True), geometry=dict(type="Point", coordinates=[lon,lat])))
    features.append(dict(type="Feature", id="R1", properties=dict(name="Illustrative river axis",kind="river",synthetic=True),
                         geometry=dict(type="LineString",coordinates=[[32.72,7.48],[32.83,7.65],[32.91,7.82],[33.0,8.12]])))
    (ROOT/'riverbend.geojson').write_text(json.dumps(dict(type="FeatureCollection",features=features),indent=2)+'\n',encoding='utf-8')
    with (ROOT/'daily_cases.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(cases[0])); writer.writeheader(); writer.writerows(cases)
    print(f"Wrote {len(features)} fictional features and {len(cases)} aggregate rows")


if __name__ == '__main__':
    main()
