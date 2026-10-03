"""Check the final deployment artifact, helpers and locally linked destinations."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'book/_build/html'

class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src') and v:self.links.append(v)

def main():
    notebooks=list((ROOT/'book/notebooks').glob('*.ipynb'))
    assert len(notebooks)==12
    for path in notebooks:
        assert (SITE/'notebooks'/path.with_suffix('.html').name).exists(),path
        built=SITE/'lite/files'/path.name
        assert built.exists(),built
        assert json.loads(built.read_text(encoding='utf-8'))==json.loads(path.read_text(encoding='utf-8')),built
    for name in ('gev_lab.py','astra_contract.py','data/riverbend.geojson','data/daily_cases.csv','viewers/map2d.html','viewers/scene3d.html'):
        assert (SITE/'lite/files'/name).exists(),name
    for name in ('_static/demos/riverbend-2d.html','_static/demos/riverbend-3d.html','glossary.html','lite/lab/index.html'):
        assert (SITE/name).exists(),name
    errors=[]
    pages=[SITE/'intro.html',SITE/'integration.html',SITE/'glossary.html',*list((SITE/'notebooks').glob('*.html'))]
    for page in pages:
        parser=Links();parser.feed(page.read_text(encoding='utf-8'))
        for href in parser.links:
            url=urlsplit(href)
            if url.scheme or url.netloc or not url.path:continue
            dest=(SITE/url.path.lstrip('/')) if url.path.startswith('/') else (page.parent/unquote(url.path))
            if not dest.exists():errors.append((page.name,href))
    assert not errors,errors
    print('PASS: 12 rendered notebooks, 12 packaged notebooks, all helpers, demos, glossary and local links')

if __name__=='__main__':main()
