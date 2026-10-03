// Syntax and interchange checks, not a browser/WebGL smoke test.
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const root=new URL('../',import.meta.url);
const source=readFileSync(new URL('integrations/gods-eye-view/training-layer.js',root),'utf8');
const {validateTrainingGeoJSON}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
const fixture=()=>JSON.parse(readFileSync(new URL('book/_static/demos/riverbend-analysis.geojson',root),'utf8'));

test('inline scripts in both published demos compile',()=>{
  for(const mode of ['2d','3d']){
    const html=readFileSync(new URL(`book/_static/demos/riverbend-${mode}.html`,root),'utf8');
    for(const match of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)){
      new vm.Script(match[1],{filename:`riverbend-${mode}.html`});
    }
  }
});

test('adapter accepts notebook layer and strips untrusted presentation fields',()=>{
  const data=fixture();
  data.features[0].properties.description='<img src=x onerror=alert(1)>';
  data.features[0].properties['marker-symbol']='https://example.invalid/tracker';
  const clean=validateTrainingGeoJSON(data);
  assert.equal(clean.features.length,16);
  assert.equal(clean.features[0].properties.description,undefined);
  assert.equal(clean.features[0].properties['marker-symbol'],undefined);
  assert.equal(clean.features[0].properties.name,'Synthetic S01');
});

test('adapter rejects non-exercise data, invalid coordinates and duplicate IDs',()=>{
  for(const mutate of [
    d=>d.features[0].properties.synthetic=false,
    d=>d.features[0].geometry.coordinates[0][0]=[200,95],
    d=>d.features[0].geometry.coordinates[0].pop(),
    d=>d.features[1].id=d.features[0].id,
    d=>d.features[0].geometry.type='GeometryCollection',
  ]){
    const data=fixture();mutate(data);
    assert.throws(()=>validateTrainingGeoJSON(data));
  }
});

test('adapter rejects oversize and empty collections',()=>{
  assert.throws(()=>validateTrainingGeoJSON({type:'FeatureCollection',features:[]}));
  assert.throws(()=>validateTrainingGeoJSON({type:'FeatureCollection',features:Array(1001).fill(fixture().features[0])}));
});
