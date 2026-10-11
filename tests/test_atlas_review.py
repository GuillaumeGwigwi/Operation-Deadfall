import json,re,math,hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sources/site/atlas'
class AtlasReviewTest(unittest.TestCase):
 def test_all_positions_match_reviewed_map_anchors(self):
  ref=json.loads((SOURCE/'positions.json').read_text())
  self.assertEqual(hashlib.sha256((SOURCE/'assets/thay-joueurs.jpg').read_bytes()).hexdigest(),ref['imageSHA256'])
  d=json.loads((SOURCE/'atlas-data.js').read_text().removeprefix('window.THAY_ATLAS = ').strip().removesuffix(';'))
  points={p['id']:p for p in d['landmarks']}
  self.assertEqual(set(points),{a['id'] for a in ref['anchors']})
  self.assertEqual(len(points),46)
  errors=[]
  for a in ref['anchors']:
   p=points[a['id']]; actual=(p['x']*ref['width']/100,p['y']*ref['height']/100)
   error=math.dist(actual,a['pixel'])
   if error>.05: errors.append((a['id'],round(error,2)))
  self.assertEqual(errors,[], 'Décalage en pixels source par rapport aux ancres vérifiées')

 def test_template_has_no_redundant_map_text(self):
  text=(SOURCE/'index.template.html').read_text()
  for phrase in ['class="map-credit"','class="detail-notice"','id="atlas-notice"','Choisissez un repère sur la carte ou un lieu dans la liste']:
   self.assertNotIn(phrase,text)

 def test_media_has_no_visible_captions_or_author_labels(self):
  code=(SOURCE/'atlas.js').read_text()
  self.assertNotIn("el('figcaption')",code)
  self.assertNotIn('Le viseur indique',code)
  self.assertNotIn('Illustration : ${l.credit}',code)
if __name__=='__main__': unittest.main()
