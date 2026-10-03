/* Original training adapter. MIT; see this repository's LICENSE.
 * Inspected against upstream e7707d9a0f34d9fbffc300023c319f95caa5be30.
 * No upstream source or third-party data is copied into this module.
 */
export function validateTrainingGeoJSON(data) {
  if (data?.type !== 'FeatureCollection' || !Array.isArray(data.features) || !data.features.length || data.features.length > 1000) {
    throw new Error('Expected 1–1000 synthetic GeoJSON features');
  }
  const ids = new Set();
  const point = p => {
    if (!Array.isArray(p) || p.length !== 2 || !p.every(Number.isFinite) || Math.abs(p[0]) > 180 || Math.abs(p[1]) > 90) {
      throw new Error('Coordinates must be [longitude, latitude]');
    }
  };
  for (const f of data.features) {
    if (f.type !== 'Feature' || f.properties?.synthetic !== true || typeof f.id !== 'string' || ids.has(f.id)) {
      throw new Error('Every feature needs a unique ID and synthetic: true');
    }
    ids.add(f.id);
    const g = f.geometry;
    if (g?.type === 'Point') point(g.coordinates);
    else if (g?.type === 'LineString') {
      if (!Array.isArray(g.coordinates) || g.coordinates.length < 2) throw new Error('Invalid line');
      g.coordinates.forEach(point);
    } else if (g?.type === 'Polygon') {
      if (!Array.isArray(g.coordinates) || !g.coordinates.length) throw new Error('Invalid polygon');
      for (const ring of g.coordinates) {
        if (!Array.isArray(ring) || ring.length < 4 || JSON.stringify(ring[0]) !== JSON.stringify(ring.at(-1))) throw new Error('Unclosed polygon');
        ring.forEach(point);
      }
    } else throw new Error('Only Point, LineString and Polygon are supported');
  }
  // Strip arbitrary display HTML and style/resource properties before Cesium loads it.
  return {type: 'FeatureCollection', features: data.features.map(f => ({
    type: 'Feature', id: f.id, geometry: f.geometry,
    properties: {name: `Synthetic ${f.id}`, synthetic: true, kind: String(f.properties.kind || 'training'),
      rate_10000: Number.isFinite(f.properties.rate_10000) ? f.properties.rate_10000 : 0}
  }))};
}

/** Mount a local-file GeoJSON loader in an existing Cesium viewer; return teardown. */
export function mountTrainingLayer({viewer, Cesium, requestRender = () => viewer.scene.requestRender()}) {
  if (!viewer?.container || !viewer?.dataSources) throw new Error('A live Cesium viewer is required');
  const panel = document.createElement('section');
  panel.setAttribute('aria-label', 'Synthetic training layer');
  panel.style.cssText = 'position:absolute;left:16px;bottom:64px;z-index:10000;background:#092237ee;color:#fff;padding:12px;max-width:340px;border:1px solid #49c9ba;border-radius:6px;font:13px system-ui';
  const title = document.createElement('strong');title.textContent = 'JupyterLite · SYNTHETIC EXERCISE';
  const input = document.createElement('input');input.type='file';input.accept='.geojson,.json';input.setAttribute('aria-label','Load synthetic training GeoJSON');input.style.cssText='display:block;margin:10px 0;max-width:310px';
  const toggle=document.createElement('button');toggle.textContent='Show / hide';
  const clear=document.createElement('button');clear.textContent='Remove layer';clear.style.marginLeft='8px';
  const status=document.createElement('p');status.setAttribute('role','status');status.textContent='Select the GeoJSON downloaded from notebook 12. No upload to a server.';
  panel.append(title,input,toggle,clear,status);viewer.container.append(panel);
  let layer=null,disposed=false,generation=0;
  function remove(){generation++;if(layer&&!viewer.isDestroyed()){viewer.dataSources.remove(layer,true);layer=null;requestRender()}}
  input.onchange=async()=>{
    const file=input.files[0];if(!file)return;
    const thisGeneration=++generation;
    input.disabled=true;
    try{
      if(file.size>2_000_000)throw new Error('File exceeds 2 MB exercise limit');
      const data=validateTrainingGeoJSON(JSON.parse(await file.text()));
      const next=await Cesium.GeoJsonDataSource.load(data,{clampToGround:false,stroke:Cesium.Color.CYAN,fill:Cesium.Color.CYAN.withAlpha(.35),markerColor:Cesium.Color.ORANGE});
      if(disposed||thisGeneration!==generation||viewer.isDestroyed()){next.entities.removeAll();return}
      if(layer)viewer.dataSources.remove(layer,true);
      layer=next;
      for(const e of layer.entities.values){e.description='Fictional training layer. Not a real outbreak or operational record.'}
      await viewer.dataSources.add(layer);requestRender();await viewer.flyTo(layer);
      if(!disposed)status.textContent=`Loaded ${data.features.length} synthetic features. Upstream provider credits remain unchanged.`;
    }catch(error){if(!disposed)status.textContent='Layer not loaded: '+error.message}
    finally{if(!disposed)input.disabled=false}
  };
  toggle.onclick=()=>{if(layer){layer.show=!layer.show;requestRender()}};
  clear.onclick=()=>{remove();status.textContent='Training layer removed.'};
  return ()=>{disposed=true;remove();panel.remove()};
}
