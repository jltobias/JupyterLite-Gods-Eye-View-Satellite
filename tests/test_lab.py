"""Numerical, data-contract and failure-path tests; no external services."""
import copy
import itertools
import json
from pathlib import Path
import sys
import unittest
import numpy as np
import jsonschema

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'book/notebooks'))
sys.path.insert(0,str(ROOT/'tools'))
import gev_lab as lab
from astra_contract import build_request, validate_evidence, validate_briefing, example_briefing, BRIEFING_SCHEMA
from astra_brief import extract_briefing


class LabTests(unittest.TestCase):
    def test_geodesic_reference_cases(self):
        self.assertEqual(float(lab.haversine_km(0,0,0,0)),0)
        self.assertAlmostEqual(float(lab.haversine_km(0,0,90,0)),np.pi*lab.EARTH_KM/2,places=7)
        self.assertAlmostEqual(float(lab.haversine_km(179,0,-179,0)),2*np.pi/180*lab.EARTH_KM,places=7)
        self.assertTrue(np.isfinite(lab.haversine_km(0,0,180,0)))

    def test_denominators_and_intervals(self):
        self.assertEqual(float(lab.rate_per_10000(5,1000)),50)
        self.assertTrue(np.isnan(lab.rate_per_10000(5,0)))
        low,high=lab.wilson_interval([0,50,100],[100,100,100])
        self.assertTrue(np.all(low>=0) and np.all(high<=1))
        self.assertAlmostEqual(float(low[1]),1-float(high[1]))
        with self.assertRaises(ValueError):lab.wilson_interval(101,100)

    def test_moran_exact_randomization_expectation(self):
        w=lab.rook_weights(2,2)
        values=[1,2,3,4]
        exact=np.mean([lab.moran_i(x,w) for x in itertools.permutations(values)])
        self.assertAlmostEqual(exact,-1/3)
        self.assertAlmostEqual(lab.moran_i([0,1,1,0],w),-1)
        with self.assertRaises(ValueError):lab.moran_i([1,1,1,1],w)

    def test_data_integrity(self):
        data=lab.validate_geojson(lab.load_scenario())
        self.assertEqual(len(data['features']),16)
        self.assertEqual(len(lab.load_cases()),168)
        self.assertTrue(all(f['properties']['synthetic'] for f in data['features']))
        bundle=lab.evidence_bundle();validate_evidence(bundle)
        self.assertEqual(sum(r['cases'] for r in lab.load_cases()),bundle['metrics']['reported_cases'])
        bad=copy.deepcopy(data);bad['features'][0]['geometry']['coordinates'][0][-1]=[0,0]
        with self.assertRaises(ValueError):lab.validate_geojson(bad)
        bad=copy.deepcopy(data);bad['features'][0]['geometry']['coordinates'][0][0]=[200,95]
        with self.assertRaises(ValueError):lab.validate_geojson(bad)

    def test_prompt_and_response_boundary(self):
        bundle=lab.evidence_bundle();request=build_request(bundle)
        self.assertEqual(request['model'],'gpt-6-astra');self.assertFalse(request['store'])
        self.assertNotIn('tools',request)
        brief=example_briefing(bundle);validate_briefing(brief,bundle)
        jsonschema.validate(brief,BRIEFING_SCHEMA)
        bad=copy.deepcopy(bundle);bad['metrics']['sectors'][0]['patient_name']='not allowed'
        with self.assertRaises(ValueError):validate_evidence(bad)
        bad=copy.deepcopy(bundle);bad['metrics']['reported_cases']+=1
        with self.assertRaises(ValueError):validate_evidence(bad)
        brief['findings'][0]['evidence_ids']=['hallucinated']
        with self.assertRaises(ValueError):validate_briefing(brief,bundle)

    def test_api_refusals_and_incomplete(self):
        with self.assertRaises(ValueError):extract_briefing({'status':'incomplete'})
        with self.assertRaises(ValueError):extract_briefing({'status':'completed','output':[{'type':'message','content':[{'type':'refusal'}]}]})
        brief=example_briefing(lab.evidence_bundle())
        parsed=extract_briefing({'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(brief)}]}]})
        self.assertEqual(parsed,brief)

    def test_map_embedding_cannot_close_script(self):
        data=lab.styled_sectors();data['features'][0]['properties']['name']='</script><script>alert(1)</script>'
        page=lab.map_page(data)
        self.assertNotIn('</script><script>alert',page)
        self.assertNotIn('__SCENARIO_JSON__',page)


if __name__=='__main__':unittest.main()
